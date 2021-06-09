from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'test_users'

    def __repr__(self):
        return f"<User(" \
               f"id='{self.id}'," \
               f"username='{self.username}',"\
               f"password='{self.password}'," \
               f"email='{self.email}'," \
               f"access='{self.access}'," \
               f"active='{self.active}'," \
               f"start_active_time='{self.start_active_time}'," \
               f")>"

    id = Column(Integer, primary_key=True)
    username = Column(String(16), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(SmallInteger, nullable=True)
    active = Column(SmallInteger, nullable=True)
    start_active_time = Column(DateTime, nullable=True)


class VKUser(Base):
    __tablename__ = 'vk_users'

    def __repr__(self):
        return f"<VK_User(" \
               f"id='{self.id}'," \
               f"username='{self.username}'," \
               f"vk_id='{self.vk_id}'," \
               f")>"

    id = Column(Integer, primary_key=True)
    username = Column(String(16), nullable=False)
    vk_id = Column(String(200), nullable=False)

