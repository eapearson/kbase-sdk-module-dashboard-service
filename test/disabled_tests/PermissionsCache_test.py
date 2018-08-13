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

from DashboardService.authclient import KBaseAuth
from DashboardService.Errors import ServiceError
from DashboardService.cache.PermissionsCache import PermissionsCache

class UserProfileTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        cls.token = token
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('DashboardService'):
            cls.cfg[nameval[0]] = nameval[1]

        test_cfg_file = '/kb/module/work/test.cfg'
        test_cfg_text = "[test]\n"
        with open(test_cfg_file, "r") as f:
            test_cfg_text += f.read()
        config = ConfigParser()
        config.readfp(StringIO.StringIO(test_cfg_text))
        test_cfg_dict = dict(config.items("test"))

        authServiceUrl = cls.cfg.get('auth-service-url',
                                     'https://kbase.us/services/authorization/Sessions/Login')
        auth_client = KBaseAuth(authServiceUrl)
        cls.username = auth_client.get_user(token)
        
        
    @classmethod
    def tearDownClass(cls):
        pass    

    def test_construction(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token,
                    'username': self.username
                }
            }
        ]
        for test in test_table:
            try:
                PermissionsCache(**test['constructor'])
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)

        test_table = [
            {
                'input': {
                    'constructor': {
                    }
                },
                'expect': {
                    'exception': True
                }
            },
            {
                'input': {
                    'constructor': {
                        # 'path': 'x',
                        'workspace_url':  'x',
                        'token': 'x',
                        'username': 'x'
                    }
                },
                'expect': {
                    'exception': True
                }
            },
            {
                'input': {
                    'constructor': {
                        'path': 'x',
                        # 'workspace_url':  'x',
                        'token': 'x',
                        'username': 'x'
                    }
                },
                'expect': {
                    'exception': True
                }
            },
            {
                'input': {
                    'constructor': {
                        'path': 'x',
                        'workspace_url':  'x',
                        # 'token': 'x',
                        'username': 'x'
                    }
                },
                'expect': {
                    'exception': False
                }
            },
            {
                'input': {
                    'constructor': {
                        'path': 'x',
                        'workspace_url':  'x',
                        'token': 'x',
                        # 'username': 'x'
                    }
                },
                'expect': {
                    'exception': False
                }
            },
            {
                'input': {
                    'constructor': {
                        'path': 123,
                        'workspace_url':  'x',
                        'token': 'x',
                        'username': 'x'
                    }
                },
                'expect': {
                    'exception': True
                }
            },
            {
                'input': {
                    'constructor': {
                        'path': 'x',
                        'workspace_url':  123,
                        'token': 'x',
                        'username': 'x'
                    }
                },
                'expect': {
                    'exception': True
                }
            },
            {
                'input': {
                    'constructor': {
                        'path': 'x',
                        'workspace_url':  'x',
                        'token': 123,
                        'username': 'x'
                    }
                },
                'expect': {
                    'exception': True
                }
            },
            {
                'input': {
                    'constructor': {
                        'path': 'x',
                        'workspace_url':  'x',
                        'token': 'x',
                        'username': 123
                    }
                },
                'expect': {
                    'exception': True
                }
            }
        ]
        for test in test_table:
            try:
                PermissionsCache(**test['input']['constructor'])
                self.assertFalse(test['expect']['exception'])
            except ValueError as err:
                self.assertTrue(test['expect']['exception'])

    def test_initialize(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token,
                    'username': self.username
                }
            }
        ]
        for test in test_table:
            try:
                cache = PermissionsCache(**test['constructor'])
                cache.initialize()
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)

    def test_add_items(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token,
                    'username': self.username
                },
                'add_items': [[
                    [1, 'me', 'hi'],
                    [4, 'you', 'hello']
                ]]
            }
        ]
        for test in test_table:
            try:
                cache = PermissionsCache(**test['constructor'])
                cache.initialize()
                cache.add_items(*test['add_items'])
                all = cache.get_all_items()
                self.assertGreater(len(all), 0)
                # TODO: test that the items are present and the only ones.
                self.assertTrue(True)
            except ValueError as err:
                print('ERROR!', err)
                self.assertTrue(False) 

    def test_get_items(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token,
                    'username': self.username
                },
                'add_items': [[
                    [34742, 'eapearson', 'hi'],
                    [34742, 'eapearson', 'hello']
                ]],
                'get_items': [[
                    [34742, 'eapearson'],
                    [34599, 'eapearson']
                ]]
            }
        ]
        for test in test_table:
            try:
                cache = PermissionsCache(**test['constructor'])
                cache.initialize()
                cache.add_items(*test['add_items'])
                items = cache.get_items(*test['get_items'])
                self.assertGreater(len(items), 0)
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)

    def test_fetch_items(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token,
                    'username': self.username
                },
                'fetch_items': [[
                    [34742, 'eapearson'],
                    [34599, 'eapearson']
                ]]
            }
        ]
        for test in test_table:
            try:
                cache = PermissionsCache(**test['constructor'])
                cache.initialize()
                items = cache.fetch_items(*test['fetch_items'])
                self.assertEqual(len(items), 2)
            except ValueError as err:
                print('ERROR!', err)
                self.assertTrue(False)  

    def test_get(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token,
                    'username': self.username
                },
                'get': [[
                    34742,
                    34599
                ]]
            }
        ]
        for test in test_table:
            try:
                cache = PermissionsCache(**test['constructor'])
                cache.initialize()
                items = cache.get(*test['get'])
                self.assertEqual(len(items), 2)
                items = cache.get(*test['get'])
                self.assertEqual(len(items), 2)
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)  

    def test_refresh(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token,
                    'username': self.username
                },
                'add_items': [[
                    [34742, 'eapearson', 'hi'],
                    [34599, 'eapearson', 'hello']
                ]],
                'refresh_items': [[34742, 34599]]
            }
        ]
        for test in test_table:
            try:
                cache = PermissionsCache(**test['constructor'])
                cache.initialize()
                cache.add_items(*test['add_items'])
                cache.refresh_items(*test['refresh_items'])
                items = cache.get_all_items()
                self.assertGreater(len(items), 0)
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)

    def test_add_items_perf(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        # test_table = [
        #     {
        #         'constructor': {
        #             'path': db_path,
        #             'workspace_url':  self.cfg['workspace-url'],
        #             'token': self.token,
        #             'username': self.username
        #         },
        #         'add_items': [[
        #             [1, 'me', 'hi'],
        #             [4, 'you', 'hello']
        #         ]]
        #     }
        # ]
        constructor = {
            'path': db_path,
            'workspace_url':  self.cfg['workspace-url'],
            'token': self.token,
            'username': self.username
        }
        data = {
            'field1': 'value1',
            'field2': 'value2',
            'field3': 1234
        }
        test_data = ([i, 'eapearson', json.dumps(data)] for i in xrange(0,1000))
        # for test_data in test_table:
        try:
            cache = PermissionsCache(**constructor)
            cache.initialize()
            start = time.time()
            print('START')
            # print(test_data)
            cache.add_items(test_data)
            elapsed = time.time() - start
            print('END %s' % (elapsed/1000))
            all = cache.get_all_items()
            self.assertGreater(len(all), 0)
            # TODO: test that the items are present and the only ones.
            self.assertTrue(True)
        except ValueError as err:
            print('ERROR!', err)
            self.assertTrue(False) 

    # def test_get2(self):
    #     db_path = self.cfg['cache-directory'] + '/object_cache.db'
    #     now = int(round(time.time() * 1000))
    #     now2 = now + 10000;
    #     test_table = [
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'workspace_url':  self.cfg['workspace-url'],
    #                 'token': self.token
    #             },
    #             'get1': [[
    #                 [34742, 1, now],
    #                 [34599, 1, now]
    #             ]],
    #             'get2': [[
    #                 [34742, 1, now2],
    #                 [34599, 1, 1532558773000]
    #             ]]
    #         }
    #     ]
    #     for test in test_table:
    #         try:
    #             object_cache = ObjectCache(**test['constructor'])
    #             object_cache.initialize()
    #             items = object_cache.get(*test['get1'])
    #             items2 = object_cache.get(*test['get2'])
    #             self.assertTrue(True)
    #         except ValueError as err:
    #             self.assertTrue(False)             

      