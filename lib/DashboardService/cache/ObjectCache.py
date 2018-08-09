import os
import itertools
import json
import apsw

from DashboardService.GenericClient import GenericClient
from DashboardService.ServiceUtils import ServiceUtils

class ObjectCache(object):
    def __init__(self, path=None, workspace_url=None, token=None):
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

        self.token = token
        self.conn = apsw.Connection(self.path)

    def initialize(self):
        self.create_schema()
 
    def create_schema(self):
        schema = '''
        drop table if exists cache;
        create table cache (
            workspace_id int not null,
            object_id int not null,
            timestamp int not null,

            value text,
             
            primary key (workspace_id, object_id, timestamp)
        );
        '''
        with self.conn:
            self.conn.cursor().execute(schema)
        
    def add_items(self, items):
        sql = '''
        insert or replace into cache (workspace_id, object_id, timestamp, value)
        values (?, ?, ?, ?)
        '''

        with self.conn:
            for wsid, objid, ts, value in items:
                self.conn.cursor().execute(sql, (wsid, objid, ts, value))

    def fetch_items(self, keys):
        rpc = GenericClient(
            module='Workspace',
            url=self.workspace_url,
            token=self.token
        )

        objects_to_get = []
        for wsid, objid in keys:
            objects_to_get.append({
                'wsid': int(wsid),
                'objid': int(objid)
            })
        [result] = rpc.call_func('get_object_info3', [{
            'objects': objects_to_get,
            'includeMetadata': 1,
            'ignoreErrors': 1
        }])

        return [ServiceUtils.obj_info_to_object(value) for value in result['infos']]

    def get_all_items(self):
        sql = '''
        select * from cache
        '''
        with self.conn:
            return self.conn.curosr().execute(sql).fetchall()

    # simply gets the specified keys
    def get_items(self, keys):
        temp_sql = '''
        create temporary table keys (
            wsid int,
            objid int,
            timestamp int,
            primary key (wsid, objid)
        );
        '''

        temp_sql2 = '''
        insert into keys (wsid, objid, timestamp) values (?, ?, ?)
        '''

        sql = '''
        select cache.*, keys.*
        from temp.keys
        left outer join cache
          on keys.wsid = cache.workspace_id and
             keys.objid = cache.object_id            
        '''

        with self.conn:
            self.conn.cursor().execute(temp_sql)
            for key in keys:
                # only use the wsid and objid
                self.conn.cursor().execute(temp_sql2, tuple(key))
            return self.conn.cursor().execute(sql).fetchall()

    # PUBLIC

    def get(self, key_specs):
        items_to_return = []
        items_to_fetch = []
        for wsid, objid, timestamp, value, key_wsid, key_objid, key_timestamp in self.get_items(key_specs):
            if wsid is None:
                items_to_fetch.append([key_wsid, key_objid])
            elif timestamp < (key_timestamp or 0):
                items_to_fetch.append([key_wsid, key_objid]) 
            else:
                items_to_return.append(json.loads(value))

        # Now fetch all of the missing objects and cache them
        if len(items_to_fetch) > 0:
            print('fetching... %s' % (len(items_to_fetch)))
            fetched_items = self.fetch_items(items_to_fetch)
            print('...fetched')
            items_to_update = []
            for object_info in fetched_items: 
                items_to_return.append(object_info)
                items_to_update.append([
                    object_info['wsid'], 
                    object_info['id'],
                    object_info['saveDateMs'],
                    json.dumps(object_info)
                ])
            self.add_items(items_to_update)

            # TODO: handle errors, but should not happen since this is 
            # driven by a set of workspaces + objects available to this
            # user. Still, other than artificial conditions due to testing, 
            # there are race conditions...
            # items_to_return.extend(items_to_update)

        # Now prepare the result items as an array in the same order as the
        # requested key specs.
        # return [items_to_return[key['cache_key']] for key in keys]
        # return as-is; the caller can sort if they wish.
        return sorted(
            items_to_return,
            key=lambda x: x.get('wsid')
        )

    # TODO: a method to harvest stale cache entries.
    # E.g. if an object is deleted or unshared, there is no way to reflect in the
    # passive cache; it will simply become unused.

    # TODO: switch to version and not timestamp??

    # def remove(self, obji):
    #     cache_key = self.make_cache_key([obji.workspace_id(), obji.object_id()])
    #     self.deleteone(cache_key)
