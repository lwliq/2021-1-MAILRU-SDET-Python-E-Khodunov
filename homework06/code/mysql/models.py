from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RequestsCount(Base):
    __tablename__ = 'requests_count'

    def __repr__(self):
        return f"<Task01(" \
               f"id='{self.id}'," \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False)


class RequestsCountByType(Base):
    __tablename__ = 'requests_count_by_type'

    def __repr__(self):
        return f"<Task02(" \
               f"id='{self.id}'," \
               f"r_type='{self.r_type}'," \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    r_type = Column(String(10), nullable=False)
    count = Column(Integer, nullable=False)


class Top10MostFrequentLocations(Base):
    __tablename__ = 'top_10_most_frequent_locations'

    def __repr__(self):
        return f"<Top10MostFrequentLocations(" \
               f"id='{self.id}'," \
               f"location='{self.location}'," \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(150), nullable=False)
    count = Column(Integer, nullable=False)


class Top5LocationsBySize(Base):
    __tablename__ = 'top_5_locations_by_size'

    def __repr__(self):
        return f"<Top5LocationsBySize(" \
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


class Top5MostFrequentIps(Base):
    __tablename__ = 'top_5_most_frequent_ips'

    def __repr__(self):
        return f"<Top5MostFrequentIps(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'," \
               f"count='{self.count}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    count = Column(Integer, nullable=False)
