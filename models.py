import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Landmark(Base):
    __tablename__ = 'landmark'

    id = Column(Integer, primary_key=True)
    coordinate = Column(String)
    name = Column(String)


class Route(Base):
    __tablename__ = 'base_route'

    id = Column(Integer, primary_key=True)
    is_finished = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    routing_point = relationship('RoutingPoint')


class RoutingPoint(Base):
    __tablename__ = 'routing_point'

    id = Column(Integer, primary_key=True)
    start_point = Column(String)
    end_point = Column(String)
    base_route = Column(Integer, ForeignKey('base_route.id'))
