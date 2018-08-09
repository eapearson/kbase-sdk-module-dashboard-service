import json
import apsw
import os
import itertools
import time
import hashlib

from DashboardService.GenericClient import GenericClient
from DashboardService.Errors import ServiceError


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
    def __init__(self, path=None, user_profile_url=None):
        if path is None:
            raise ValueError('The "path" argument is required')
        if not isinstance(path, basestring):
            raise ValueError('The "path" argument must be a string')
        self.path = path

        if user_profile_url is None:
            raise ValueError('The "user_profile_url" argument is required')
        if not isinstance(user_profile_url, basestring):
            raise ValueError('The "user_profile_url" argument must be a string')
        self.user_profile_url = user_profile_url

        self.conn = apsw.Connection(self.path)

    def initialize(self):
        self.create_schema()

    def create_schema(self):
        alerts_schema = '''
        drop table if exists cache;
        create table cache (
            key text not null primary key,
            value text,
            size int not null,
            md5 blob not null
        );
        '''
        with self.conn:
            self.conn.cursor().execute(alerts_schema)

    # def load_all(self):
    #     sql = '''
    #     insert or replace into cache
    #     (key, value, size, md5)
    #     values
    #     (?, ?, ?, ?)
    #     '''

    #     start = time.time()
    #     profiles = self.fetch_profiles()
    #     fetched_at = time.time()
    #     fetched = fetched_at - start

    #     with self.conn:
    #         for profile in profiles:
    #             key = get_path(profile, ['user', 'username'])
    #             params = (key, json.dumps(profile))
    #             self.conn.cursor().execute(sql, params)
    #     added = time.time() - fetched_at

    # def sync1(self):
    #     sql = '''
    #     insert or replace into cache
    #     (key, value, size, md5)
    #     values
    #     (?, ?, ?, ?)
    #     '''

    #     profiles = self.fetch_profiles()

    #     with self.conn:
    #         for profile in profiles:
    #             key = get_path(profile, ['user', 'username'])
    #             value = json.dumps(profile)
    #             hasher = hashlib.md5()
    #             hasher.update(value)
    #             hash = hasher.digest()
    #             params = (key, value, len(value), buffer(hash))
    #             self.conn.cursor().execute(sql, params)


    def sync(self):
        temp_sql = '''
        create temporary table updater (
        key text not null primary key,
        value text not null,
        size int not null,
        md5 blob not null    
        )
        '''
        update_temp_sql = '''
        insert into updater
        (key, value, size, md5)
        values
        (?, ?, ?, ?)
        '''

        insert_sql = '''
        insert into cache
        (key, value, size, md5)
        select key, value, size, md5
        from updater where 
          not exists (select updater.key from cache where cache.key = updater.key)
        '''

        update_sql = '''
        with updates as (select * 
                            from updater a
                            join cache b
                                on a.key = b.key and
                                a.md5 != b.md5)
        update cache
        set (value, size, md5) = (select value, size, md5 from updates where updates.key = cache.key)
        where cache.key in (select key from updates)
        '''

        profiles = self.fetch_profiles()
        fetched_at = time.time()

        with self.conn:
            self.conn.cursor().execute(temp_sql)

            for profile in profiles:
                key = get_path(profile, ['user', 'username'])
                value = json.dumps(profile)
                hasher = hashlib.md5()
                hasher.update(value)
                hash = hasher.digest()
                params = (key, value, len(value), buffer(hash))
                self.conn.cursor().execute(update_temp_sql, params)

            self.conn.cursor().execute(insert_sql)
            self.conn.cursor().execute(update_sql)
            

    def fetch_profiles(self):
        rpc = GenericClient(
            module='UserProfile',
            url=self.user_profile_url,
            token=None
        )
        [users] = rpc.call_func('filter_users', [{
            'filter': ''
        }])

        # Annoying, but we need to turn around and get the full profiles now.

        # TODO: batches of 1000.

        usernames = [user['username'] for user in users]

        profiles = []

        batches, rem = divmod(len(usernames), 1000)

        for batch_number in range(0, batches + 1):
            if batch_number == batches:
                start = batch_number * 1000
                stop = start + rem
            else:
                start = batch_number*1000
                stop = (batch_number+1)*1000

            username_group = usernames[start:stop]
            [result] = rpc.call_func('get_user_profile', [
                username_group
            ])

            profiles.extend(result)

        return profiles

    # public interface

    def get(self, usernames):
        # TODO: handle usernames > 1000
        placeholders = ','.join(list('?' for _ in usernames))
        sql = '''
        select key, value
        from cache
        where key in (%s)
        ''' % (placeholders)

        profiles = []
        with self.conn:
            for key, value in self.conn.cursor().execute(sql, usernames).fetchall():
                profiles.append([key, json.loads(value)])
        return profiles
