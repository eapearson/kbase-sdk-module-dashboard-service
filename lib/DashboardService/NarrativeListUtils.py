from time import time
import pylru
import itertools
from DashboardService.ServiceUtils import ServiceUtils
from DashboardService.cache.ObjectCache import ObjectCache

# For reference:
#   workspace_info:
#     0 ws_id id
#     1 ws_name workspace
#     2 username owner
#     3 timestamp moddate
#     4 int max_objid
#     5 permission user_permission
#     6 permission globalread
#     7 lock_status lockstat
#     8 usermeta metadata


class NarrativeInfoCache(object):

    def __init__(self, cache_size):
        self.cache = pylru.lrucache(int(cache_size))

    def clear_cache(self):
        self.cache.clear()

    def check_cache_size(self):
        return len(self.cache)

    def get_info_list(self, ws_lookup_table, wsClient):
        '''
            Given a set of WS info, lookup the corresponding Narrative
            information.

            input:
                ws_lookup_table = dict of ws_id -> workspace_info
            output:
                [{
                    'ws': workspace_info,
                    'nar': narrative_info
                 },
                 ...
                 ]
        '''
        # search the cache and extract what we have, mark what was missed
        res = self._search_cache(ws_lookup_table)
        items = res['items']
        missed_items = res['missed']

        # for objects that were missed, we have to go out and fetch that
        # narrative object info
        all_items = items
        if len(missed_items) > 0:
            more_items = self._fetch_objects_and_cache(missed_items,
                                                       ws_lookup_table,
                                                       wsClient)
            all_items += more_items

        return all_items

    def _search_cache(self, ws_lookup_table):
        items = []  # =[{'ws': [...], 'nar': [...]}, ...]
        missed = []  # =[ws_info1, ws_info2, ... ]
        for ws_info in ws_lookup_table.itervalues():
            key = self._get_cache_key(ws_info)
            if key in self.cache:
                items.append({'ws': ws_info, 'nar': self.cache[key]})
            else:
                missed.append(ws_info)
        return {'items': items, 'missed': missed}

    def _fetch_objects_and_cache(self, ws_list, full_ws_lookup_table, 
                                 wsClient):
        '''
        Fetches narrative objects (if possible) for everything in ws_list
        '''
        obj_ref_list = []
        for ws_info in ws_list:
            if 'narrative' not in ws_info[8]:
                continue
            if (not ws_info[8]['narrative'].isdigit() or not
                    int(ws_info[8]['narrative']) > 0):
                continue
            ref = str(ws_info[0]) + '/' + str(ws_info[8]['narrative'])
            obj_ref_list.append({'ref': ref})

        if len(obj_ref_list) == 0:
            return []

        # ignore errors
        get_obj_params = {'objects': obj_ref_list,
                          'includeMetadata': 1,
                          'ignoreErrors': 1}
        narrative_list = wsClient.get_object_info3(get_obj_params)['infos']

        items = []
        for nar in narrative_list:
            if nar:
                ws_info = full_ws_lookup_table[nar[6]]
                items.append({'ws': ws_info, 'nar': nar})
                self.cache[self._get_cache_key(ws_info)] = nar
        return items

    def _get_cache_key(self, ws_info):
        return str(ws_info[0]) + '__' + str(ws_info[3])


# This is a variation of the NarrativeInfoCache.
# It differs in the following ways:
# - caches the raw object info converted to a dict
# - get_object_info_for_workspaces a parallel list of narrative objects for workspaces
#   That is, it can be used to zip up with the source workspaces.
# TODO: should figure out how to remove obsolete cache entries. When a workspace is 
# updated and the mod date newer, a new narrative object will be fetched. The old
# version, indexed with some unknown older mod date, will remain.
# A bit slower is that we could cache just by the workspace id, store the ws info 
# along with the obj info in the cache, and then compare the mod date for the fetched
# ws info with the existing ws info.
class ObjectInfoCache(object):

    def __init__(self, cache_size):
        self.cache = pylru.lrucache(int(cache_size))

    def clear_cache(self):
        self.cache.clear()

    def check_cache_size(self):
        return len(self.cache)

    def dump_keys(self):
        return list(self.cache.keys())

    def get_object_info_for_workspaces(self, workspaces, ws_client):
        '''
            Given a set of WS info, lookup the corresponding Narrative
            information.

            input:
                ws_lookup_table = dict of ws_id -> workspace_info
            output:
                [{
                    'ws': workspace_info,
                    'nar': narrative_info
                 },
                 ...
                 ]
        '''
        # find items not in the cache, we need to fetch those.
        to_lookup = [(self._make_key(ws_info), ws_info) for ws_info in workspaces]
        missing = self.find_missing(to_lookup)
        if len(missing) > 0:
            self.sync(missing, ws_client)
        found, missed = self.search_cache(to_lookup)
        return found, missing, missed

    def search_cache(self, to_lookup):
        found_items = []  # list of object info
        missed = []  # list of workspace info
        for (key, ws_info) in to_lookup:
            if key in self.cache:
                found_items.append(self.cache[key])
            else:
                found_items.append(None)
                missed.append((key, ws_info))
        return (found_items, missed)

    def find_missing(self, to_find):
        missing = []  # list of workspace info
        for (key, ws_info) in to_find:
            if key not in self.cache:
                missing.append((key, ws_info))
        return missing

    def sync(self, to_fetch, ws_client):
        ''' 
        Fetches narrative objects (if possible) for everything in ws_list
        '''
        obj_ref_list = []
        for _, ws_info in to_fetch:
            ref = str(ws_info['id']) + '/' + ws_info['metadata']['narrative']
            obj_ref_list.append({'ref': ref})

        if len(obj_ref_list) == 0:
            return []

        # Get all requested object info, ignoring errors, which sets an item
        # to null (None) if an error was encountered fetching that one.
        get_obj_params = {'objects': obj_ref_list,
                          'includeMetadata': 1,
                          'ignoreErrors': 1}
        obj_infos = ws_client.get_object_info3(get_obj_params)['infos']

        # Loop over the results, converting info raw tuples to friendler
        # dictionaries (friendlier here, and for returning via the api)
        # and caching them too
        result = []
        for (key, ws_info), obj_info in itertools.izip(to_fetch, obj_infos):
            if obj_info:
                obj_info2 = ServiceUtils.objectInfoToObject(obj_info)
                result.append(obj_info2)
                self.cache[key] = obj_info2
            else:
                result.append(None)
        return result

    def _make_key(self, ws_info):
        # The cache key is based on the workspace id and modification date
        # this keeps it naturally "fresh"
        return str(ws_info['id']) + '_' + str(ws_info['moddate'])


def parse_app_key(key):
    parts = (list(filter(
                lambda part: len(part) > 0,
                key.split('/'))))
    if len(parts) == 1:
        return {
            'name': parts[0],
            'shortRef': parts[0],
            'ref': parts[0]
        }
    elif len(parts) == 3:
        return {
            'module': parts[0],
            'name': parts[1],
            'gitCommitHash': parts[2],
            'shortRef': parts[0] + '/' + parts[1],
            'ref': parts[0] + '/' + parts[1] + '/' + parts[2]
        }
    elif len(parts) == 2:
        return {
            'module': parts[0],
            'name': parts[1],
            'shortRef': parts[0] + '/' + parts[1],
            'ret': parts[0] + '/' + parts[1]
        }
    else:
        return None


def get_path(from_dict, path):
    current_dict = from_dict
    for el in path:
        if not isinstance(current_dict, dict):
            return None
        if el not in current_dict:
            return None
        current_dict = current_dict[el]
    return current_dict


class NarrativeListUtils(object):

    def __init__(self, cache_size, app_cache, user_profile_cache):
        self.narrativeInfo = NarrativeInfoCache(cache_size)
        self.objectInfo = ObjectInfoCache(cache_size)
        self.app_cache = app_cache
        self.user_profile_cache = user_profile_cache
        # self.config = config
        # self.cache = cache

    def list_all_narratives(self, ctx, clients):
        # current_username = ctx['user_id']
        stats = []
        then = time()
        ws_arg = {'meta': {'is_temporary': 'false'}}
        ws_list = clients['Workspace'].list_workspace_info(ws_arg)
        now = time()
        stats.append(['list_workspace', now - then])
        then = now
        
        # This will filter out invalid narratives - we've already filter for 
        # "probably valid narrative workspace" above.
        # This gives us a list of workspace info but transformed to a 
        # dictionary.
        narrative_workspaces = list(
            map(
                lambda nar_ws: ServiceUtils.workspaceInfoToObject(nar_ws),
                filter(
                    lambda ws_info: self.is_valid_narrative_workspace(ws_info),
                    ws_list)))

        # PERMISSIONS
        # Now get permissions for each workspace.
        workspaces_for_perms = [{'id': ws_info['id']} for ws_info in narrative_workspaces]
        
        workspaces_perms = clients['Workspace'].get_permissions_mass({
            'workspaces': workspaces_for_perms
        })['perms']
        now = time()
        stats.append(['get_permissions', now - then])
        then = now

        narrative_workspaces_perms = list(
            map(
                lambda perms: list(
                    filter(
                        # lambda p: p['username'] != current_username and p['username'] != '*',
                        lambda p: p['username'] != '*',
                        map(
                            lambda (username, perm): {'username': username, 'perm': perm},
                            perms.iteritems()
                        )
                    )
                ),
                workspaces_perms
            )
        )

        # PROFILE PER USER
        # Get all profiles for all users in the permissions list. It is returned with the 
        # response so that the caller can map usernames to profiles.
        users = set()
        for perms in narrative_workspaces_perms:
            for perm in perms:
                users.add(perm['username'])
        usernames = list(users)

        fetched_profiles = self.user_profile_cache.get(usernames)

        profiles = dict()
        for (username, realname, avatar_option,
             gravatar_default, gravatar_hash) in fetched_profiles:
            profiles[username] = {
                'username': username,
                'realname': realname,
                'avatarOption': avatar_option,
                'gravatarHash': gravatar_hash,
                'gravatarDefault': gravatar_default
            }

        # profiles_list = self.user_profile_cache.find(usernames=usernames)
        # profiles = dict()

        # for username, profile in itertools.izip(usernames, profiles_list):
        #     if profile is not None:
        #         profiles[username] = {
        #             'username': profile['user']['username'],
        #             'realname': profile['user']['realname'],
        #             'avatarOption': get_path(profile, ['profile', 'userdata', 'avatarOption']),
        #             'gravatarHash': get_path(profile, ['profile', 'synced', 'gravatarHash']),
        #             'gravatarDefault': get_path(profile, ['profile', 'gravatarDefault'])
        #         }
        #     else:
        #         profiles[username] = None
                
        now = time()
        stats.append(['user_profiles', now - then])
        then = now

        # NARRATIVE OBJECT
        # based on the WS lookup table, lookup the narratives
        # narrative_objects, _missing, _missed = self.objectInfo.get_object_info_for_workspaces(
        #     narrative_workspaces, clients['Workspace'])

        object_cache = self.object_cache.newInstance(token=ctx['token'])
        # convert to the cache format, which includes the mod date as timestamp
        # NB: includes object id, because the key should have enough info to fetch
        # the object from storage as well as form a unique key
        to_get = [(ws['id'],
                  int(ws['metadata']['narrative']),
                  ws['modDateMs']) for ws in narrative_workspaces]
        narrative_objects = object_cache.get(to_get)

        # stats.append(['missing', missing])
        # stats.append(['missed', len(missed)])
        # stats.append(['check cache', self.objectInfo.check_cache_size()])
        # stats.append(['cache keys', self.objectInfo.dump_keys()])

        now = time()
        stats.append(['narrative_objects', now - then])
        then = now

        # APPS
        # Gather all apps in this narrative, 
        # Get the apps
        # Profile a map of apps for a given tag
        
        narrative_apps = []
        narrative_cell_types = []
        for obj_info in narrative_objects:
            cell_types = {
                'app': 0,
                'code': 0,
                'markdown': 0
            }
            apps = []
            if obj_info is not None:
                for key in obj_info['metadata'].keys():
                    key_parts = key.split('.')
                    if key_parts[0] == 'method' or key_parts[0] == 'app':
                        parsed_id = parse_app_key(key_parts[1])

                        app = {
                            # 'key': key_parts[1],
                            'id': parsed_id,
                            'count': int(obj_info['metadata'][key]),
                            'obsolete': True
                        }

                    if key_parts[0] == 'method':
                        parsed_id = parse_app_key(key_parts[1])

                        app = {
                            # 'key': key_parts[1],
                            'id': parsed_id,
                            'count': int(obj_info['metadata'][key])
                        }

                        app_ref = parsed_id['shortRef']
                        app_spec = self.app_cache.find(app_ref)

                        if app_spec is None:
                            app['notFound'] = True
                        else:
                            app_icon_url = None
                            if 'icon' in app_spec['info']:
                                app_icon_url = app_spec['info']['icon']['url']
                            app['title'] = app_spec['info']['name']
                            app['subtitle'] = app_spec['info']['subtitle']
                            app['iconUrl'] = app_icon_url
               
                        apps.append(app)
                        cell_types['app'] += 1

                    elif key_parts[0] == 'ipython' or key_parts[0] == 'jupyter':
                        if key_parts[1] not in cell_types:
                            cell_types[key_parts[1]] = 0
                        cell_types[key_parts[1]] += int(obj_info['metadata'][key])

            narrative_apps.append(apps)
            narrative_cell_types.append(cell_types)

        # TODO: permissions, user profiles for permissions, apps

        narratives = []
        for (ws,
             obj,
             perms,
             cell_stats,
             apps) in itertools.izip(narrative_workspaces,
                                     narrative_objects,
                                     narrative_workspaces_perms,
                                     narrative_cell_types,
                                     narrative_apps):
                if obj is None:
                    continue
                narratives.append({
                    'workspaceId': ws['id'],
                    'objectId': obj['id'],
                    'objectVersion': obj['version'],
                    'owner': ws['owner'],
                    'permission': ws['user_permission'],
                    'isPublic': ws['isPublic'],
                    'isNarratorial': ws['isNarratorial'],
                    'title': ws['metadata']['narrative_nice_name'],
                    'modifiedTime': ws['modDateMs'],
                    'savedTime': obj['saveDateMs'],
                    'savedBy': obj['saved_by'],
                    'permissions': perms,
                    'cellTypes': cell_stats,
                    'apps': apps
                })

        # narratives = map(
        #     lambda ws, obj, perms, cell_stats, apps:
        #         {
        #             'workspaceId': ws['id'],
        #             'objectId': obj['id'],
        #             'objectVersion': obj['version'],
        #             'owner': ws['owner'],
        #             'permission': ws['user_permission'],
        #             'isPublic': ws['isPublic'],
        #             'isNarratorial': ws['isNarratorial'],
        #             'title': ws['metadata']['narrative_nice_name'],
        #             'modifiedTime': ws['modDateMs'],
        #             'savedTime': obj['saveDateMs'],
        #             'savedBy': obj['saved_by'],
        #             'permissions': perms,
        #             'cellTypes': cell_stats,
        #             'apps': apps
        #         },
        #         # {'workspace_info': ws,
        #         #  'permissions': perms,
        #         #  'object_info': obj,
        #         #  'cell_stats': cell_stats,
        #         #  'apps': apps},
        #     narrative_workspaces, narrative_objects, narrative_workspaces_perms,
        #     narrative_cell_types, narrative_apps)

        # cleaned = list(
        #     filter(
        #         lambda narrative: narrative['object_info'] is not None,
        #         narratives
        #     )
        # )

        now = time()
        stats.append(['finalize', now - then])
        then = now
        result = {
            'narratives': narratives,
            'profiles': profiles
        }
        return result, stats

    def list_public_narratives(self, wsClient):
        # get all the workspaces marked as narratorials
        ws_arg = {
            'meta': {'is_temporary': 'false'}
        }
        ws_list = wsClient.list_workspace_info(ws_arg)
        ws_global_list = []
        for ws_info in ws_list:
            if ws_info[6] == 'r':  # this ws is globally readable
                ws_global_list.append(ws_info)
        # build a ws_list lookup table
        ws_lookup_table = self._build_ws_lookup_table(ws_global_list)
        # based on the WS lookup table, lookup the narratives
        return self.narrativeInfo.get_info_list(ws_lookup_table, wsClient)

    def list_my_narratives(self, my_user_id, wsClient):
        # get all the workspaces marked as narratorials
        ws_arg = {
            'owners': [my_user_id],
            'meta': {'is_temporary': 'false'}
        }
        ws_list = wsClient.list_workspace_info(ws_arg)
        # build a ws_list lookup table
        ws_lookup_table = self._build_ws_lookup_table(ws_list)
        # based on the WS lookup table, lookup the narratives
        return self.narrativeInfo.get_info_list(ws_lookup_table, wsClient)

    def list_shared_narratives(self, my_user_id, wsClient):
        # get all the workspaces marked as narratorials
        ws_arg = {
            'meta': {'is_temporary': 'false'}
        }
        ws_list = wsClient.list_workspace_info(ws_arg)
        ws_shared_list = []
        for ws_info in ws_list:
            if ws_info[2] == my_user_id:
                continue
            if ws_info[5] == 'n':  # this ws is globally readable
                continue
            ws_shared_list.append(ws_info)
        # build a ws_list lookup table
        ws_lookup_table = self._build_ws_lookup_table(ws_shared_list)
        # based on the WS lookup table, lookup the narratives
        return self.narrativeInfo.get_info_list(ws_lookup_table, wsClient)

    def list_narratorials(self, wsClient):
        # get all the workspaces marked as narratorials
        ws_list = wsClient.list_workspace_info({'meta': {'narratorial': '1'}})
        # build a ws_list lookup table
        ws_lookup_table = self._build_ws_lookup_table(ws_list)
        # based on the WS lookup table, lookup the narratives
        return self.narrativeInfo.get_info_list(ws_lookup_table, wsClient)

    def is_valid_narrative_workspace(self, ws_info):
        if 'narrative' in ws_info[8]:
            if (ws_info[8]['narrative'].isdigit() and
                    int(ws_info[8]['narrative']) > 0):
                return True
        return False

    def _build_ws_lookup_table(self, ws_list):
        ''' 
        builds a lookup table, skips anything without a 'narrative' metadata
        field set
        '''
        ws_lookup_table = {}
        for ws_info in ws_list:
            if 'narrative' in ws_info[8]:
                if (ws_info[8]['narrative'].isdigit() and 
                        int(ws_info[8]['narrative']) > 0):
                    ws_lookup_table[ws_info[0]] = ws_info
        return ws_lookup_table


class NarratorialUtils(object):

    def __init__(self):
        pass

    def _get_workspace_identity(self, wsid):
        if str(wsid).isdigit():
            return {'id': int(wsid)}
        else:
            return {'workspace': str(wsid)}

    def set_narratorial(self, wsid, description, wsClient):
        wsi = self._get_workspace_identity(wsid)
        wsClient.alter_workspace_metadata({
            'wsi': wsi,
            'new': {'narratorial': '1'}})
        wsClient.alter_workspace_metadata({
            'wsi': wsi,
            'new': {
                'narratorial_description': description}})

    def remove_narratorial(self, wsid, wsClient):
        wsi = self._get_workspace_identity(wsid)
        wsClient.alter_workspace_metadata({
            'wsi': wsi,
            'remove': ['narratorial', 'narratorial_description']})
