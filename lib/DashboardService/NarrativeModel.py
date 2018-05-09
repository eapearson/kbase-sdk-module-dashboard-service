import time
import itertools
from DashboardService.GenericClient import GenericClient
from DashboardService.ServiceUtils import ServiceUtils
from DashboardService.cache.UserProfileCache import UserProfileCache
from DashboardService.cache.AppCache import AppCache
from DashboardService.cache.ObjectCache import ObjectCache
from DashboardService.cache.WorkspaceCache import WorkspaceCache


class WorkspaceIdentity(object):
    def __init__(self, workspace=None, id=None):
        if (workspace is None):
            if (id is None):
                raise ValueError('either "workspace" or "id" are required')   
        elif (id is not None):
            raise ValueError('only one of "workspace" or "id" may be provided')
        self.workspace_name = workspace
        self.workspace_id = id

    def make_wsi(self):
        return {
            'workspace': self.workspace_name,
            'id': self.workspace_id
        }

    def workspace(self):
        return self.workspace_name

    def id(self):
        return self.workspace_id


class NarrativeModel(object):
    def __init__(self, config=None, token=None):
        self.config = config
        self.token = token
        self.narrative_workspaces = None
        self.app_cache = AppCache(
            url=self.config['services']['NarrativeMethodStore'],
            path=self.config['caches']['app']['path']
        )
        self.app_cache.start()
        # self.user_profiles = UserProfileCache(url=self.config['services']['UserProfile'])

    def fetch_narrative_workspaces(self):
        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )
        result, error = rpc.call_func('list_workspace_info', [
             {'meta': {'is_temporary': 'false'}}
        ])
        if error:
            raise ValueError(error)
        ws_list = result[0]

        # This will filter out invalid narratives - we've already filter for
        # "probably valid narrative workspace" above.
        # This gives us a list of workspace info but transformed to a
        # dictionary.
        self.narrative_workspaces = list(
            map(
                lambda nar_ws: ServiceUtils.workspaceInfoToObject(nar_ws),
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
                for key in obj_info['metadata'].keys():
                    key_parts = key.split('.')
                    if key_parts[0] == 'method' or key_parts[0] == 'app':
                        parsed_id = ServiceUtils.parse_app_key(key_parts[1])

                        app = {
                            # 'key': key_parts[1],
                            'id': parsed_id,
                            'count': int(obj_info['metadata'][key]),
                            'obsolete': True
                        }

                    if key_parts[0] == 'method':
                        parsed_id = ServiceUtils.parse_app_key(key_parts[1])

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

            narrative_apps.append(apps)
            narrative_cell_types.append(cell_types)
        return narrative_apps, narrative_cell_types, query_time

    def list_all_narratives(self):
        # current_username = ctx['user_id']
        stats = []
        then = time.time()

        # WORKSPACES
        narrative_workspaces = self.fetch_narrative_workspaces()
        now = time.time()
        stats.append(['list_workspace', now - then])
        then = now

        # PERMISSION
       
        workspace_cache = WorkspaceCache(
            url=self.config['services']['Workspace'],
            path=self.config['caches']['workspace']['path'],
            token=self.token
        )
        workspace_cache.start()
        # workspace_ids = [ws['id'] for ws in narrative_workspaces]
        narrative_workspaces_perms = workspace_cache.get(narrative_workspaces)
        now = time.time()
        stats.append(['get_permissions', now - then])
        then = now

        # PROFILE PER USER
        # Get all profiles for all users in the permissions list. It is returned with the
        # response so that the caller can map usernames to profiles.
        users = set()
        for perms in narrative_workspaces_perms:
            for perm in perms:
                users.add(perm['username'])

        # We end up with a map of username -> profile
        # Transform profiles into map of user to record.
        # The profile record itself is simplified down to just what
        # we need
        profiles_cache = UserProfileCache(
            url=self.config['services']['UserProfile'],
            path=self.config['caches']['userprofile']['path'])
        profiles_cache.start()
        profiles = profiles_cache.get(list(users))
        profiles_cache.stop()
        profiles_map = dict()
        for (username, profile) in itertools.izip(users, profiles):
            profiles_map[username] = profile

        now = time.time()
        stats.append(['user_profiles', now - then])
        then = now

        # NARRATIVE OBJECT
        # based on the WS lookup table, lookup the narratives
        # narrative_objects, _missing, _missed = self.objectInfo.get_object_info_for_workspaces(
        #     narrative_workspaces, clients['Workspace'])
        object_cache = ObjectCache(
            url=self.config['services']['Workspace'],
            path=self.config['caches']['object']['path'],
            token=self.token
        )
        object_cache.start()

        # object_cache = object_cache.newInstance(token=ctx['token'])
        # convert to the cache format, which includes the mod date as timestamp
        # NB: includes object id, because the key should have enough info to fetch
        # the object from storage as well as form a unique key
        to_get = [(ws['id'],
                  int(ws['metadata']['narrative']),
                  ws['modDateMs']) for ws in narrative_workspaces]
        narrative_objects = object_cache.get(to_get)

        now = time.time()
        stats.append(['narrative_objects', now - then])
        then = now

        # APPS
        # Gather all apps in this narrative, 
        # Get the apps
        # Profile a map of apps for a given tag

        (narrative_apps, narrative_cell_types, elapsed) = self.parse_apps(narrative_objects)

        stats.append(['app_gets', elapsed])

        now = time.time()
        stats.append(['parse_apps', now - then])
        then = now

        # TODO: permissions, user profiles for permissions, apps

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
            'profiles': profiles_map,
            # 'debug': {
            #     'workspaces': narrative_workspaces,
            #     'objects': narrative_objects,
            #     'toget': to_get,
            #     'perms': narrative_workspaces_perms,
            #     'celltypes': narrative_cell_types,
            #     'apps': narrative_apps
            # }
        }
        return result, stats

    def delete_narrative(self, wsi=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')

        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )

        rpc.call_func('delete_workspace', [wsi.make_wsi()])
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
        pass

    def unshare_narrative(self, wsi=None, users=None):
        if (wsi is None):
            raise ValueError('"wsi" is required')
        if (users is None):
            raise ValueError('"users" is required')

        rpc = GenericClient(
            module='Workspace',
            url=self.config['services']['Workspace'],
            token=self.token
        )

        rpc.call_func('set_permissions', [{
            'workspace': wsi.workspace(),
            'id': wsi.id(),
            'new_permission': 'n',
            'users': users
        }])
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
            'workspace': wsi.workspace(),
            'id': wsi.id(),
            'new_permission': 'n',
        }])
        pass
