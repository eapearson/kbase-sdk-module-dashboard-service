# -*- coding: utf-8 -*-
#BEGIN_HEADER
from time import time
from DashboardService.NarrativeManager import NarrativeManager
from DashboardService.DynamicServiceCache import DynamicServiceCache
from DashboardService.cache.AppCache import AppCache
from DashboardService.cache.UserProfileCache import UserProfileCache
from DashboardService.cache.ObjectCache import ObjectCache
from DashboardService.NarrativeModel import NarrativeModel, WorkspaceIdentity
#END_HEADER


class DashboardService:
    '''
    Module Name:
    DashboardService

    Module Description:
    A KBase module: DashboardService
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.8"
    GIT_URL = "git@github.com:eapearson/kbase-sdk-module-dashboard-service.git"
    GIT_COMMIT_HASH = "1421396836789af110526793ab28a17297b87ddc"

    #BEGIN_CLASS_HEADER
    def _nm(self, ctx):
        return NarrativeManager(self.config, ctx, self.setAPICache, self.dataPaletteCache)
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config

        self.cache_directory = config['cache-directory']
        self.workspaceURL = config['workspace-url']
        self.serviceWizardURL = config['service-wizard']
        self.setAPICache = DynamicServiceCache(self.serviceWizardURL,
                                               config['setapi-version'],
                                               'SetAPI')
        self.dataPaletteCache = DynamicServiceCache(self.serviceWizardURL,
                                                    config['datapaletteservice-version'],
                                                    'DataPaletteService')

        user_profile_cache = UserProfileCache(
            path=self.cache_directory + '/user_profile_cache.db',
            url=config['user-profile-service-url'])
        user_profile_cache.initialize()

        # The app cache can be populated upon load.
        app_cache = AppCache(
            path=self.cache_directory + '/app_cache.db',
            url=config['narrative-method-store-url']
        )
        app_cache.initialize()

        object_cache = ObjectCache(
            path=self.cache_directory + '/object_cache.db',
            url=config['workspace-url']
        )
        object_cache.initialize()
        #END_CONSTRUCTOR
        pass


    def list_all_narratives(self, ctx, params):
        """
        :param params: instance of type "ListAllNarrativesParams" ->
           structure:
        :returns: multiple set - (1) parameter "result" of type
           "ListAllNarrativesResult" -> structure: parameter "narratives" of
           list of type "NarrativeX" -> structure: parameter "ws" of type
           "workspace_info" (Information about a workspace. ws_id id - the
           numerical ID of the workspace. ws_name workspace - name of the
           workspace. username owner - name of the user who owns (e.g.
           created) this workspace. timestamp moddate - date when the
           workspace was last modified. int max_objid - the maximum object ID
           appearing in this workspace. Since cloning a workspace preserves
           object IDs, this number may be greater than the number of objects
           in a newly cloned workspace. permission user_permission -
           permissions for the authenticated user of this workspace.
           permission globalread - whether this workspace is globally
           readable. lock_status lockstat - the status of the workspace lock.
           usermeta metadata - arbitrary user-supplied metadata about the
           workspace.) -> tuple of size 9: parameter "id" of Long, parameter
           "workspace" of String, parameter "owner" of String, parameter
           "moddate" of String, parameter "max_objid" of Long, parameter
           "user_permission" of String, parameter "globalread" of String,
           parameter "lockstat" of String, parameter "metadata" of mapping
           from String to String, parameter "nar" of type "object_info"
           (Information about an object, including user provided metadata.
           obj_id objid - the numerical id of the object. obj_name name - the
           name of the object. type_string type - the type of the object.
           timestamp save_date - the save date of the object. obj_ver ver -
           the version of the object. username saved_by - the user that saved
           or copied the object. ws_id wsid - the workspace containing the
           object. ws_name workspace - the workspace containing the object.
           string chsum - the md5 checksum of the object. int size - the size
           of the object in bytes. usermeta meta - arbitrary user-supplied
           metadata about the object.) -> tuple of size 11: parameter "objid"
           of Long, parameter "name" of String, parameter "type" of String,
           parameter "save_date" of type "timestamp" (A time in the format
           YYYY-MM-DDThh:mm:ssZ, where Z is either the character Z
           (representing the UTC timezone) or the difference in time to UTC
           in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500 (EST time)
           2013-04-03T08:56:32+0000 (UTC time) 2013-04-03T08:56:32Z (UTC
           time)), parameter "version" of Long, parameter "saved_by" of
           String, parameter "wsid" of Long, parameter "workspace" of String,
           parameter "chsum" of String, parameter "size" of Long, parameter
           "meta" of mapping from String to String, parameter "permissions"
           of list of type "UserPermission" -> structure: parameter
           "username" of String, parameter "permission" of type "permission"
           (Represents the permissions a user or users have to a workspace:
           'a' - administrator. All operations allowed. 'w' - read/write. 'r'
           - read. 'n' - no permissions.), parameter "profiles" of list of
           type "UserProfile" (LIST ALL NARRATIVES) -> unspecified object,
           (2) parameter "stats" of type "RunStats" -> structure: parameter
           "timings" of list of tuple of size 2: String, Long
        """
        # ctx is the context object
        # return variables are: result, stats
        #BEGIN list_all_narratives
        start = time()

        # The narrative model implements the interface to the services and any caching
        # mechanisms. Here we just need to pass it whatever it needs from here...
        #  model = self.make_model(token=ctx['token'])
        model = NarrativeModel(
            config={
                'services': {
                    'Workspace': self.config['workspace-url'],
                    'NarrativeMethodStore': self.config['narrative-method-store-url'],
                    'UserProfile': self.config['user-profile-service-url']
                },
                'caches': {
                    'object': {
                        'path': self.cache_directory + '/object_cache.db'
                    },
                    'userprofile': {
                        'path': self.cache_directory + '/user_profile_cache.db'
                    },
                    'app': {
                        'path': self.cache_directory + '/app_cache.db'
                    }
                }
            },
            token=ctx['token']
        )

        # ws = Workspace(self.workspaceURL, token=ctx["token"])

        # # NB use the module name as the key for the clients.
        # clients = {
        #     'Workspace': ws
        # }
        
        result, timings = model.list_all_narratives()
        end = time()
        timings.append(['total', end - start])
        stats = {
            'timings': timings
        }
        #END list_all_narratives

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method list_all_narratives return value ' +
                             'result is not type dict as required.')
        if not isinstance(stats, dict):
            raise ValueError('Method list_all_narratives return value ' +
                             'stats is not type dict as required.')
        # return the results
        return [result, stats]

    def delete_narrative(self, ctx, params):
        """
        :param params: instance of type "DeleteNarrativeParams" -> structure:
           parameter "wsi" of type "WorkspaceIdentity" -> structure:
           parameter "workspace" of type "ws_name", parameter "id" of type
           "ws_id" (from workspace_deluxe Note too that naming conventions
           for paramters using these types (may) also use the
           workspace_deluxe conventions.)
        """
        # ctx is the context object
        #BEGIN delete_narrative
        if 'wsi' not in params:
            raise ValueError('"wsi" field, identifying the narrative workspace, required')

        model = NarrativeModel(
            config={
                'services': {
                    'Workspace': self.config['workspace-url'],
                    'NarrativeMethodStore': self.config['narrative-method-store-url'],
                    'UserProfile': self.config['user-profile-service-url']
                },
                'caches': {
                    'object': {
                        'path': './work/object_cache.db'
                    },
                    'userprofile': {
                        'path': './work/user_profile_cache.db'
                    },
                    'app': {
                        'path': './work/app_cache.db'
                    }
                }
            },
            token=ctx['token']
        )

        wsi = WorkspaceIdentity(workspace=params['wsi'].get('workspace'),
                                id=params['wsi'].get('id'))

        model.delete_narrative(wsi=wsi)
        #END delete_narrative
        pass

    def share_narrative(self, ctx, params):
        """
        :param params: instance of type "ShareNarrativeParams" -> structure:
           parameter "wsi" of type "WorkspaceIdentity" -> structure:
           parameter "workspace" of type "ws_name", parameter "id" of type
           "ws_id" (from workspace_deluxe Note too that naming conventions
           for paramters using these types (may) also use the
           workspace_deluxe conventions.), parameter "users" of list of type
           "username", parameter "permission" of type "permission"
           (Represents the permissions a user or users have to a workspace:
           'a' - administrator. All operations allowed. 'w' - read/write. 'r'
           - read. 'n' - no permissions.)
        """
        # ctx is the context object
        #BEGIN share_narrative
        if 'wsi' not in params:
            raise ValueError('"wsi" field, identifying the narrative workspace, ' +
                             'is required but was not provided')

        wsi = WorkspaceIdentity(workspace=params['wsi'].get('workspace'),
                                id=params['wsi'].get('id'))

        if 'users' not in params:
            raise ValueError('"users" field, a list of usernames with whom to share, ' +
                             'is required but was not provided')
        users = params['users']

        if 'permission' not in params:
            raise ValueError('"permission" field, the permission to give the users, ' +
                             'is required but was not provided')
        permission = params['permission']

        model = NarrativeModel(
            config={
                'services': {
                    'Workspace': self.config['workspace-url'],
                    'NarrativeMethodStore': self.config['narrative-method-store-url'],
                    'UserProfile': self.config['user-profile-service-url']
                },
                'caches': {
                    'object': {
                        'path': './work/object_cache.db'
                    },
                    'userprofile': {
                        'path': './work/user_profile_cache.db'
                    },
                    'app': {
                        'path': './work/app_cache.db'
                    }
                }
            },
            token=ctx['token']
        )

        model.share_narrative(wsi=wsi, users=users, permission=permission)
        #END share_narrative
        pass

    def unshare_narrative(self, ctx, params):
        """
        :param params: instance of type "UnshareNarrativeParams" ->
           structure: parameter "wsi" of type "WorkspaceIdentity" ->
           structure: parameter "workspace" of type "ws_name", parameter "id"
           of type "ws_id" (from workspace_deluxe Note too that naming
           conventions for paramters using these types (may) also use the
           workspace_deluxe conventions.), parameter "users" of list of type
           "username"
        """
        # ctx is the context object
        #BEGIN unshare_narrative
        if 'wsi' not in params:
            raise ValueError('"wsi" field, identifying the narrative workspace, ' +
                             'is required but was not provided')

        wsi = WorkspaceIdentity(workspace=params['wsi'].get('workspace'),
                                id=params['wsi'].get('id'))

        if 'users' not in params:
            raise ValueError('"users" field, a list of usernames with whom to share, ' +
                             'is required but was not provided')
        users = params['users']

        model = NarrativeModel(
            config={
                'services': {
                    'Workspace': self.config['workspace-url'],
                    'NarrativeMethodStore': self.config['narrative-method-store-url'],
                    'UserProfile': self.config['user-profile-service-url']
                },
                'caches': {
                    'object': {
                        'path': './work/object_cache.db'
                    },
                    'userprofile': {
                        'path': './work/user_profile_cache.db'
                    },
                    'app': {
                        'path': './work/app_cache.db'
                    }
                }
            },
            token=ctx['token']
        )

        model.unshare_narrative(wsi=wsi, users=users)
        #END unshare_narrative
        pass

    def share_narrative_global(self, ctx, params):
        """
        :param params: instance of type "ShareNarrativeGlobalParams" ->
           structure: parameter "wsi" of type "WorkspaceIdentity" ->
           structure: parameter "workspace" of type "ws_name", parameter "id"
           of type "ws_id" (from workspace_deluxe Note too that naming
           conventions for paramters using these types (may) also use the
           workspace_deluxe conventions.)
        """
        # ctx is the context object
        #BEGIN share_narrative_global
        if 'wsi' not in params:
            raise ValueError('"wsi" field, identifying the narrative workspace, ' +
                             'is required but was not provided')

        wsi = WorkspaceIdentity(workspace=params['wsi'].get('workspace'),
                                id=params['wsi'].get('id'))

        model = NarrativeModel(
            config={
                'services': {
                    'Workspace': self.config['workspace-url'],
                    'NarrativeMethodStore': self.config['narrative-method-store-url'],
                    'UserProfile': self.config['user-profile-service-url']
                },
                'caches': {
                    'object': {
                        'path': './work/object_cache.db'
                    },
                    'userprofile': {
                        'path': './work/user_profile_cache.db'
                    },
                    'app': {
                        'path': './work/app_cache.db'
                    }
                }
            },
            token=ctx['token']
        )

        model.share_narrative_global(wsi=wsi)
        #END share_narrative_global
        pass

    def unshare_narrative_global(self, ctx, params):
        """
        :param params: instance of type "UnshareNarrativeGlobalParams" ->
           structure: parameter "wsi" of type "WorkspaceIdentity" ->
           structure: parameter "workspace" of type "ws_name", parameter "id"
           of type "ws_id" (from workspace_deluxe Note too that naming
           conventions for paramters using these types (may) also use the
           workspace_deluxe conventions.)
        """
        # ctx is the context object
        #BEGIN unshare_narrative_global
        if 'wsi' not in params:
            raise ValueError('"wsi" field, identifying the narrative workspace, ' +
                             'is required but was not provided')

        wsi = WorkspaceIdentity(workspace=params['wsi'].get('workspace'),
                                id=params['wsi'].get('id'))

        model = NarrativeModel(
            config={
                'services': {
                    'Workspace': self.config['workspace-url'],
                    'NarrativeMethodStore': self.config['narrative-method-store-url'],
                    'UserProfile': self.config['user-profile-service-url']
                },
                'caches': {
                    'object': {
                        'path': './work/object_cache.db'
                    },
                    'userprofile': {
                        'path': './work/user_profile_cache.db'
                    },
                    'app': {
                        'path': './work/app_cache.db'
                    }
                }
            },
            token=ctx['token']
        )   

        model.unshare_narrative_global(wsi=wsi)
        #END unshare_narrative_global
        pass
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
