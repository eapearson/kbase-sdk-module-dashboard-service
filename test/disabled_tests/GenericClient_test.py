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
from DashboardService.GenericClient import GenericClient 

class GenericClientTest(unittest.TestCase):

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

        
    @classmethod
    def tearDownClass(cls):
        pass

    def test_generic_client(self):
        test_table = [
            {
                'constructor': {
                    'module': 'Test',
                    'url': 'http://localhost:5001',
                    'token': 'x'
                },
                'call_func': ['status', [{}]]
            }
        ]
        for test in test_table:
            try:
                client = GenericClient(**test['constructor'])
                client.call_func(*test['call_func'])
                self.assertTrue(True)
            except ValueError as err:
                print('ERROR!', err)
                self.assertTrue(False)


    def test_generic_client_bad_calls(self):
        test_table = [
            {
                'input': {
                }
            },
            {
                'input': {
                    'url': 'x',
                    'token': 'x'
                }
            },
            {
                'input': {
                    'module': 'x',
                    'token': 'x'
                }
            }
        ]
        for test in test_table:
            try:
                GenericClient(**test['input'])
                self.assertTrue(False)
            except ValueError:
                self.assertTrue(True)

        test_table = [
            {
                'input': {
                    'constructor': {
                        'module': 'x',
                        'url': 'x',
                        'token': 'x'
                    },
                    'call_func': [None, None]
                }
            },
            {
                'input': {
                    'constructor': {
                        'module': 'x',
                        'url': 'x',
                        'token': 'x'
                    },
                    'call_func': ['x', None]
                }
            },
            {
                'input': {
                    'constructor': {
                        'module': 'x',
                        'url': 'x',
                        'token': 'x'
                    },
                    'call_func': [None, 'x']
                }
            },
        ]
        for test in test_table:
            try:
                client = GenericClient(**test['input']['constructor'])
                client.call_func(*test['input']['call_func'])
                self.assertTrue(False)
            except ValueError as err:
                self.assertTrue(True)

    # These simulate service errors - detected by the 
    # jsonrpc server and returned as official jsonrpc errors

    def test_generic_client_mock_500(self):
        try:
            client = GenericClient(
                module='Test',
                url='http://localhost:5001',
                token='x'
            )
            client.call_func('trigger_500', [{}])
            self.assertTrue(False)
        except ServiceError as err:
            self.assertTrue(True)
            self.assertEqual(err.code, -32000)

    # TODO: many more!


    # These simulate json server mistakes -- invalid responses.

    def test_generic_client_mock_not_json(self):
        try:
            client = GenericClient(
                module='Test',
                url='http://localhost:5001',
                token='x'
            )
            client.call_func('non_json_response', [{}])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_generic_client_mock_not_json_content_type(self):
        try:
            client = GenericClient(
                module='Test',
                url='http://localhost:5001',
                token='x'
            )
            client.call_func('incorrect_content_type', [{}])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_return_non_list(self):
        try:
            client = GenericClient(
                module='Test',
                url='http://localhost:5001',
                token='x'
            )
            client.call_func('return_non_list', [{}])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
