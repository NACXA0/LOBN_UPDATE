import global_config
import uuid, itertools, time, datetime, random, ast, calendar
from sqlmodel import Session, select, update, func, or_, outerjoin, and_, exists, not_
from LOBN_UPDATE.DataBase_function.database import engine
from LOBN_UPDATE.DataBase_function.models import config_page, config_system, user, org, org_map_org2identity, identity
from uuid_extensions import uuid7, uuid7str

def print_info():
    print('UUID7:', uuid7str())
    print('当前时间Datetime:', datetime.datetime.now())
    print(uuid7(0))


def test_db():
    with Session(engine) as session:
        command = select(config_system)
        info_data = session.exec(command).first()
        print('WWWWWWWWW', type(info_data), info_data)


def test_redis():
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')
    value = r.get('foo')
    print('Redis value for key "foo":', value.decode('utf-8'))

if __name__ == '__main__':
    print_info()
    #test_db()
    test_redis()
