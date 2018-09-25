# -*- coding: utf-8 -*-
#BEGIN_HEADER
from time import time
import apsw

from DashboardService.DynamicServiceClient import DynamicServiceClient
from DashboardService.cache.AppCache import AppCache
from DashboardService.cache.UserProfileCache import UserProfileCache
from DashboardService.cache.ObjectCache import ObjectCache
from DashboardService.cache.PermissionsCache import PermissionsCache
from DashboardService.Model import Model, WorkspaceIdentity, ObjectIdentity
from DashboardService.Validation import Validation
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
    VERSION = "0.1.0"
    GIT_URL = "ssh://git@github.com/eapearson/kbase-sdk-module-dashboard-service"
    GIT_COMMIT_HASH = "3a463c90289c412485f65bb806a58a0bc817da0d"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config

        config, err = Validation.validate_config(config)
        if err:
            raise ValueError(err)

        self.call_config = config

        def setwal(db):
            db.cursor().execute("pragma journal_mode=wal")
            # custom auto checkpoint interval (use zero to disable)
            db.wal_autocheckpoint(0)

        apsw.connection_hooks.append(setwal)


        # TODO: move into Model?

        user_profile_cache = UserProfileCache(
            path=config['caches']['userprofile']['path'],
            user_profile_url=config['services']['UserProfile'])
        user_profile_cache.initialize()

        # The app cache can be populated upon load.
        app_cache = AppCache(
            path=config['caches']['app']['path'],
            narrative_method_store_url=config['services']['NarrativeMethodStore']
        )
        app_cache.initialize()

        object_cache = ObjectCache(
            path=config['caches']['object']['path'],
            workspace_url=config['services']['Workspace']
        )
        object_cache.initialize()

        workspace_cache = PermissionsCache(
            path=config['caches']['workspace']['path'],
            workspace_url=config['services']['Workspace']
        )
        workspace_cache.initialize()

        #END_CONSTRUCTOR
        pass


    def list_all_narratives(self, ctx, params):
        """
        :param params: instance of type "ListAllNarrativesParams" ->
           structure: parameter "just_modified_after" of type "timestamp" (A
           time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
           character Z (representing the UTC timezone) or the difference in
           time to UTC in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500
           (EST time) 2013-04-03T08:56:32+0000 (UTC time)
           2013-04-03T08:56:32Z (UTC time))
        :returns: multiple set - (1) parameter "result" of type
           "ListAllNarrativesResult" (typedef structure { workspace_info
           workspace; object_info object; list<UserPermission> permissions; }
           NarrativeX;) -> structure: parameter "narratives" of list of type
           "Narrative" -> structure: parameter "objectId" of type "obj_id",
           parameter "objectVersion" of type "obj_ver", parameter "owner" of
           String, parameter "permission" of String, parameter "isPublic" of
           type "boolean" (@range [0,1]), parameter "isNarratorial" of type
           "boolean" (@range [0,1]), parameter "title" of String, parameter
           "savedTime" of Long, parameter "savedBy" of String, parameter
           "permissions" of list of type "UserPermission" -> structure:
           parameter "username" of type "Username", parameter "permission" of
           type "permission" (Represents the permissions a user or users have
           to a workspace: 'a' - administrator. All operations allowed. 'w' -
           read/write. 'r' - read. 'n' - no permissions.), parameter
           "cellTypes" of list of type "NarrativeCellStat" (typedef
           UnspecifiedObject NarrativePermission;) -> unspecified object,
           parameter "apps" of list of type "NarrativeApp" -> structure:
           parameter "id" of String, parameter "count" of Long, parameter
           "profiles" of mapping from type "Username" to type "UserProfile"
           (LIST ALL NARRATIVES) -> unspecified object, parameter "apps" of
           mapping from type "AppID" (Just the subset of info that the front
           end will use) to type "App" -> structure: parameter "id" of type
           "AppID" (Just the subset of info that the front end will use),
           parameter "notFound" of type "boolean" (@range [0,1]), parameter
           "title" of String, parameter "subtitle" of String, parameter
           "iconURL" of String, (2) parameter "error" of type "Error" ->
           structure: parameter "message" of String, parameter "type" of
           String, parameter "code" of String, parameter "info" of
           unspecified object, (3) parameter "stats" of type "RunStats" ->
           structure: parameter "timings" of list of tuple of size 2: String,
           Long
        """
        # ctx is the context object
        # return variables are: result, error, stats
        #BEGIN list_all_narratives
        params, err = Validation.validate_list_all_narratives(ctx, params)
        if err:
            return None, err, None

        start = time()

        # The narrative model implements the interface to the services and any caching
        # mechanisms. Here we just need to pass it whatever it needs from here...
        #  model = self.make_model(token=ctx['token'])
        model = Model(
            token=ctx['token'],
            username=ctx['user_id'],
            config=self.call_config,
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
        return [result, None, stats]
        #END list_all_narratives

        # # At some point might do deeper type checking...
        # if not isinstance(result, dict):
        #     raise ValueError('Method list_all_narratives return value ' +
        #                      'result is not type dict as required.')
        # if not isinstance(error, dict):
        #     raise ValueError('Method list_all_narratives return value ' +
        #                      'error is not type dict as required.')
        # if not isinstance(stats, dict):
        #     raise ValueError('Method list_all_narratives return value ' +
        #                      'stats is not type dict as required.')
        # # return the results
        # return [result, error, stats]

    def create_narrative(self, ctx, param):
        """
        :param param: instance of type "CreateNarrativeParam" (Create
           Narrative) -> structure: parameter "title" of String, parameter
           "name" of type "ws_name"
        :returns: multiple set - (1) parameter "result" of type
           "CreateNarrativeResult" -> structure: parameter "narrative" of
           type "Narrative" -> structure: parameter "objectId" of type
           "obj_id", parameter "objectVersion" of type "obj_ver", parameter
           "owner" of String, parameter "permission" of String, parameter
           "isPublic" of type "boolean" (@range [0,1]), parameter
           "isNarratorial" of type "boolean" (@range [0,1]), parameter
           "title" of String, parameter "savedTime" of Long, parameter
           "savedBy" of String, parameter "permissions" of list of type
           "UserPermission" -> structure: parameter "username" of type
           "Username", parameter "permission" of type "permission"
           (Represents the permissions a user or users have to a workspace:
           'a' - administrator. All operations allowed. 'w' - read/write. 'r'
           - read. 'n' - no permissions.), parameter "cellTypes" of list of
           type "NarrativeCellStat" (typedef UnspecifiedObject
           NarrativePermission;) -> unspecified object, parameter "apps" of
           list of type "NarrativeApp" -> structure: parameter "id" of
           String, parameter "count" of Long, (2) parameter "error" of type
           "Error" -> structure: parameter "message" of String, parameter
           "type" of String, parameter "code" of String, parameter "info" of
           unspecified object
        """
        # ctx is the context object
        # return variables are: result, error
        #BEGIN create_narrative
        param, err = Validation.validate_create_narrative(ctx, param)
        if err:
            return None, err

        model = Model(
            config=self.call_config,
            token=ctx['token'],
            username=ctx['user_id']
        )

        # obji = ObjectIdentity(workspace_id=params['obji'].get('workspace_id'),
        #                       object_id=params['obji'].get('object_id'))

        result, err2 = model.create_narrative(name=param['name'], title=param['title'])
        return [{
            'narrative': result
        }, err2]
        #END create_narrative

        # At some point might do deeper type checking...
        # if not isinstance(result, dict):
        #     raise ValueError('Method create_narrative return value ' +
        #                      'result is not type dict as required.')
        # if not isinstance(error, dict):
        #     raise ValueError('Method create_narrative return value ' +
        #                      'error is not type dict as required.')
        # # return the results
        # return [result, error]

    def delete_narrative(self, ctx, params):
        """
        :param params: instance of type "DeleteNarrativeParams" (Delete
           Narrative) -> structure: parameter "obji" of type "ObjectIdentity"
           -> structure: parameter "workspace_id" of type "ws_id" (from
           workspace_deluxe Note too that naming conventions for parameters
           using these types (may) also use the workspace_deluxe conventions.
           workspace), parameter "object_id" of type "obj_id", parameter
           "version" of type "obj_ver"
        :returns: instance of type "Error" -> structure: parameter "message"
           of String, parameter "type" of String, parameter "code" of String,
           parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: error
        #BEGIN delete_narrative
        params, err = Validation.validate_delete_narrative(ctx, params)
        if err:
            return None, err

        # if 'obji' not in params:
        #     raise ValueError('"wsi" field, identifying the narrative workspace, required')

        model = Model(
            config=self.call_config,
            token=ctx['token']
        )

        obji = ObjectIdentity(workspace_id=params['obji'].get('workspace_id'),
                              object_id=params['obji'].get('object_id'))

        model.delete_narrative(obji=obji)

        return [None]
        #END delete_narrative

        # # At some point might do deeper type checking...
        # if not isinstance(error, dict):
        #     raise ValueError('Method delete_narrative return value ' +
        #                      'error is not type dict as required.')
        # # return the results
        # return [error]

    def share_narrative(self, ctx, params):
        """
        :param params: instance of type "ShareNarrativeParams" (Share
           Narrative) -> structure: parameter "wsi" of type
           "WorkspaceIdentity" -> structure: parameter "workspace" of type
           "ws_name", parameter "id" of type "ws_id" (from workspace_deluxe
           Note too that naming conventions for parameters using these types
           (may) also use the workspace_deluxe conventions. workspace),
           parameter "users" of list of type "Username", parameter
           "permission" of type "permission" (Represents the permissions a
           user or users have to a workspace: 'a' - administrator. All
           operations allowed. 'w' - read/write. 'r' - read. 'n' - no
           permissions.)
        :returns: instance of type "Error" -> structure: parameter "message"
           of String, parameter "type" of String, parameter "code" of String,
           parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: error
        #BEGIN share_narrative
        params, err = Validation.validate_share_narrative(ctx, params)
        if err:
            return [err]

        wsi = WorkspaceIdentity(id=params['wsi'].get('id'))

        model = Model(
            config=self.call_config,
            token=ctx['token'],
            username=ctx['user_id']
        )

        model.share_narrative(wsi=wsi, users=params['users'], permission=params['permission'])
        return [None]
        #END share_narrative

        # # At some point might do deeper type checking...
        # if not isinstance(error, dict):
        #     raise ValueError('Method share_narrative return value ' +
        #                      'error is not type dict as required.')
        # # return the results
        # return [error]

    def unshare_narrative(self, ctx, params):
        """
        :param params: instance of type "UnshareNarrativeParams" ->
           structure: parameter "wsi" of type "WorkspaceIdentity" ->
           structure: parameter "workspace" of type "ws_name", parameter "id"
           of type "ws_id" (from workspace_deluxe Note too that naming
           conventions for parameters using these types (may) also use the
           workspace_deluxe conventions. workspace), parameter "users" of
           list of type "Username"
        :returns: instance of type "Error" -> structure: parameter "message"
           of String, parameter "type" of String, parameter "code" of String,
           parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: error
        #BEGIN unshare_narrative
        params, err = Validation.validate_unshare_narrative(ctx, params)
        if err:
            return [err]

        wsi = WorkspaceIdentity(id=params['wsi'].get('id'))
        users = params['users']

        # if 'timestamp' not in params:
        #     raise ValueError('"timestamp" field, the laste modified timestamp for '+
        #                      'the narrative, is required but was not provided')

        model = Model(
            config=self.call_config,
            token=ctx['token'],
            username=ctx['user_id']
        )

        model.unshare_narrative(wsi=wsi, users=users)
        return [None]
        #END unshare_narrative

        # # At some point might do deeper type checking...
        # if not isinstance(error, dict):
        #     raise ValueError('Method unshare_narrative return value ' +
        #                      'error is not type dict as required.')
        # # return the results
        # return [error]

    def share_narrative_global(self, ctx, params):
        """
        :param params: instance of type "ShareNarrativeGlobalParams" ->
           structure: parameter "wsi" of type "WorkspaceIdentity" ->
           structure: parameter "workspace" of type "ws_name", parameter "id"
           of type "ws_id" (from workspace_deluxe Note too that naming
           conventions for parameters using these types (may) also use the
           workspace_deluxe conventions. workspace)
        :returns: instance of type "Error" -> structure: parameter "message"
           of String, parameter "type" of String, parameter "code" of String,
           parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: error
        #BEGIN share_narrative_global
        if 'wsi' not in params:
            raise ValueError('"wsi" field, identifying the narrative workspace, ' +
                             'is required but was not provided')

        wsi = WorkspaceIdentity(id=params['wsi'].get('id'))

        model = Model(
            config=self.call_config,
            token=ctx['token']
        )

        model.share_narrative_global(wsi=wsi)
        #END share_narrative_global

        # # At some point might do deeper type checking...
        # if not isinstance(error, dict):
        #     raise ValueError('Method share_narrative_global return value ' +
        #                      'error is not type dict as required.')
        # # return the results
        # return [error]

    def unshare_narrative_global(self, ctx, params):
        """
        :param params: instance of type "UnshareNarrativeGlobalParams" ->
           structure: parameter "wsi" of type "WorkspaceIdentity" ->
           structure: parameter "workspace" of type "ws_name", parameter "id"
           of type "ws_id" (from workspace_deluxe Note too that naming
           conventions for parameters using these types (may) also use the
           workspace_deluxe conventions. workspace)
        :returns: instance of type "Error" -> structure: parameter "message"
           of String, parameter "type" of String, parameter "code" of String,
           parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: error
        #BEGIN unshare_narrative_global
        params, error = Validation.validate_unshare_narrative_global(ctx, params)
        if error:
            return [error]

        wsi = WorkspaceIdentity(id=params['wsi'].get('id'))
 
        model = Model(
            config=self.call_config,
            token=ctx['token'],
            username=ctx['user_id']
        )

        model.unshare_narrative_global(wsi=wsi)
        return [None]
        #END unshare_narrative_global

        # At some point might do deeper type checking...
        # if not isinstance(error, dict):
        #     raise ValueError('Method unshare_narrative_global return value ' +
        #                      'error is not type dict as required.')
        # # return the results
        # return [error]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
