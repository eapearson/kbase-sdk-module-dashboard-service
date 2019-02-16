import json
import apsw

from DashboardService.GenericClient import GenericClient
from DashboardService.Errors import ServiceError

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
        self.conn = apsw.Connection(self.path)

    def initialize(self):
        self.create_schema()
        self.load_all()

    def create_schema(self):
        schema = '''
        drop table if exists cache;
        create table cache (
            key text not null primary key,
            tag text not null,
            value text
        )    
        '''
        with self.conn:
            self.conn.cursor().execute(schema)
        
    def load_for_tag(self, tag):
        rpc = GenericClient(
            module='NarrativeMethodStore',
            url=self.narrative_method_store_url,
            token=None
        )
        [result] = rpc.call_func('list_methods', [{
            'tag': tag
        }])

        to_add = []
        for app in result:
            to_add.append((app['id'], app))
        self.add_many(to_add, tag)

    def load_all(self):
        # Note that these are applied as "insert or replace", so 
        # order is important.
        self.load_for_tag('dev')
        self.load_for_tag('beta')
        self.load_for_tag('release')

    def add_many(self, to_add, tag):
        sql = '''
        insert or replace into cache
        (key, tag, value)
        values
        (?, ?, ?)
        '''
        with self.conn:
            for key, value in to_add:
                params = (key, tag, json.dumps(value))
                self.conn.cursor().execute(sql, params)


    def get(self, app_id):
        sql = '''
        select key, tag, value
        from cache
        where key = ?
        '''
        params = (app_id,)
        with self.conn:
            record = self.conn.cursor().execute(sql, params).fetchone()

        if not record:
            return None, None

        (_key, tag, value_as_string) = record

        value = json.loads(value_as_string)

        return tag, value

    def get_items(self, app_ids):
        temp_sql = '''
        create temporary table keys (
            key text primary key
        );
        '''

        temp_sql2 = '''
        insert into keys (key) values (?)
        '''

        sql = '''
        select cache.*, keys.*
        from temp.keys
        left outer join cache
          on keys.key = cache.key            
        '''

        with self.conn:
            self.conn.cursor().execute(temp_sql)
            for app_id in app_ids:
                # nb trailing comma to force tuple to be, er, a tuple
                self.conn.cursor().execute(temp_sql2, (app_id,))
            apps = self.conn.cursor().execute(sql).fetchall()
    
        retval = []
        for (key, tag, value_as_string, temp_key) in apps:
            if value_as_string is None:
                value_as_json = None
            else:
                value_as_json = json.loads(value_as_string)

            retval.append((key, tag, value_as_json, temp_key))

        return retval
