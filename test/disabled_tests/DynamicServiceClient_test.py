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
from DashboardService.DynamicServiceClient import DynamicServiceClient

class DynamicServiceClientTest(unittest.TestCase):

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

        # Second user
        test_cfg_file = '/kb/module/work/test.cfg'
        test_cfg_text = "[test]\n"
        with open(test_cfg_file, "r") as f:
            test_cfg_text += f.read()
        config = ConfigParser()
        config.readfp(StringIO.StringIO(test_cfg_text))
        test_cfg_dict = dict(config.items("test"))

        
        cls.createdWorkspaces = [];
        
    @classmethod
    def tearDownClass(cls):
        pass

    def test_dynamic_service_client_bad_input(self):
        # TODO: add constructor validation?
        # test_table = [
        #     {
        #         'input': {
        #             'constructor': {
        #                 'url': 'x',
        #                 'module: 'x',
        #                 'token': 'x',
        #                 'service_ver': 'x',
        #                 'refresh_cycle_seconds': 100
        #             },
        #             'call_func': ['a_method', None]
        #         }
        #     }
            
        # ]
        # for test in test_table:
        #     try:
        #         DynamicServiceClient(**test['input'])
        #         self.assertTrue(False)
        #     except ValueError as err:
        #         self.assertTrue(True)

        test_table = [
            {
                'input': {
                    'constructor': {
                        'url': 'x',
                        'module': 'x',
                        'token': 'x',
                        'service_ver': 'x',
                        'refresh_cycle_seconds': 100
                    },
                    'call_func': ['a_method', None]
                }
            },
            {
                'input': {
                    'constructor': {
                        'url': 'x',
                        'module': 'x',
                        'token': 'x',
                        'service_ver': 'x',
                        'refresh_cycle_seconds': 100
                    },
                    'call_func': [None, []]
                }
            }
        ]
        for test in test_table:
            try:
                client = DynamicServiceClient(**test['input']['constructor'])
                client.call_func(*test['input']['call_func'])
                self.assertTrue(False)
            except ValueError as err:
                self.assertTrue(True)

    def test_call_module(self):
        test_table = [
            {
                'constructor': {
                    'module': 'Test',
                    'url': 'http://localhost:5001',
                    'token': 'x'
                },
                'call_func': ['status', [{}]],
                'expect': {
                    'result': [{'state': 'ok'}]
                }
            }
        ]
        for test in test_table:
            try:
                client = DynamicServiceClient(**test['constructor'])
                result = client.call_func(*test['call_func'])

                r1 = json.dumps(result, sort_keys=True, indent=2)
                r2 = json.dumps(test['expect']['result'], sort_keys=True, indent=2)
                self.assertEqual(r1, r2)
            except Exception as err:
                self.assertTrue(False)

    def test_bad_module_name(self):
        test_table = [
            {
                'constructor': {
                    'module': 'Testx',
                    'url': 'http://localhost:5001',
                    'token': 'x'
                },
                'call_func': ['status', [{}]],
                'expect': {
                    'exception': ServiceError
                }
            }
        ]
        for test in test_table:
            try:
                client = DynamicServiceClient(**test['constructor'])
                client.call_func(*test['call_func'])
                self.assertTrue(False)
            except Exception as err:
                self.assertIsInstance(err, ServiceError)

    # def test_throws(self):
    #     try:
    #         client = DynamicServiceClient(
    #             module='Test',
    #             url='http://localhost:5001',
    #             token='x'
    #         )
    #         result, error = client.call_func('non_json_response', [{}])
    #         self.assertTrue(False)
    #     except Exception as err:
    #         self.assertTrue(True)            