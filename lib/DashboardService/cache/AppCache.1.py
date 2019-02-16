import json
import bsddb3
from DashboardService.GenericClient import GenericClient

class ServiceError(Exception):
    def __init__(self, name=None, code=None, message=None, data=None, error=None):
        super(ServiceError, self).__init__(message)
        self.name = name
        self.code = code
        self.message = '' if message is None else message
        self.data = data or error or ''
        # data = JSON RPC 2.0, error = 1.1

    def __str__(self):
        return self.name + ': ' + str(self.code) + '. ' + self.message + \
            '\n' + self.data

class AppCache:
    def __init__(self, path=None, narrative_method_store_url=None):
        if path is None:
            raise ValueError('The "path" argument is required')
        if not isinstance(path, str):
            raise ValueError('The "path" argument must be a string')
        self.path = path

        if narrative_method_store_url is None:
            raise ValueError('The "narrative_method_store_url" argument is required')
        if not isinstance(narrative_method_store_url, str):
            raise ValueError('The "narrative_method_store_url" argument must be a string')
        self.narrative_method_store_url = narrative_method_store_url
    
        # self.make()
        

    def make(self):
        self.db = bsddb3.db.DB()

    def close(self):
        self.db.close()

    def start(self):
        print('+OPEN1')
        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_RDONLY)
        print('-OPEN1')

    def stop(self):
        self.db.close()

    def initialize(self):
        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_CREATE)
        self.populate_cache()
        self.db.close()

    def create(self):
        print('+OPEN3')
        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_CREATE)
        # self.db.close()
        print('-OPEN3')

    def remove(self):
        try:
            self.db.remove(self.path)
        except bsddb3.db.DBNoSuchFileError as err:
            pass

    def load_for_tag(self, tag):
        rpc = GenericClient(
            module='NarrativeMethodStore',
            url=self.narrative_method_store_url,
            token=None
        )
        result, error = rpc.call_func('list_methods', [{
            'tag': tag
        }])
        if error:
            raise ServiceError(**error)

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
