from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task01(Base):
    __tablename__ = 'task01'

    def __repr__(self):
        return f"<Task01(" \
               f"id='{self.id}'," \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False)


class Task02(Base):
    __tablename__ = 'task02'

    def __repr__(self):
        return f"<Task02(" \
               f"id='{self.id}'," \
               f"r_type='{self.r_type}'," \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    r_type = Column(String(10), nullable=False)
    count = Column(Integer, nullable=False)


class Task03(Base):
    __tablename__ = 'task03'

    def __repr__(self):
        return f"<Task03(" \
               f"id='{self.id}'," \
               f"location='{self.location}'," \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(150), nullable=False)
    count = Column(Integer, nullable=False)


class Task04(Base):
    __tablename__ = 'task04'

    def __repr__(self):
        return f"<Task04(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'," \
               f"location='{self.location}'," \
               f"status='{self.status}'," \
               f"size='{self.size}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    location = Column(String(400), nullable=False)
    status = Column(String(3), nullable=False)
    size = Column(Integer, nullable=False)


class Task05(Base):
    __tablename__ = 'task05'

    def __repr__(self):
        return f"<Task05(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'," \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    count = Column(Integer, nullable=False)
