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

from DashboardService.Errors import ServiceError
from DashboardService.cache.ObjectCache import ObjectCache

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

        # Second user
        test_cfg_file = '/kb/module/work/test.cfg'
        test_cfg_text = "[test]\n"
        with open(test_cfg_file, "r") as f:
            test_cfg_text += f.read()
        config = ConfigParser()
        config.readfp(StringIO.StringIO(test_cfg_text))
        test_cfg_dict = dict(config.items("test"))
        
        
    @classmethod
    def tearDownClass(cls):
        pass    

    def test_construction(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url']
                }
            }
        ]
        for test in test_table:
            try:
                ObjectCache(**test['constructor'])
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)

        test_table = [
            {
                'input': {
                    'constructor': {
                    }
                }
            },
            {
                'input': {
                    'constructor': {
                        'workspace_url':  'x'
                    }
                }
            },
            {
                'input': {
                    'constructor': {
                        'path': 'x',
                    }
                }
            },
            {
                'input': {
                    'constructor': {
                        'workspace_url':  123,
                        'path': 'x',
                    }
                }
            },
            {
                'input': {
                    'constructor': {
                        'workspace_url':  'x',
                        'path': 123,
                    }
                }
            }
        ]
        for test in test_table:
            try:
                ObjectCache(**test['input']['constructor'])
                self.assertTrue(False)
            except ValueError as err:
                self.assertTrue(True)

    def test_initialize(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url']
                }
            }
        ]
        for test in test_table:
            try:
                app_cache = ObjectCache(**test['constructor'])
                app_cache.initialize()
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)

    def test_add_items(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url']
                },
                'add_items': [[
                    [1, 2, 3, 'hi'],
                    [4, 5, 6, 'hello']
                ]]
            }
        ]
        for test in test_table:
            try:
                object_cache = ObjectCache(**test['constructor'])
                object_cache.initialize()
                object_cache.add_items(*test['add_items'])
                all = object_cache.get_all_items()
                # TODO: test that the items are present and the only ones.
                self.assertTrue(True)
            except ValueError as err:
                print('ERROR!', err)
                self.assertTrue(False) 

    def test_caching(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url']
                },
                'get': [[
                    [34742, 1, None],
                    [34599, 1, None]
                ]]
            }
        ]
        for test in test_table:
            try:
                object_cache = ObjectCache(**test['constructor'])
                object_cache.initialize()
                items = object_cache.get_items(*test['get'])
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
                    'token': self.token
                },
                'fetch_items': [[
                    [34742, 1],
                    [34599, 1]
                ]]
            }
        ]
        for test in test_table:
            try:
                object_cache = ObjectCache(**test['constructor'])
                object_cache.initialize()
                items = object_cache.fetch_items(*test['fetch_items'])
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)  

    def test_get(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token
                },
                'get': [[
                    [34742, 1, None],
                    [34599, 1, None]
                ]]
            }
        ]
        for test in test_table:
            try:
                object_cache = ObjectCache(**test['constructor'])
                object_cache.initialize()
                items = object_cache.get(*test['get'])
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)  

    def test_get2(self):
        db_path = self.cfg['cache-directory'] + '/object_cache.db'
        now = int(round(time.time() * 1000))
        now2 = now + 10000;
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'workspace_url':  self.cfg['workspace-url'],
                    'token': self.token
                },
                'get1': [[
                    [34742, 1, now],
                    [34599, 1, now]
                ]],
                'get2': [[
                    [34742, 1, now2],
                    [34599, 1, 1532558773000]
                ]]
            }
        ]
        for test in test_table:
            try:
                object_cache = ObjectCache(**test['constructor'])
                object_cache.initialize()
                items = object_cache.get(*test['get1'])
                items2 = object_cache.get(*test['get2'])
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)             

    # def test_load(self):
    #     db_path = self.cfg['cache-directory'] + '/app_cache.db'
    #     test_table = [
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'narrative_method_store_url':  self.cfg['narrative-method-store-url']
    #             },
    #             'load_for_tag': {
    #                 'input': ['dev']
    #             },
    #             'expect': {
    #                 'success': True,
    #                 'exception': False
    #             }
    #         },
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'narrative_method_store_url':  self.cfg['narrative-method-store-url']
    #             },
    #             'load_for_tag': {
    #                 'input': ['beta']
    #             },
    #             'expect': {
    #                 'success': True,
    #                 'exception': False
    #             }
    #         },
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'narrative_method_store_url':  self.cfg['narrative-method-store-url']
    #             },
    #             'load_for_tag': {
    #                 'input': ['release']
    #             },
    #             'expect': {
    #                 'success': True,
    #                 'exception': False
    #             }
    #         },
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'narrative_method_store_url':  self.cfg['narrative-method-store-url']
    #             },
    #             'load_for_tag': {
    #                 'input': ['foo']
    #             },
    #             'expect': {
    #                 'success': False,
    #                 'exception': True,
    #                 'exceptionClass': ServiceError,
    #                 'error': {
    #                     'message': 'Repo-tag [foo] is not supported',
    #                     'code': -32500,
    #                     'name': 'JSONRPCError'
    #                 }
    #             }
    #         }
    #     ]
    #     for test in test_table:
    #         try:
    #             app_cache = AppCache(**test['constructor'])
    #             app_cache.initialize()
    #             app_cache.load_for_tag(*test['load_for_tag']['input'])
    #             self.assertTrue(test['expect']['success'])
    #         except Exception as err:
    #             # print('ERR', err)
    #             self.assertTrue(test['expect']['exception'])
    #             self.assertIsInstance(err, test['expect']['exceptionClass'])
    #             self.assertIsInstance(str(err), basestring)
    #             # print('ERR code', err.args[1])
    #             # print(test['expect']['error'])
    #             for key, value in test['expect']['error'].iteritems():
    #                 self.assertEquals(getattr(err, key), value)

    # def test_get(self):
    #     db_path = self.cfg['cache-directory'] + '/user_profile_cache.db'
    #     test_table = [
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'user_profile_url':  self.cfg['user-profile-service-url']
    #             },
    #             'input': ['eapearson'],
    #             'expect': {
    #                 'found': True,
    #             }
    #         },
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'user_profile_url':  self.cfg['user-profile-service-url']
    #             },
    #             'input': ['mickey_mouse_123'],
    #             'expect': {
    #                 'found': False,
    #             }
    #         },
    #     ]
    #     for test in test_table:
    #         try:
    #             cache = UserProfileCache(**test['constructor'])
    #             cache.initialize()
    #             cache.load_all()
    #             app, found = cache.get(*test['input'])
    #             if (test['expect']['found']):
    #                 self.assertTrue(found)
    #                 self.assertIsNotNone(app)
    #             else:
    #                 self.assertFalse(found)
    #         except ValueError as err:
    #             self.assertTrue(False)   

    # def test_fetch_profiles(self):
    #     db_path = self.cfg['cache-directory'] + '/user_profile_cache.db'
    #     test_table = [
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'user_profile_url':  self.cfg['user-profile-service-url']
    #             },
    #             'input': ['eapearson'],
    #             'expect': {
    #                 'found': True,
    #             }
    #         },
    #         {
    #             'constructor': {
    #                 'path': db_path,
    #                 'user_profile_url':  self.cfg['user-profile-service-url']
    #             },
    #             'input': ['mickey_mouse_123'],
    #             'expect': {
    #                 'found': False,
    #             }
    #         },
    #     ]
    #     for test in test_table:
    #         try:
    #             cache = UserProfileCache(**test['constructor'])
    #             cache.initialize()
    #             cache.load_all()
    #             app, found = cache.get(*test['input'])
    #             if (test['expect']['found']):
    #                 self.assertTrue(found)
    #                 self.assertIsNotNone(app)
    #             else:
    #                 self.assertFalse(found)
    #         except ValueError as err:
    #             self.assertTrue(False)     