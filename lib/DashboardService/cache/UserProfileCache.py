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


class UserProfileCache:
    def __init__(self, path=None, url=None):
        if path is None:
            raise ValueError('The "path" argument is required')
        parent_dir = os.path.dirname(path)
        if not os.path.isdir(parent_dir):
            raise ValueError('The "path" parent directory does not exist: ' + parent_dir)
        
        self.path = path

        if url is None:
            raise ValueError('The "url" argument is required')
        self.url = url

        self.db = bsddb3.db.DB()

    def start(self):
        print('opening user profile cache')
        print(self.path)
        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_RDONLY)

    def stop(self):
        self.db.close()

    def initialize(self):
        print('opening user profile cache')
        print(self.path)
        if os.path.isfile(self.path):
            # raise ValueError('The cache file indicated by "path" already exists: ' + self.path)
            os.remove(self.path)
        
        self.db.open(self.path, None, bsddb3.db.DB_HASH, bsddb3.db.DB_CREATE)
        self.populate_cache()
        self.db.close()

    def populate_cache(self):
        profiles = self.fetch_profiles()
        for profile in profiles:
            key = get_path(profile, ['user', 'username'])
            # realname = get_path(profile, ['user', 'realname'])
            # avatarOption = get_path(profile, ['profile', 'userdata', 'avatarOption'])
            # gravatarDefault = get_path(profile, ['profile', 'userdata', 'gravatarDefault'])
            # gravatarHash = get_path(profile, ['profile', 'synced', 'gravatarHash'])
            # record = {
            #     'username': key,
            #     'realname': realname,
            #     'avatarOption': avatarOption,
            #     'gravatarDefault': gravatarDefault,
            #     'gravatarHash': gravatarHash
            # }

            self.db.put(key.encode('utf8'), json.dumps(profile).encode('utf8'))

    def fetch_profiles(self):
        rpc = GenericClient(
            module='UserProfile',
            url=self.url,
            token=None
        )
        result, error = rpc.call_func('filter_users', [{
            'filter': ''
        }])
        if error:
            raise ValueError(error)

        users = result[0]

        # Annoying, but we need to turn around and get the full profiles now.

        usernames = [user['username'] for user in users]
        result, error = rpc.call_func('get_user_profile', [
            usernames
        ])
        if error:
            raise ValueError(error)

        return result[0]

    # public interface

    def get(self, usernames):
        result = []
        for username in usernames:
            value = self.db.get(username.encode('utf8'))

            if value is not None:
                result.append(json.loads(value.decode('utf8')))
            else:
                result.append(None)
        return result
