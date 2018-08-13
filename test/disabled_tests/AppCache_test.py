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
from DashboardService.cache.AppCache import AppCache

class GenericClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
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

    def test_app_cache(self):
        db_path = self.cfg['cache-directory'] + '/app_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                }
            }
        ]
        for test in test_table:
            try:
                AppCache(**test['constructor'])
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
                        'narrative_method_store_url':  'x'
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
                        'narrative_method_store_url':  123,
                        'path': 'x',
                    }
                }
            },
            {
                'input': {
                    'constructor': {
                        'narrative_method_store_url':  'x',
                        'path': 123,
                    }
                }
            }
        ]
        for test in test_table:
            try:
                AppCache(**test['input']['constructor'])
                self.assertTrue(False)
            except ValueError as err:
                self.assertTrue(True)

    def test_initialize(self):
        db_path = self.cfg['cache-directory'] + '/app_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                }
            }
        ]
        for test in test_table:
            try:
                app_cache = AppCache(**test['constructor'])
                app_cache.initialize()
                self.assertTrue(True)
            except ValueError as err:
                self.assertTrue(False)

    def test_populate(self):
        db_path = self.cfg['cache-directory'] + '/app_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                }
            }
        ]
        for test in test_table:
            try:
                app_cache = AppCache(**test['constructor'])
                app_cache.initialize()
                app_cache.load_all()
                self.assertTrue(True)
            except ValueError as err:
                print('ERROR!', err)
                self.assertTrue(False)                

    def test_load(self):
        db_path = self.cfg['cache-directory'] + '/app_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                },
                'load_for_tag': {
                    'input': ['dev']
                },
                'expect': {
                    'success': True,
                    'exception': False
                }
            },
            {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                },
                'load_for_tag': {
                    'input': ['beta']
                },
                'expect': {
                    'success': True,
                    'exception': False
                }
            },
            {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                },
                'load_for_tag': {
                    'input': ['release']
                },
                'expect': {
                    'success': True,
                    'exception': False
                }
            },
            {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                },
                'load_for_tag': {
                    'input': ['foo']
                },
                'expect': {
                    'success': False,
                    'exception': True,
                    'exceptionClass': ServiceError,
                    'error': {
                        'message': 'Repo-tag [foo] is not supported',
                        'code': -32500,
                        'name': 'JSONRPCError'
                    }
                }
            }
        ]
        for test in test_table:
            try:
                app_cache = AppCache(**test['constructor'])
                app_cache.initialize()
                app_cache.load_for_tag(*test['load_for_tag']['input'])
                self.assertTrue(test['expect']['success'])
            except Exception as err:
                # print('ERR', err)
                self.assertTrue(test['expect']['exception'])
                self.assertIsInstance(err, test['expect']['exceptionClass'])
                self.assertIsInstance(str(err), basestring)
                # print('ERR code', err.args[1])
                # print(test['expect']['error'])
                for key, value in test['expect']['error'].iteritems():
                    self.assertEquals(getattr(err, key), value)

    def test_get(self):
        db_path = self.cfg['cache-directory'] + '/app_cache.db'
        test_table = [
            {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                },
                'input': ['ug_kb_ea_utils/run_Fastq_Multx'],
                'expect': {
                    'found': True,
                }
            },
             {
                'constructor': {
                    'path': db_path,
                    'narrative_method_store_url':  self.cfg['narrative-method-store-url']
                },
                'input': ['does_not_exist'],
                'expect': {
                    'found': False,
                }
            }
        ]
        for test in test_table:
            try:
                app_cache = AppCache(**test['constructor'])
                app_cache.initialize()
                app_cache.load_all()
                app, found = app_cache.get(*test['input'])
                if (test['expect']['found']):
                    self.assertTrue(found)
                    self.assertIsNotNone(app)
                else:
                    self.assertFalse(found)
            except ValueError as err:
                self.assertTrue(False)    