# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import StringIO

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

# from Workspace.WorkspaceClient import Workspace
# from DashboardService.DashboardServiceImpl import DashboardService
# from DashboardService.DashboardServiceServer import MethodContext
# from DashboardService.Validation import Validation
# from DashboardService.authclient import KBaseAuth as _KBaseAuth
# from DashboardService.ServiceUtils import ServiceUtils
# from DashboardService.GenericClient import GenericClient 
# from DashboardService.DynamicServiceClient import DynamicServiceClient
import DashboardService.Model as Model


class ModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        os.environ['USE_DP'] = "1"
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.NARRATIVE_TYPE = "KBaseNarrative.Narrative-4.0"
        cls.cfg = {}
        config = _ConfigParser()
        config.read(config_file)
        for nameval in config.items('DashboardService'):
            cls.cfg[nameval[0]] = nameval[1]


        # authServiceUrl = cls.cfg.get('auth-service-url',
        #                              'https://kbase.us/services/authorization/Sessions/Login')
        # auth_client = _KBaseAuth(authServiceUrl)
        # user_id = auth_client.get_user(token)
        # # WARNING: don't call any logging methods on the context object,
        # # it'll result in a NoneType error
        # cls.ctx = MethodContext(None)
        # cls.ctx.update({'token': token,
        #                 'user_id': user_id,
        #                 'provenance': [
        #                     {'service': 'DashboardService',
        #                      'method': 'please_never_use_it_in_production',
        #                      'method_params': []
        #                      }],
        #                 'authenticated': 1})
        # cls.wsURL = cls.cfg['workspace-url']
        # cls.serviceWizardURL = cls.cfg['service-wizard']

        # cls.wsClient = Workspace(cls.wsURL, token=token)

        # cls.serviceImpl = DashboardService(cls.cfg)

        # Second user
        test_cfg_file = '/kb/module/work/test.cfg'
        test_cfg_text = "[test]\n"
        with open(test_cfg_file, "r") as f:
            test_cfg_text += f.read()
        config = _ConfigParser()
        config.readfp(StringIO.StringIO(test_cfg_text))
        test_cfg_dict = dict(config.items("test"))

      
        # cls.createdWorkspaces = [];

    # @classmethod
    # def tearDownClass(cls):
    #     for wsName in cls.createdWorkspaces:
    #         try:
    #             cls.wsClient.delete_workspace({'workspace': wsName})
    #             print("Test workspace " + wsName + " was deleted for user" + cls.ctx['user_id'])
    #         except:
    #             print("Error deleting test workspace " + wsName + " was deleted for user" + cls.ctx['user_id'])

    # def getWsClient(self):
    #     return self.__class__.wsClient

    # # def getWsClient2(self):
    # #     return self.__class__.wsClients[1]

    # def createWs(self):
    #     return self.__class__.createWsStatic

    # # def createWs2(self):
    # #     return self.__class__.createWsStatic(1)

    # @classmethod
    # def createWsStatic(cls):
    #     suffix = int(time.time() * 1000)
    #     wsName = "test_DashboardService_" + str(suffix)
    #     cls.wsClient.create_workspace({'workspace': wsName})  # noqa
    #     cls.createdWorkspaces.append(wsName)
    #     return wsName

    # def getImpl(self):
    #     return self.__class__.serviceImpl

    # def getContext(self):
    #     return self.__class__.ctx

    # WorkspaceIdentity
    def test_model_workspace_identity_bad_input(self):
        test_table = [
            {
                'input': {
                    'workspace': None,
                    'id': None
                }
            },
            {
                'input': {
                    'workspace': 'x',
                    'id': 123
                }
            }
        ]
        for test in test_table:
            try:
                Model.WorkspaceIdentity(**test['input'])
                self.assertTrue(False)
            except ValueError as error:
                self.assertTrue(True)

    def test_model_workspace_identity(self):
        test_table = [
            {
                'input': {
                    'workspace': 'workspace_here',
                    'id': None,
                    'timestamp': 'timestamp_here'
                }
            },
            {
                'input': {
                    'workspace': None,
                    'id': 'id_here',
                    'timestamp': 'timestamp_here'
                }
            }
        ]
        for test in test_table:
            input = test['input']
            wsi = Model.WorkspaceIdentity(**input)

            self.assertEquals(wsi.workspace(), input['workspace'])
            self.assertEquals(wsi.name(), input['workspace'])
            self.assertEquals(wsi.id(), input['id'])
            self.assertEquals(wsi.timestamp(), input['timestamp'])

    # ObjectIdentity
    def test_object_identity_bad_input(self):
        test_table = [
            {
                'input': {
                    'workspace_id': None,
                    'object_id': None,
                    'version': None
                }
            },
            {
                'input': {
                    'workspace_id': 123,
                    'object_id': None,
                    'version': None
                }
            },
            {
                'input': {
                    'workspace_id': None,
                    'object_id': 123,
                    'version': None
                }
            }
        ]
        for test in test_table:
            try:
                Model.ObjectIdentity(**test['input'])
                self.assertTrue(False)
            except ValueError as error:
                self.assertTrue(True)

    def test_object_identity(self):
        test_table = [
            {
                'input': {
                    'workspace_id': 123,
                    'object_id': 456,
                    'version': 789
                }
            },
            {
                'input': {
                    'workspace_id': 123,
                    'object_id': 456
                }
            }
        ]
        for test in test_table:
            input = test['input']
            obji = Model.ObjectIdentity(**input)

            self.assertEquals(obji.workspace_id(), input['workspace_id'])
            self.assertEquals(obji.object_id(), input['object_id'])
            if ('version' in input):
                self.assertEquals(obji.version(), input['version'])
