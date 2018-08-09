import time
import itertools
import uuid
from DashboardService.GenericClient import GenericClient
from DashboardService.DynamicServiceClient import DynamicServiceClient
from DashboardService.ServiceUtils import ServiceUtils
from DashboardService.cache.UserProfileCache import UserProfileCache
from DashboardService.cache.AppCache import AppCache
from DashboardService.cache.ObjectCache import ObjectCache
from DashboardService.cache.PermissionsCache import PermissionsCache


class WorkspaceIdentity(object):
    def __init__(self, workspace=None, id=None, timestamp=None):
        if (workspace is None):
            if (id is None):
                raise ValueError('either "workspace" or "id" are required')   
        elif (id is not None):
            raise ValueError('only one of "workspace" or "id" may be provided')
        self._name = workspace
        self._id = id

        # also optional timestamp;
        self._timestamp = timestamp

    def make_wsi(self):
        return {
            'id': self._id
        }

    def workspace(self):
        return self._name

    def name(self):
        return self._name

    def id(self):
        return self._id

    def timestamp(self):
        return self._timestamp


class ObjectIdentity(object):
    def __init__(self, workspace_id=None, object_id=None, version=None):
        if (workspace_id is None):
            raise ValueError('"workspace_id" is required for object identity')
        if (object_id is None):
            raise ValueError('"object_id" is required for object identity')

        self._workspace_id = workspace_id
        self._object_id = object_id
        self._version = version

    def workspace_id(self):
        return self._workspace_id
    
    def object_id(self):
        return self._object_id

    def version(self):
        return self._version


class Model(object):
    def __init__(self, config=None, token=None, username=None):
        self.config = config
        self.token = token
        self.username = username
        self.narrative_workspaces = None
        self.app_cache = AppCache(
            narrative_method_store_url=self.config['services']['NarrativeMethodStore'],
            path=self.config['caches']['app']['path']
        )

    def fetch_narrative_workspaces(self):
        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )
        [ws_list] = rpc.call_func('list_workspace_info', [
             {'meta': {'is_temporary': 'false'}}
        ])

        # This will filter out invalid narratives - we've already filter for
        # "probably valid narrative workspace" above.
        # This gives us a list of workspace info but transformed to a
        # dictionary.
        self.narrative_workspaces = list(
            map(
                lambda nar_ws: ServiceUtils.ws_info_to_object(nar_ws),
                filter(
                    lambda ws_info: self.is_valid_narrative_workspace(ws_info),
                    ws_list)))

        return self.narrative_workspaces

    def is_valid_narrative_workspace(self, ws_info):
        metadata = ws_info[8]
        if 'narrative' in metadata:
            if (metadata['narrative'].isdigit() and
                    int(metadata['narrative']) > 0):
                return True
        return False

    def parse_apps(self, narrative_objects):
        narrative_apps = []
        narrative_cell_types = []
        query_time = 0

        for obj_info in narrative_objects:
            cell_types = {
                'app': 0,
                'code': 0,
                'markdown': 0
            }
            apps = []
            if obj_info is not None:
                # print('obj info...', obj_info)
                for key in obj_info['metadata'].keys():
                    key_parts = key.split('.')
                    if key_parts[0] == 'method' or key_parts[0] == 'app':
                        parsed_id = ServiceUtils.parse_app_key(key_parts[1])
                        if parsed_id is None:
                            continue

                        app = {
                            # 'key': key_parts[1],
                            'id': parsed_id,
                            'count': int(obj_info['metadata'][key]),
                            'obsolete': True
                        }

                    if key_parts[0] == 'method':
                        parsed_id = ServiceUtils.parse_app_key(key_parts[1])
                        if parsed_id is None:
                            continue

                        app_ref = parsed_id['shortRef']
                        start = time.time()
                        tag, app_info = self.app_cache.get(app_ref)
                        query_time += (time.time() - start)

                        # 'key': key_parts[1],
                        app = {
                            'id': parsed_id,
                            'count': int(obj_info['metadata'][key]),
                            'tag': tag
                        }

                        # print('app info??', app_ref, app_info)
                        if app_info is None:
                            app['notFound'] = True
                        else:
                            app_icon_url = None
                            # if 'info' not in app_spec:
                            #     raise ValueError('"info" key not found in app spec ' + app_ref)
                            if 'icon' in app_info:
                                app_icon_url = app_info['icon']['url']
                            else:
                                app_icon_url = None
                            app['title'] = app_info['name']
                            app['subtitle'] = app_info['subtitle']
                            app['iconUrl'] = app_icon_url

                        apps.append(app)
                        cell_types['app'] += 1

                    elif key_parts[0] == 'ipython' or key_parts[0] == 'jupyter':
                        if key_parts[1] not in cell_types:
                            cell_types[key_parts[1]] = 0
                        cell_types[key_parts[1]] += int(obj_info['metadata'][key])

            # condense apps into just one instance per module.id
            apps_map = dict()
            for app in apps:
                ref = app['id']['shortRef']
                if ref not in apps_map:
                    apps_map[ref] = app
                else:
                    apps_map[ref]['count'] += app['count']

            final_apps = [v for _, v in apps_map.iteritems()]

            narrative_apps.append(final_apps)
            narrative_cell_types.append(cell_types)
        return narrative_apps, narrative_cell_types, query_time

    def list_all_narratives(self):
        # current_username = ctx['user_id']
        stats = []
        then = time.time()

        # WORKSPACES
        print('getting workspaces...')
        narrative_workspaces = sorted(
            self.fetch_narrative_workspaces(),
            key=lambda x: x.get('id')
        )
        now = time.time()
        stats.append(['list_workspace', now - then])
        then = now

        # NB - all workpace/narrative related data below must be 
        # eventually formed into a list with the same order as the
        # narrative workspaces.

        # PERMISSION
        print('getting permissions...')
        # TODO: we need to ensure that at the very least the items which are 
        # returned are returned in the same order requested. This will allow us
        # to weave the results back together in the end.
        workspace_cache = PermissionsCache(
            workspace_url=self.config['services']['Workspace'],
            path=self.config['caches']['workspace']['path'],
            username=self.username,   # just use the token for now...
            token=self.token
        )
        workspaces_to_get = [ws['id'] for ws in narrative_workspaces]
        narrative_workspaces_perms = workspace_cache.get(workspaces_to_get)
        now = time.time()
        stats.append(['get_permissions', now - then])
        then = now

        # PROFILE PER USER
        print('getting profiles...')
        # Get all profiles for all users in the permissions list. It is returned with the
        # response so that the caller can map usernames to profiles.
        users = set()
        for perms in narrative_workspaces_perms:
            for username, _perm in perms:
                users.add(username)

        # print('USERS?', list(users))

        # We end up with a map of username -> profile
        # Transform profiles into map of user to record.
        # The profile record itself is simplified down to just what
        # we need
        profiles_cache = UserProfileCache(
            user_profile_url=self.config['services']['UserProfile'],
            path=self.config['caches']['userprofile']['path'])
        profiles = profiles_cache.get(list(users))
        # profiles_map = dict()
        # for (username, profile) in itertools.izip(users, profiles):
        #     profiles_map[username] = profile

        now = time.time()
        stats.append(['user_profiles', now - then])
        then = now

        # NARRATIVE OBJECT
        # based on the WS lookup table, lookup the narratives
        # narrative_objects, _missing, _missed = self.objectInfo.get_object_info_for_workspaces(
        #     narrative_workspaces, clients['Workspace'])
        object_cache = ObjectCache(
            workspace_url=self.config['services']['Workspace'],
            path=self.config['caches']['object']['path'],
            token=self.token
        )
        # object_cache.start()

        # object_cache = object_cache.newInstance(token=ctx['token'])
        # convert to the cache format, which includes the mod date as timestamp
        # NB: includes object id, because the key should have enough info to fetch
        # the object from storage as well as form a unique key
        to_get = [(ws['id'],
                  int(ws['metadata']['narrative']),
                  ws['modDateMs']) for ws in narrative_workspaces]

        # to_get = [(ws['id'],
        #           int(ws['metadata']['narrative']))
        #           for ws in narrative_workspaces]

        # TODO: split up into batches of 1000
        # if len(to_get) >= 1000:
        #     to_get = to_get[1:1000]

        print('getting objects...')
        narrative_objects = object_cache.get(to_get)
        print('done')

        now = time.time()
        stats.append(['narrative_objects', now - then])
        then = now

        # APPS
        # Gather all apps in this narrative, 
        # Get the apps
        # Profile a map of apps for a given tag

        print('parsing apps...')
        (narrative_apps, narrative_cell_types, elapsed) = self.parse_apps(narrative_objects)
        print('...done')

        stats.append(['app_gets', elapsed])

        now = time.time()
        stats.append(['parse_apps', now - then])
        then = now

        # TODO: permissions, user profiles for permissions, apps

        print('assembling...')
        # Now weave together the sources into a single narratiive
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

        now = time.time()
        stats.append(['finalize', now - then])
        then = now
        result = {
            'narratives': narratives,
            'profiles': profiles
        }
        return result, stats

    def create_narrative(self, name=None, title=None):
        url=self.config['services']['ServiceWizard']
        narrative_service = DynamicServiceClient(url=url,
                                                 module='NarrativeService',
                                                 token=self.token) 
        try:
            [result], error = narrative_service.call_func('create_new_narrative', [{
                'title': title
            }])
            ws = result['workspaceInfo']
            obj = result['narrativeInfo']
            if error:
                return None, error
            is_narratorial = True if ws['metadata'].get('narratorial') == '1' else False
            is_public = ws['globalread'] == 'r'
            mod_date_ms = ServiceUtils.iso8601ToMillisSinceEpoch(ws['moddate'])
            narrative = {
                    'workspaceId': ws['id'],
                    'objectId': obj['id'],
                    'objectVersion': obj['version'],
                    'owner': ws['owner'],
                    'permission': ws['user_permission'],
                    'isPublic': is_public,
                    'isNarratorial': is_narratorial,
                    'title': ws['metadata']['narrative_nice_name'],
                    'modifiedTime': ws['modDateMs'],
                    'savedTime': obj['saveDateMs'],
                    'savedBy': obj['saved_by'],
                    'permissions': None,
                    'cellTypes': None,
                    'apps': None
                }
            return narrative, None
        except Exception as err:
            return None, err.message

        # Now if the title was provided, set that and save it.
        # Otherwise just set the basic metadata.



    def delete_narrative(self, obji=None):
        if (obji is None):
            raise ValueError('"wsi" is required')

        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )

        wsi = WorkspaceIdentity(id=obji.workspace_id())
        rpc.call_func('delete_workspace', [wsi.make_wsi()])
 
        permissions_cache = PermissionsCache(
            workspace_url=self.config['services']['Workspace'],
            path=self.config['caches']['workspace']['path'],
            username=self.username,  # just use the token for now...
            token=self.token
        )
        # permissions_cache.remove(wsi)

        # TODO:
        object_cache = ObjectCache(
            workspace_url=self.config['services']['Workspace'],
            path=self.config['caches']['object']['path'],
            token=self.token
        )
        # object_cache.remove(obji)

        pass

    def share_narrative(self, wsi=None, users=None, permission=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')
        if (users is None):
            raise ValueError('"users" is required')
        if (permission is None):
            raise ValueError('"permission" is required')                        

        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )

        rpc.call_func('set_permissions', [{
            'workspace': wsi.workspace(),
            'id': wsi.id(),
            'new_permission': permission,
            'users': users
        }])

        # Then ensure that the cache for this workspace is
        # refreshed.
        workspace_cache = PermissionsCache(
            workspace_url=self.config['services']['Workspace'],
            path=self.config['caches']['workspace']['path'],
            username=self.username,  # just use the token for now...
            token=self.token
        )
        # workspace_cache.start() 
        workspace_cache.refresh_items([wsi.id()])
        pass

    def unshare_narrative(self, wsi=None, users=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')
        if (users is None):
            raise ValueError('"users" is required')

        # First do the actual unsharing in the workspace.
        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )
        rpc.call_func('set_permissions', [{
            'id': wsi.id(),
            'new_permission': 'n',
            'users': users
        }])

        # Then ensure that the cache for this workspace is
        # refreshed.
        workspace_cache = PermissionsCache(
            workspace_url=self.config['services']['Workspace'],
            path=self.config['caches']['workspace']['path'],
            username=self.username,  # just use the token for now...
            token=self.token
        )
        workspace_cache.refresh_items([wsi.id()])

        pass

    def share_narrative_global(self, wsi=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')

        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )

        rpc.call_func('set_global_permission', [{
            'workspace': wsi.workspace(),
            'id': wsi.id(),
            'new_permission': 'r',
        }])

        # Note: the global permissions are on the workspace info, which is
        # fetched fresh for every narrative listing, so nothing to uncache.

        pass

    def unshare_narrative_global(self, wsi=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')

        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )

        rpc.call_func('set_global_permission', [{
            'id': wsi.id(),
            'new_permission': 'n',
        }])

        # Note: the global permissions are on the workspace info, which is
        # fetched fresh for every narrative listing, so nothing to uncache.

        pass
