import apsw
import json

print 'hi'

db = apsw.Connection('test.db')

cursor = db.cursor()
schema_sql = '''
drop table if exists test;
create table test (
    workspace_id int not null,
    username text not null,

    value text,
        
    primary key (workspace_id, username)
);
'''
cursor.execute(schema_sql)

insert_sql = '''
insert into test (workspace_id, username, value)
values (?, ?, ?)
'''

text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed consectetur nulla vulputate tellus lacinia, vitae pharetra leo maximus. Nullam fermentum, nulla nec luctus porttitor, sapien neque finibus enim, vitae ultrices elit sapien eu sapien. Nunc non vehicula diam. Curabitur magna dui, pellentesque non consectetur maximus, sagittis non purus. Duis venenatis nisi ac leo malesuada, in tempor libero ullamcorper. Donec imperdiet mi at diam interdum, fermentum egestas sem hendrerit. Donec eget ante eget lorem tincidunt porttitor. Fusce quis scelerisque ipsum, vitae feugiat nibh. Praesent sit amet quam ultricies, aliquam sem quis, laoreet ligula. Nullam convallis tellus sapien, ac finibus mi tincidunt eget.

Aenean vel dolor accumsan, interdum mi a, sagittis velit. Quisque quis mi porta arcu viverra tempus. Suspendisse tincidunt neque ac posuere luctus. Vestibulum rutrum, ante eget interdum dapibus, tellus quam rutrum sapien, id faucibus mauris nisl ut sapien. Duis feugiat, purus et ultrices dictum, magna turpis elementum dolor, eu consequat justo quam in nulla. Nunc eget rutrum ipsum. Vestibulum scelerisque consequat sodales. Nunc quis dolor nec metus tempor efficitur nec pretium libero. Ut sed ultricies magna. Vivamus vestibulum lacus a lectus laoreet, sed tincidunt nunc tempus. Curabitur suscipit turpis sed ornare interdum. Maecenas ut felis leo. Integer mollis nisl ac justo tempus, in condimentum sapien iaculis.

Pellentesque posuere velit tortor, eget finibus felis eleifend vitae. Donec non commodo nulla. Mauris quis ullamcorper arcu, sed auctor arcu. Nulla nisl purus, pulvinar vitae dolor faucibus, consequat rutrum leo. Cras lobortis id urna quis aliquet. Fusce id neque tincidunt, fermentum nunc vel, congue eros. Aliquam lacus nunc, malesuada quis ipsum a, mollis dignissim leo. Vivamus sit amet metus ac dolor accumsan convallis non vel ipsum. Sed fringilla, turpis sit amet mollis laoreet, tellus mi suscipit velit, sed dictum felis enim vel quam. Vestibulum cursus ante eget rutrum faucibus.

Praesent consequat orci eros, nec faucibus orci imperdiet a. Suspendisse cursus aliquam facilisis. Mauris non dapibus lectus, ac porta elit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut congue purus ac mauris accumsan, vitae mollis nisi pretium. Etiam congue, purus vitae consequat ultricies, magna nunc elementum diam, ac porta turpis ante a ex. Nulla auctor consequat mi ac tempor. Proin pulvinar lectus felis, quis vulputate eros dignissim sit amet. Nullam sodales nisi vel purus pretium vestibulum. Phasellus a nibh eu odio commodo tristique eu ut orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur maximus nibh in congue eleifend. Phasellus fringilla sit amet mi at maximus. In hac habitasse platea dictumst.

Donec eget aliquet metus. Maecenas dictum sit amet augue sit amet ultrices. Sed commodo, lacus consectetur dignissim accumsan, erat magna cursus nibh, imperdiet vestibulum risus metus et lorem. Mauris at dolor commodo, lobortis dolor sit amet, ullamcorper lacus. Aenean tempus velit eget facilisis rhoncus. Quisque in libero quam. Aliquam nec tempus neque, in pharetra orci. Integer ante felis, dignissim id accumsan at, finibus at nunc. Nam elementum eget felis vitae interdum. Vestibulum dignissim mollis magna, eget pellentesque lorem egestas a. Pellentesque non sem erat. Nulla sed fringilla dolor, quis porttitor elit.
'''

# cursor.execute('begin transaction')
# for i in range(0,1000):
#     cursor.execute(insert_sql, (i, 'eapearson', json.dumps(text)))
# cursor.execute('commit')

gen = ((i, 'eapearson', json.dumps(text)) for i in xrange(0,1000))

with db:
    db.cursor().executemany(insert_sql, gen)