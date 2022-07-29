from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def db_connector():
    params = {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'username': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': 3306,
        'db_name': 'scms'
    }
    eng = create_engine(
        # dialect+driver://username:password@host:port/database
        "{dialect}+{driver}://{username}:{password}@{host}:{port}/{db_name}".format(**params),
        future=True,
        # echo=True

    # 绑定引擎
    DBSession = sessionmaker(bind=eng)

    return DBSession


params = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3306,
    'db_name': 'scms'
}

my_engine = create_engine(
    # dialect+driver://username:password@host:port/database
    "{dialect}+{driver}://{username}:{password}@{host}:{port}/{db_name}".format(**params),
    future=True,
    # echo=True
)
