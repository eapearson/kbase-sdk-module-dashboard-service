# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import StringIO

from os import environ
from DashboardService.NarrativeManager import NarrativeManager
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from Workspace.WorkspaceClient import Workspace
from DashboardService.DashboardServiceImpl import DashboardService
from DashboardService.DashboardServiceServer import MethodContext
from SetAPI.SetAPIClient import SetAPI
from DashboardService.WorkspaceListObjectsIterator import WorkspaceListObjectsIterator
from FakeObjectsForTests.FakeObjectsForTestsClient import FakeObjectsForTests
from DataPaletteService.DataPaletteServiceClient import DataPaletteService
from DataPaletteService.authclient import KBaseAuth as _KBaseAuth


def in_list(wsid, nar_list):
    ''' Helper function to determine if ws with ID is returned from the Narrative listing functions '''
    for nt in nar_list:
        if wsid == nt['ws'][0]:
            return True
    return False


class DashboardServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        os.environ['USE_DP'] = "1"
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.NARRATIVE_TYPE = "KBaseNarrative.Narrative-4.0"
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('DashboardService'):
            cls.cfg[nameval[0]] = nameval[1]
        authServiceUrl = cls.cfg.get('auth-service-url',
                                     'https://kbase.us/services/authorization/Sessions/Login')
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'DashboardService',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.serviceWizardURL = cls.cfg['service-wizard']
        cls.wsClient1 = Workspace(cls.wsURL, token=token)
        cls.serviceImpl = DashboardService(cls.cfg)
        # cls.SetAPI_version = cls.cfg['setapi-version']
        # cls.DataPalette_version = cls.cfg['datapaletteservice-version']
        # cls.intro_text_file = cls.cfg['intro-markdown-file']
        # Second user
        test_cfg_file = '/kb/module/work/test.cfg'
        test_cfg_text = "[test]\n"
        with open(test_cfg_file, "r") as f:
            test_cfg_text += f.read()
        config = ConfigParser()
        config.readfp(StringIO.StringIO(test_cfg_text))
        test_cfg_dict = dict(config.items("test"))
        if 'test_token2' not in test_cfg_dict:
            raise ValueError("Configuration in <module>/test_local/test.cfg file should " +
                             "include second user credentials ('test_token2' key)")
        token2 = test_cfg_dict['test_token2']
        user2 = auth_client.get_user(token2)
        print("Test user2: " + user2)
        cls.ctx2 = MethodContext(None)
        cls.ctx2.update({'token': token2,
                         'user_id': user2,
                         'provenance': [
                            {'service': 'DashboardService',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                         'authenticated': 1})
        cls.wsClient2 = Workspace(cls.wsURL, token=token2)
        cls.wsClients = [cls.wsClient1, cls.wsClient2]
        cls.createdWorkspaces = [[], []]
        # Example objects:
        cls.example_ws_name = cls.createWsStatic(0)
        # Reads
        # cls.example_reads_name = "example_reads.1"
        # foft = FakeObjectsForTests(os.environ['SDK_CALLBACK_URL'])
        # info1 = foft.create_fake_reads({'ws_name': cls.example_ws_name,
        #                                 'obj_names': [cls.example_reads_name]})[0]
        # cls.example_reads_ref = str(info1[6]) + '/' + str(info1[0]) + '/' + str(info1[4])
        # # Genome
        # cls.example_genome_name = "example_genome.1"
        # foft = FakeObjectsForTests(os.environ['SDK_CALLBACK_URL'])
        # info2 = foft.create_fake_genomes({'ws_name': cls.example_ws_name,
        #                                   'obj_names': [cls.example_genome_name]})[0]
        # cls.example_genome_ref = str(info2[6]) + '/' + str(info2[0]) + '/' + str(info2[4])
        # # Other objects
        # foft.create_any_objects({'ws_name': cls.example_ws_name,
        #                          'obj_names': ['any_obj_' + str(i) for i in range(0, 30)]})

    @classmethod
    def tearDownClass(cls):
        for user_pos in range(0, 2):
            for wsName in cls.createdWorkspaces[user_pos]:
                try:
                    cls.wsClients[user_pos].delete_workspace({'workspace': wsName})
                    print("Test workspace was deleted for user" + str(user_pos + 1))
                except:
                    print("Error deleting test workspace for user" + str(user_pos + 1))

    def getWsClient(self):
        return self.__class__.wsClients[0]

    def getWsClient2(self):
        return self.__class__.wsClients[1]

    def createWs(self):
        return self.__class__.createWsStatic(0)

    def createWs2(self):
        return self.__class__.createWsStatic(1)

    @classmethod
    def createWsStatic(cls, user_pos):
        suffix = int(time.time() * 1000)
        wsName = "test_DashboardService_" + str(suffix)
        cls.wsClients[user_pos].create_workspace({'workspace': wsName})  # noqa
        cls.createdWorkspaces[user_pos].append(wsName)
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def getContext2(self):
        return self.__class__.ctx2

    def test_list_narratives(self):
        ws = self.getWsClient()
        # ret = self.getImpl().create_new_narrative(self.getContext(),
        #                                           {"method": "",
        #                                            "appparam": "",
        #                                            "copydata": ""})[0]
        ret = self.getImpl().status(self.getContext())
        print('TESTING!!')
        try:
            self.assertTrue('state' in ret)
            # wsid = ret['workspaceInfo']['id']
            # nar_list = self.getImpl().list_narratives(self.getContext(), {'type': 'mine'})[0]['narratives']
            # self.assertTrue(in_list(wsid, nar_list))
            # nar_list = self.getImpl().list_narratives(self.getContext(), {'type': 'shared'})[0]['narratives']
            # self.assertTrue(not in_list(wsid, nar_list))
            # nar_list = self.getImpl().list_narratives(self.getContext(), {'type': 'public'})[0]['narratives']
            # self.assertTrue(not in_list(wsid, nar_list))

            # # check from User2 perspective, should not be able to see it
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'mine'})[0]['narratives']
            # self.assertTrue(not in_list(wsid, nar_list))
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'shared'})[0]['narratives']
            # self.assertTrue(not in_list(wsid, nar_list))
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'public'})[0]['narratives']
            # self.assertTrue(not in_list(wsid, nar_list))

            # # make it public, it should appear in the public list, but not in the shared with me list
            # ws.set_global_permission({'id': wsid, 'new_permission': 'r'})
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'mine'})[0]['narratives']
            # self.assertTrue(not in_list(wsid, nar_list))
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'shared'})[0]['narratives']
            # self.assertTrue(not in_list(wsid, nar_list))
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'public'})[0]['narratives']
            # self.assertTrue(in_list(wsid, nar_list))


            # # give user2 write access, which should make it visible to user2's shared narrative list
            # ws.set_permissions({'id': wsid, 'users': [self.getContext2()['user_id']], 'new_permission': 'r'})
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'mine'})[0]['narratives']
            # self.assertTrue(not in_list(wsid, nar_list))
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'shared'})[0]['narratives']
            # self.assertTrue(in_list(wsid, nar_list))
            # nar_list = self.getImpl().list_narratives(self.getContext2(), {'type': 'public'})[0]['narratives']
            # self.assertTrue(in_list(wsid, nar_list))

        finally:
            # new_ws_id = ret['workspaceInfo']['id']
            # ws.delete_workspace({'id': new_ws_id})
            return None
