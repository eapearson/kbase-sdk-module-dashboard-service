import requests
import json


class GenericClient(object):
    def __init__(self, module=None, url=None, token=None):
        if module is None:
            raise ValueError('The "module" argument is required')
        if url is None:
            raise ValueError('The "url" argument is required')

        self.module = module
        self.token = token
        self.url = url

    def call_func(self, func_name, params):
        call_params = {
            'id': 'uniquestring',
            'method': self.module + '.' + func_name,
            'version': '1.1',
            'params': params
        }
        header = {
            'Content-Type': 'application/json'
        }
        if self.token:
            header['Authorization'] = self.token

        r = requests.post(self.url, headers=header, data=json.dumps(call_params), timeout=60)
        if r.headers['content-type'].startswith('application/json'):
            result = r.json()
            return result.get('result'), result.get('error')

        r.raise_for_status()
        raise ValueError('Invalid response; not json, not an error status')
        
