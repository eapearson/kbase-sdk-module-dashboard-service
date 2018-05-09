import json
import bsddb3
from DashboardService.GenericClient import GenericClient


def get_path(from_dict, path):
    current_dict = from_dict
    for el in path:
        if not isinstance(current_dict, dict):
            return None
        if el not in current_dict:
            return None
        current_dict = current_dict[el]
    return current_dict


class AppCache:
    def __init__(self, path=None, url=None):
        if path is None:
            raise ValueError('The "path" argument is required')
        if not isinstance(path, basestring):
            raise ValueError('The "path" argument must be a string')
        self.path = path

        if url is None:
            raise ValueError('The "url" argument is required')
        self.url = url
        self.db = bsddb3.db.DB()

    def start(self):
        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_RDONLY)

    def stop(self):
        self.db.close()

    def initialize(self):
        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_CREATE)
        self.populate_cache()
        self.db.close()

    def load_for_tag(self, tag):
        rpc = GenericClient(
            module='NarrativeMethodStore',
            url=self.url,
            token=None
        )
        result, error = rpc.call_func('list_methods', [{
            'tag': tag
        }])
        if error:
            raise ValueError(error)

        for app in result[0]:
            key = app['id']
            if not self.db.exists(key.encode('utf8')):
                self.db.put(key.encode('utf8'), json.dumps(app).encode('utf8'))

    def populate_cache(self):
        self.load_for_tag('release')
        self.load_for_tag('beta')
        self.load_for_tag('dev')      

    # public interface

    def get(self, app_id): 
        value = self.db.get(app_id.encode('utf8'))

        if value is not None:
            return (None, json.loads(value.decode('utf8')))
        else:
            return (None, None)
