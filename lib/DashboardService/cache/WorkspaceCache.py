import itertools
import bsddb3
import json
import os
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


class WorkspaceCache:
    def __init__(self, path=None, url=None, token=None):
        if path is None:
            raise ValueError('The "path" argument is required')
        parent_dir = os.path.dirname(path)
        if not os.path.isdir(parent_dir):
            raise ValueError('The "path" parent directory does not exist: ' + parent_dir)

        self.path = path

        if url is None:
            raise ValueError('The "url" argument is required')
        self.url = url

        # if token is None:
        #     raise ValueError('The "token" argument is required')
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

    def fetch(self, keys):
        ws_client = GenericClient(
            module='Workspace',
            url=self.url,
            token=self.token
        )
        workspaces_for_perms = [{'id': wsid} for (wsid, _ts) in keys]
        result, error = ws_client.call_func('get_permissions_mass', [{
            'workspaces': workspaces_for_perms
        }])
        if error:
            raise ValueError(error)
        workspaces_permissions = result[0]

        # Adjust the permissions:
        # - filter out the public "shared user"
        perms = []
        for permissions in workspaces_permissions['perms']:
            if permissions is None:
                perms.append(None)
            else:
                perms.append(list(
                    filter(
                        lambda p: p['username'] != '*',
                        map(
                            lambda (username, perm): {'username': username, 'perm': perm},
                            permissions.iteritems()
                        )
                    )
                ))
        return perms

    # public interface

    def get_items(self, keys):
        result = []
        for cache_key in keys:
            # cache_key = self.make_cache_key(key)
            value = self.db.get(cache_key.encode('utf8'))

            if value is not None:
                result.append((cache_key, json.loads(value.decode('utf8'))))
            else:
                result.append((cache_key, None))
        return result

    def make_cache_key(self, key):
        return '.'.join([str(p) for p in key])

    def setone(self, cache_key, value):
        # cache_key = self.make_cache_key(key)
        self.db.put(cache_key.encode('utf8'), json.dumps(value).encode('utf8'))

    def get(self, workspaces):
        cache_keys = [self.make_cache_key([ws['id'], ws['modDateMs']]) for ws in workspaces]
        items_to_return = dict()
        for (cache_key, value) in self.get_items(cache_keys):
            if value is not None:
                items_to_return[cache_key] = value
        if len(items_to_return) != len(cache_keys):
            missing_cache_keys = set(cache_keys).difference(items_to_return.keys())
            # TODO: make more compact
            missing_keys = [[int(p) for p in k.split('.')] for k in missing_cache_keys]
            # missing_keys = []
            # for missing_key in missing_cache_keys:
            #     # TODO: avoid packing and unpacking the key...
            #     # maybe keep as a struct with cache_key, key?
            #     key = missing_key.split('.')
            #     missing_keys.append([int(p) for p in key])
            fetched = self.fetch(missing_keys)
            for key, value in itertools.izip(missing_keys, fetched):
                cache_key = self.make_cache_key(key)
                self.setone(cache_key, value)
                items_to_return[cache_key] = value

        # TODO: don't refetch, but merge together the previously db-fetched and 
        # newly service-fetched.
        return [items_to_return.get(cache_key2, None) for cache_key2 in cache_keys]
