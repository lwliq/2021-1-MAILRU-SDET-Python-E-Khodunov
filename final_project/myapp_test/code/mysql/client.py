import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session, class_mapper
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect, event
from sqlalchemy.pool import NullPool

from mysql.models import Base, User
from utils.decorators import wait


class MysqlClient:

    def __init__(self, user, password, db_name, db_host):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = db_host
        self.port = 3306

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''

        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}',
            encoding='utf8',
            poolclass=NullPool
        )
        self.connection = wait(
            method=self.engine.connect,
            error=OperationalError,
            timeout=50,
            interval=0.5,
        )

        self.session = sessionmaker(bind=self.connection.engine,
                                    autoflush=True
                                    )()

    def close(self):
        self.connection.close()
        self.engine.dispose()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def recreate_db(self, username):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)
        query = f"GRANT ALL ON {self.db_name}.* TO {username}@'%%'"
        self.execute_query(query, fetch=False)
        self.execute_query('FLUSH PRIVILEGES', fetch=False)
        self.close()

    def drop_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.close()

    def create_app_table(self):
        self.connect()
        if not inspect(self.engine).has_table('test_users'):
            Base.metadata.tables['test_users'].create(self.engine)
        self.close()

    def add(self, model):
        self.session.add(model)
        self.session.commit()

    def get_user(self, username):
        return self.session.query(User).filter_by(username=username).first()

    def user_exists(self, username):
        return self.session.query(User).filter_by(username=username).first() is not None

    def expire_all(self):
        self.session.expire_all()
        self.session.commit()

