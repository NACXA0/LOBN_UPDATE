
import rxconfig
import uuid, itertools, time, datetime, random, ast, calendar
from sqlmodel import Session, select, update, func, or_, outerjoin, and_, exists, not_
from LOBN_UPDATE.DataBase_function.database import engine
from LOBN_UPDATE.DataBase_function.models import user, org, org_map_org2identity, identity
from uuid_extensions import uuid7, uuid7str

def print_info():
    print('UUID7:', uuid7str())
    print('当前时间Datetime:', datetime.datetime.now())



def test_db():
    with Session(engine) as session:
            # 1. 找出中间表所有拥有的基地
            command = select(org_base)
            info_data = session.exec(command).first()
            print('WWWWWWWWW', type(info_data), info_data)


if __name__ == '__main__':
    print_info()
