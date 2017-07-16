from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from swamp.utils import Singleton
from swamp import exception
from swamp import datasource

Base = declarative_base()


class DB(Singleton):
    _engine = None

    def __init__(self):
        if not self._engine:
            self._engine = create_engine('sqlite:///./sqlite.db', echo=True)

    def create_tables(self):
        Base.metadata.create_all(self._engine)

    def drop_tables(self):
        Base.metadata.drop_all(self._engine)

    @property
    def engine(self):
        return self._engine


def get_session():
    db = DB()
    session = Session(db.engine)
    return session


class DBMixin(object):

    def save(self):
        session = get_session()
        session.add(self)
        session.commit()

    @classmethod
    def get_all(cls):
        session = get_session()
        return session.query(cls).all()


class Device(Base, DBMixin):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    check_infos = relationship("CheckInfo")
    settings = relationship("DeviceSetting")

    def __repr__(self):
        return "<Device(name='%s')>" % self.name

    def __init__(self, name):
        self.name = name


class DeviceSetting(Base, DBMixin):
    __tablename__ = 'device_settings'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    key = Column(String)
    value = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    device = relationship("Device", back_populates="settings")

    def __repr__(self):
        return "<DeviceSetting(key='%s')>" % self.key


class CheckInfo(Base, DBMixin):
    __tablename__ = 'check_infos'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    created_at = Column(DateTime, default=datetime.now)
    data = Column(String)

    device = relationship("Device", back_populates="check_infos")

    def __init__(self, device_id, data=None):
        self.device_id = device_id
        self.data = data

    @classmethod
    def get_new(cls, device_id):
        adsys = datasource.get_ad_source()
        if adsys.test():
            data = adsys.get_data()
        else:
            raise exception.DataSourceGetError
        info = cls(device_id=device_id, data=data)
        info.save()
        return info
