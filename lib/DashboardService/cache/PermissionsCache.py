import itertools
import apsw
import json
import os

from DashboardService.GenericClient import GenericClient
from DashboardService.ServiceUtils import ServiceUtils


class PermissionsCache:
    def __init__(self, path=None, workspace_url=None, username=None, token=None):
        if path is None:
            raise ValueError('The "path" argument is required')
        if not isinstance(path, basestring):
            raise ValueError('The "path" argument must be a string')
        self.path = path

        if workspace_url is None:
            raise ValueError('The "workspace_url" argument is required')
        if not isinstance(workspace_url, basestring):
            raise ValueError('The "workspace_url" argument must be a string')
        self.workspace_url = workspace_url

        if token is not None:
            if not isinstance(token, basestring):
                raise ValueError('The "token" argument must be a string')
            self.token = token

        if username is not None:
            if not isinstance(username, basestring):
                raise ValueError('The "username" argument must be a string')
            self.username = username


    def connect(self):
        self.conn = apsw.Connection(self.path)
        # self.conn.execute('pragma journal_mode=wal;')

    def connect_cursor(self):
        self.connect()
        return self.conn.cursor()

    def disconnect(self):
        cursor = self.conn.cursor()
        cursor.execute('pragma optimize')
        self.conn.close()

    def initialize(self):
        self.connect()
        self.create_schema()
        self.disconnect()

    def create_schema(self):
            # timestamp int not null,
        schema = '''
        drop table if exists cache;
        create table cache (
            workspace_id int not null,
            username text not null,

            value text,
             
            primary key (workspace_id, username)
        )    
        '''
        cursor = self.conn.cursor()
        cursor.execute(schema)
        cursor.close()

    def add_items(self, items):
        sql = '''
        insert or replace into cache (workspace_id, username, value)
        values (?, ?, ?)
        '''

        self.connect()

        with self.conn:
            for wsid, username, value in items:
                self.conn.cursor().execute(sql, (wsid, username, json.dumps(value)))

        self.disconnect()

    def get_all_items(self):
        sql = '''
        select * from cache
        '''
        cursor = self.connect_cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        self.disconnect()
        return result

    def fetch_items(self, keys):
        ws_client = GenericClient(
            module='Workspace',
            url=self.workspace_url,
            token=self.token
        )
        workspaces_for_perms = [{'id': wsid} for (wsid, _username) in keys]
        [workspaces_permissions] = ws_client.call_func('get_permissions_mass', [{
            'workspaces': workspaces_for_perms
        }])

        # Adjust the permissions:
        # - filter out the public "shared user"
        perms = []
        for permissions in workspaces_permissions['perms']:
            if permissions is None:
                perms.append(None)
            else:
                perms.append([ [k,v] for k,v in permissions.iteritems() if k != '*'])

        # return a list of [workspace_id, perms]
        ret = []
        for key, value in itertools.izip(keys, perms):
            ret.append([key[0], value])
        return ret

    # # public interface

    def get_items(self, keys):
        temp_sql = '''
        create temporary table keys (
            wsid int,
            username text
        );
        '''

        temp_sql2 = '''
        insert into keys (wsid, username) values (?, ?)
        '''

        sql = '''
        select cache.*, keys.*
        from keys
        left outer join cache
          on keys.wsid = cache.workspace_id and
             keys.username = cache.username            
        '''

        cursor = self.connect_cursor()

        cursor.execute(temp_sql)
        for key in keys:
            # only use the wsid and objid
            cursor.execute(temp_sql2, tuple(key))

        cursor.execute(sql)

        result = cursor.fetchall()

        cursor.close()
        self.disconnect()   

        return result

    def get(self, workspaces):
        cache_keys = [[ws, self.username] for ws in workspaces]
        
        items_to_return = []
        items_to_fetch = []
        for (wsid, username, value, key_wsid, key_username) in self.get_items(cache_keys):
            if wsid is None:
                items_to_fetch.append([key_wsid, key_username])
            else:
                items_to_return.append([wsid, json.loads(value)])

        if (len(items_to_fetch)):
            fetched = self.fetch_items(items_to_fetch)
            items_to_add = [[wsid, self.username, perms] for [wsid, perms] in fetched]
            self.add_items(items_to_add)
            items_to_return.extend(fetched)

        return [v for k,v in sorted(items_to_return, key=lambda x: x[0])]

    # def remove(self, wsi):
    #     cache_key = self.make_cache_key([self.username, wsi.id()])
    #     self.deleteone(cache_key)

    def refresh_items(self, wsids):
        keys = [[wsid, self.username] for wsid in wsids]
        items_to_add = []
        for (wsid, value) in self.fetch_items(keys):
            items_to_add.append([wsid, self.username, value])

        self.add_items(items_to_add)
