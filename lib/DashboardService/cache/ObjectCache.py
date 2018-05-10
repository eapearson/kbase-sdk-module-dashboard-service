import os
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
        if os.path.isfile(self.path):
            # raise ValueError('The cache file indicated by "path" already exists: ' + self.path)
            os.remove(self.path)

        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_CREATE)
        # self.populate_cache()
        self.db.close()
        
    def setone(self, cache_key, value, timestamp):
        # cache_key = self.make_cache_key(key)
        record = {
            'value': value,
            'timestamp': timestamp
        }
        self.db.put(cache_key.encode('utf8'), json.dumps(record).encode('utf8'))

    def deleteone(self, cache_key):
        self.db.delete(cache_key)

    def fetch(self, keys):
        rpc = GenericClient(
            module='Workspace',
            url=self.url,
            token=self.token
        )

        objects_to_get = []
        for key in keys:
            (wsid, objid) = key['key']
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
            # cache_key = self.make_cache_key(key['cache_key'])
            value = self.db.get(key['cache_key'].encode('utf8'))

            if value is not None:
                result.append((key, json.loads(value.decode('utf8'))))
            else:
                result.append((key, None))
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

    def get(self, key_specs):
        keys = []
        for (workspace_id, object_id, timestamp) in key_specs:
            key = [workspace_id, object_id]
            keys.append({
                'key': key,
                'cache_key': self.make_cache_key(key),
                'timestamp': timestamp})

        # cache_keys = [self.make_cache_key(key_spec['key']) for key_spec in key_specs]
        #
        # Fetch all narrative objects in the cache, building a list of missing
        # or expired items.
        # Expiratino is defined as the last modification timestamp of the given
        # search key being greater than the cached one.
        #
        items_to_return = dict()
        items_to_fetch = []
        for (key, record) in self.get_items(keys):
            if record is None:
                items_to_fetch.append(key)
                # items_to_return[cache_key] = value
            elif record['timestamp'] < key['timestamp']:
                self.deleteone(key['cache_key'])
                items_to_fetch.append(key)
            else:
                items_to_return[key['cache_key']] = record['value']

        # Now fetch all of the missing objects and cache them
        if len(items_to_fetch) > 0:
            fetched = self.fetch(items_to_fetch)
            for key, value in itertools.izip(items_to_fetch, fetched):
                self.setone(key['cache_key'], value, key['timestamp'])
                items_to_return[key['cache_key']] = value

        # Now prepare the result items as an array in the same order as the
        # requested key specs.
        return [items_to_return[key['cache_key']] for key in keys]

        # if len(items_to_return) != len(keys):
        #     missing_cache_keys = set(cache_keys).difference(items_to_return.keys())
        #     missing_keys = []
        #     for missing_key in missing_cache_keys:
        #         key = missing_key.split('.')
        #         missing_keys.append([int(p) for p in key])
        #     fetched = self.fetch(missing_keys)
        #     for key, value in itertools.izip(missing_keys, fetched):
        #         self.setone(key, value)
        #         cache_key = '.'.join([str(p) for p in key])
        #         items_to_return[cache_key] = value

        # return [items_to_return.get(cache_key2, None) for cache_key2 in cache_keys]

    def remove(self, obji):
        cache_key = self.make_cache_key([obji.workspace_id(), obji.object_id()])
        self.deleteone(cache_key)
