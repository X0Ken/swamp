import json
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

from swamp import exception
from swamp import log
from swamp.data_source import factory
from swamp.utils import Singleton

logger = log.get_logger()
Base = declarative_base()


class DB(Singleton):
    _engine = None
    _session = None

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

    @property
    def session(self):
        if self._session:
            return self._session
        else:
            logger.debug("Create new DB session")
            self._session = Session(self._engine)
            return self._session


class DBMixin(object):
    def save(self):
        session = DB().session
        session.add(self)
        session.commit()
        session.refresh(self)

    @classmethod
    def get_all(cls):
        session = DB().session
        return session.query(cls).all()

    def destroy(self):
        session = DB().session
        session = session.object_session(self)
        session.delete(self)
        session.commit()


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

    @classmethod
    def name_exist(cls, name):
        session = Session(DB().engine)
        return session.query(cls).filter_by(name=name).all()


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

    def __str__(self):
        return str(self.created_at)[:16]

    @classmethod
    def get_new(cls, device_id):
        adsys = factory.get_ad_source()
        if adsys.test():
            data = adsys.get_data()
        else:
            raise exception.DataSourceGetError
        info = cls(device_id=device_id, data=json.dumps(data))
        info.save()
        return info

    @classmethod
    def get_all_by_device(cls, device_id):
        session = Session(DB().engine)
        return session.query(cls).filter_by(device_id=device_id).all()
