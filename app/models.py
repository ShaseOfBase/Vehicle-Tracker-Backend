import json
from flask_sqlalchemy import SQLAlchemy
import uuid
from . import db
from flask_appbuilder import Model
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, backref


class RoutePoint(Model):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    route_id = Column(Integer, ForeignKey('route.id'), nullable=False)

    def __repr__(self):
        return f'rp_{self.id}'

    def to_dict(self):
        clean_dict = self.__dict__.copy()
        clean_dict.pop('_sa_instance_state')
        return clean_dict


class Route(Model):
    id = Column(Integer, primary_key=True)
    label = Column(String(128), nullable=False)
    route_points = relationship('RoutePoint', backref='routes')
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), nullable=False)

    def __repr__(self):
        return self.label

    def to_dict(self):
        clean_dict = self.__dict__.copy()
        clean_dict.pop('_sa_instance_state')
        return clean_dict


class Vehicle(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    routes = relationship('Route', backref='vehicle')
    user_id = Column(String(64), ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}'

    def to_dict(self):
        clean_dict = self.__dict__.copy()
        clean_dict.pop('_sa_instance_state')
        return clean_dict


class User(Model):
    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(128), unique=True)
    password = Column(String(128))
    vehicles = relationship('Vehicle', backref='user')

    def __repr__(self):
        return f'{self.name}'

    def to_dict(self):
        clean_dict = self.__dict__.copy()
        clean_dict.pop('_sa_instance_state')
        clean_dict.pop('password')
        return clean_dict
