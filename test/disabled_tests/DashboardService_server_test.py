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

from Workspace.WorkspaceClient import Workspace
from DashboardService.DashboardServiceImpl import DashboardService
from DashboardService.DashboardServiceServer import MethodContext
from DashboardService.Validation import Validation
from DashboardService.authclient import KBaseAuth as _KBaseAuth
from DashboardService.ServiceUtils import ServiceUtils
from DashboardService.DynamicServiceClient import DynamicServiceClient

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

        cls.wsClient = Workspace(cls.wsURL, token=token)

        cls.serviceImpl = DashboardService(cls.cfg)

        # Second user
        test_cfg_file = '/kb/module/work/test.cfg'
        test_cfg_text = "[test]\n"
        with open(test_cfg_file, "r") as f:
            test_cfg_text += f.read()
        config = ConfigParser()
        config.readfp(StringIO.StringIO(test_cfg_text))
        test_cfg_dict = dict(config.items("test"))

        # Disable second test user for now. 
        # TODO: add back later
        # if 'test_token2' not in test_cfg_dict:
        #     raise ValueError("Configuration in <module>/test_local/test.cfg file should " +
        #                      "include second user credentials ('test_token2' key)")
        # token2 = test_cfg_dict['test_token2']
        # user2 = auth_client.get_user(token2)
        # print("Test user2: " + user2)
        # cls.ctx2 = MethodContext(None)
        # cls.ctx2.update({'token': token2,
        #                  'user_id': user2,
        #                  'provenance': [
        #                     {'service': 'DashboardService',
        #                      'method': 'please_never_use_it_in_production',
        #                      'method_params': []
        #                      }],
        #                  'authenticated': 1})
        # cls.wsClient2 = Workspace(cls.wsURL, token=token2)

        # cls.wsClients = [cls.wsClient1, cls.wsClient2]
        # cls.createdWorkspaces = [[], []]
        cls.createdWorkspaces = [];
        # Example objects:

        # TODO: have narrative, not workspace, created and destroyed on demand by specific tests,
        # not globally for the tests.
        # cls.example_ws_name = cls.createWsStatic()

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
        for wsName in cls.createdWorkspaces:
            try:
                cls.wsClient.delete_workspace({'workspace': wsName})
                print("Test workspace " + wsName + " was deleted for user" + cls.ctx['user_id'])
            except:
                print("Error deleting test workspace " + wsName + " was deleted for user" + cls.ctx['user_id'])

    def getWsClient(self):
        return self.__class__.wsClient

    # def getWsClient2(self):
    #     return self.__class__.wsClients[1]

    def createWs(self):
        return self.__class__.createWsStatic

    # def createWs2(self):
    #     return self.__class__.createWsStatic(1)

    @classmethod
    def createWsStatic(cls):
        suffix = int(time.time() * 1000)
        wsName = "test_DashboardService_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': wsName})  # noqa
        cls.createdWorkspaces.append(wsName)
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # def getContext2(self):
    #     return self.__class__.ctx2

    def test_status(self):
        # ret = self.getImpl().create_new_narrative(self.getContext(),
        #                                           {"method": "",
        #                                            "appparam": "",
        #                                            "copydata": ""})[0]
        ret = self.getImpl().status(self.getContext())[0]
        
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, dict) 
        self.assertEquals(ret['state'], 'OK')

    def test_list_all_narratives(self):
        ret, err, stats = self.getImpl().list_all_narratives(self.getContext(), {})

        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsNotNone(stats)
        self.assertIsInstance(ret, dict)
        narratives = ret['narratives']
        profiles = ret['profiles']
        self.assertIsInstance(narratives, list) 
        self.assertIsInstance(profiles, list)

    def test_list_all_narratives_bad_input(self):
        test_table = [
            {
                'input': {
                    'just_modified_after': 123
                },
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            }
        ]
        for test in test_table:
            ret, err, stats = self.getImpl().list_all_narratives(self.getContext(), test['input'])
            self.assertIsNone(ret)
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], test['expected']['type'])
            self.assertEquals(err['code'], test['expected']['code'])

    def test_create_narrative(self):
        input = {
            'title': 'Test Narrative'
        }
        ret, err = self.getImpl().create_narrative(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)

    def test_create_narrative_bad_input(self):
        test_table = [
            {
                'input': {                    
                },
                'expected': {
                    'type': 'input',
                    'code': 'missing'
                }
            },
            {
                'input': {
                    'title': 123
                },
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            },
            {
                'input': {
                    'title': 'my narrative which will never exist',
                    'name': 123
                },
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            }
        ]
        for test in test_table:
            ret, err = self.getImpl().create_narrative(self.getContext(), test['input'])
            self.assertIsNone(ret)
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], test['expected']['type'])
            self.assertEquals(err['code'], test['expected']['code'])

    def test_delete_narrative(self):
        input = {
            'title': 'Test Delete Narrative'
        }
        ret, err = self.getImpl().create_narrative(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)

        narrative = ret['narrative']

        input = {
            'obji': {
                'workspace_id': narrative['workspaceId'],
                'object_id': narrative['objectId'],
                'version': narrative['objectVersion']
            }
        }
        [err] = self.getImpl().delete_narrative(self.getContext(), input)
        self.assertIsNone(err)

    def test_delete_narrative_bad_input(self):
        # input = {
        #     'title': 'Test Delete Narrative with Bad Input'
        # }
        # ret, err = self.getImpl().create_narrative(self.getContext(), input)
        # self.assertIsNotNone(ret)
        # self.assertIsNone(err)
        # self.assertIsInstance(ret, dict)

        # narrative = ret['narrative']

        test_table = [
            {
                'input': {
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'missing'
                }
            },
            {
                'input': {
                    'obji': '123'
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            }
        ]
        for test in test_table:
            [err] = self.getImpl().delete_narrative(self.getContext(), test['input'])
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], test['expected']['type'])
            self.assertEquals(err['code'], test['expected']['code'])

    def test_share_narrative(self):
        input = {
            'title': 'Test Share Narrative'
        }
        ret, err = self.getImpl().create_narrative(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)

        narrative = ret['narrative']

        input = {
            'wsi': {
                'id': narrative['workspaceId']
            },
            'users': ['eaptest30'],
            'permission': 'r'
        }
        [err] = self.getImpl().share_narrative(self.getContext(), input)
        self.assertIsNone(err)

    def test_share_narrative_bad_input(self):
        test_table = [
            {
                'input': {
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'missing'
                }
            },
            {
                'input': {
                    'wsi': '123',
                    'users': ['eaptest30'],
                    'permission': 'r'
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            },
            {
                'input': {
                    'wsi': {
                        'id': 'astring'
                    },
                    'users': 'anotherstring',
                    'permission': 'r'
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            },
            {
                'input': {
                    'wsi': {
                        'id': 'astring'
                    },
                    'users': ['eaptest30'],
                    'permission': 123
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            }
        ] 
        for test in test_table:
            [err] = self.getImpl().share_narrative(self.getContext(), test['input'])
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], test['expected']['type'])
            self.assertEquals(err['code'], test['expected']['code'])
    
    def test_unshare_narrative(self):
        input = {
            'title': 'Test UnShare Narrative'
        }
        ret, err = self.getImpl().create_narrative(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)

        narrative = ret['narrative']

        input = {
            'wsi': {
                'id': narrative['workspaceId']
            },
            'users': ['eaptest30'],
            'permission': 'r'
        }
        [err] = self.getImpl().share_narrative(self.getContext(), input)
        self.assertIsNone(err)

        input = {
            'wsi': {
                'id': narrative['workspaceId']
            },
            'users': ['eaptest30']
        }
        [err] = self.getImpl().unshare_narrative(self.getContext(), input)
        self.assertIsNone(err)

    def test_unshare_narrative_bad_input(self):
        test_table = [
            {
                'input': {
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'missing'
                }
            },
            {
                'input': {
                    'wsi': '123',
                    'users': ['eaptest30'],
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            },
            {
                'input': {
                    'wsi': {
                        'id': 'astring'
                    },
                    'users': 'anotherstring',
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            }
        ] 
        for test in test_table:
            [err] = self.getImpl().unshare_narrative(self.getContext(), test['input'])
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], test['expected']['type'])
            self.assertEquals(err['code'], test['expected']['code'])

    def test_share_narrative_global(self):
        input = {
            'title': 'Test Share Narrative Global/Public'
        }
        ret, err = self.getImpl().create_narrative(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)

        narrative = ret['narrative']

        input = {
            'wsi': {
                'id': narrative['workspaceId']
            }
        }
        [err] = self.getImpl().share_narrative_global(self.getContext(), input)
        self.assertIsNone(err)

    def test_share_narrative_global_bad_input(self):
        test_table = [
            {
                'input': {
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'missing'
                }
            },
            {
                'input': {
                    'wsi': '123'
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            }
        ] 
        for test in test_table:
            [err] = self.getImpl().share_narrative_global(self.getContext(), test['input'])
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], test['expected']['type'])
            self.assertEquals(err['code'], test['expected']['code'])

    def test_unshare_narrative_global(self):
        input = {
            'title': 'Test Share and Unshare Narrative Global/Public'
        }
        ret, err = self.getImpl().create_narrative(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)

        narrative = ret['narrative']

        input = {
            'wsi': {
                'id': narrative['workspaceId']
            }
        }
        [err] = self.getImpl().share_narrative_global(self.getContext(), input)
        self.assertIsNone(err)

        [err] = self.getImpl().unshare_narrative_global(self.getContext(), input)
        self.assertIsNone(err) 

    def test_unshare_narrative_global_bad_input(self):
        test_table = [
            {
                'input': {
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'missing'
                }
            },
            {
                'input': {
                    'wsi': '123'
                }, 
                'expected': {
                    'type': 'input',
                    'code': 'wrong-type'
                }
            }
        ] 
        for test in test_table:
            [err] = self.getImpl().unshare_narrative_global(self.getContext(), test['input'])
            self.assertIsInstance(err, dict)
            self.assertEquals(err['type'], test['expected']['type'])
            self.assertEquals(err['code'], test['expected']['code'])

    def test_config_bad(self):
        test_table = [
            {
                'input': {                        
                }
            },
            {
                'input': {
                    'xcache-directory': 'x',
                    'workspace-url': 'x',
                    'service-wizard': 'x',
                    'narrative-method-store-url': 'x',
                    'user-profile-service-url': 'x'
                }
            },
            {
                'input': {
                    'cache-directory': 'x',
                    'xworkspace-url': 'x',
                    'service-wizard': 'x',
                    'narrative-method-store-url': 'x',
                    'user-profile-service-url': 'x'
                }
            },
            {
                'input': {
                    'cache-directory': 'x',
                    'workspace-url': 'x',
                    'xservice-wizard': 'x',
                    'narrative-method-store-url': 'x',
                    'user-profile-service-url': 'x'
                }
            },
            {
                'input': {
                    'cache-directory': 'x',
                    'workspace-url': 'x',
                    'service-wizard': 'x',
                    'xnarrative-method-store-url': 'x',
                    'user-profile-service-url': 'x'
                }
            },
            {
                'input': {
                    'cache-directory': 'x',
                    'workspace-url': 'x',
                    'service-wizard': 'x',
                    'narrative-method-store-url': 'x',
                    'xuser-profile-service-url': 'x'
                }
            }
        ]

        for test in test_table:
            ret, error = Validation.validate_config(test['input'])
            self.assertIsNone(ret)
            self.assertIsInstance(error, basestring)

    def test_impl_bad_config(self):
        test_table = [
            {
                'input': {                        
                }
            }
        ]
        for test in test_table:
            try:
                DashboardService(test['input'])
                self.assertTrue(False)
            except ValueError as err:
                self.assertTrue(True)

    def test_service_utils(self):
        # parse_app
        test_table = [
            {
                'input': 'name',
                'expected': {
                    'type': dict
                }
            },
            {
                'input': 'module/name',
                'expected': {
                    'type': dict
                }
            },
            {
                'input': 'module/name/hash',
                'expected': {
                    'type': dict
                }
            },
            {
                'input': '',
                'expected': {
                    'type': type(None)
                }
            }
        ]
        for test in test_table:
            value = ServiceUtils.parse_app_key(test['input'])
            self.assertIsInstance(value, test['expected']['type'])

   
