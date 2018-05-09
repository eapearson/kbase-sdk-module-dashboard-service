import itertools
import json
import bsddb3
from DashboardService.GenericClient import GenericClient
from DashboardService.ServiceUtils import ServiceUtils


class ObjectCache(object):
    def __init__(self, path=None, url=None, token=None):
        if path is None:
            raise ValueError('the "path" argument is required')
        self.path = path

        if url is None:
            raise ValueError('the "url" argument is required')
        self.url = url

        self.token = token

        self.db = bsddb3.db.DB()

    def start(self):
        self.db.open(self.path, None, bsddb3.db.DB_HASH)

    def stop(self):
        self.db.close()

    def initialize(self):
        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_CREATE)
        # self.populate_cache()
        self.db.close()
        
    def setone(self, key, value):
        cache_key = self.make_cache_key(key)
        self.db.put(cache_key.encode('utf8'), json.dumps(value).encode('utf8'))

    def fetch(self, keys):
        rpc = GenericClient(
            module='Workspace',
            url=self.url,
            token=self.token
        )

        objects_to_get = []
        for (wsid, objid, _timestamp) in keys:
            objects_to_get.append({
                'wsid': int(wsid),
                'objid': int(objid)
            })
        result, error = rpc.call_func('get_object_info3', [{
            'objects': objects_to_get,
            'includeMetadata': 1,
            'ignoreErrors': 1
        }])
        if error:
            raise ValueError(error)

        return [ServiceUtils.objectInfoToObject(value) for value in result[0]['infos']]

    # simply gets the specified keys
    def get_items(self, keys):
        result = []
        for key in keys:
            cache_key = self.make_cache_key(key)
            value = self.db.get(cache_key.encode('utf8'))

            if value is not None:
                result.append((cache_key, json.loads(value.decode('utf8'))))
            else:
                result.append((cache_key, None))
        return result

    def make_key(self, key):
        return '.'.join(list(
            map(
                lambda k: str(k),
                key
            )))

    def make_cache_key(self, key):
        return '.'.join([str(p) for p in key])

    # PUBLIC

    def get(self, keys):
        cache_keys = [self.make_cache_key(key) for key in keys]
        items_to_return = dict()
        for (cache_key, value) in self.get_items(keys):
            if value is not None:
                items_to_return[cache_key] = value
            # else:
            #     items_to_return[cache_key] = None
        if len(items_to_return) != len(keys):
            missing_cache_keys = set(cache_keys).difference(items_to_return.keys())
            missing_keys = []
            for missing_key in missing_cache_keys:
                key = missing_key.split('.')
                missing_keys.append([int(p) for p in key])
            fetched = self.fetch(missing_keys)
            for key, value in itertools.izip(missing_keys, fetched):
                self.setone(key, value)
                cache_key = '.'.join([str(p) for p in key])
                items_to_return[cache_key] = value

        return [items_to_return.get(cache_key2, None) for cache_key2 in cache_keys]
