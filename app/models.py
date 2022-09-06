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
    long = Column(Float)
    route_id = Column(Integer, ForeignKey('route.id'), nullable=False)

    def __repr__(self):
        return f'{self.timestamp} - {self.lat}:{self.long}'


class Route(Model):
    id = Column(Integer, primary_key=True)
    route_points = relationship('RoutePoint', backref='routes')
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), nullable=False)

    def __repr__(self):
        return f'route {self.id} - rp count: {len(self.route_points)}'

    def to_dict(self):
        return json.dumps(
            {'id': self.id,
             'route_points': self.route_points,
             'vehicle_id': self.vehicle_id}
        )


class Vehicle(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    routes = relationship('Route', backref='vehicle')
    user_id = Column(String(64), ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}'


class User(Model):
    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(128), unique=True)
    password = Column(String(128))
    vehicles = relationship('Vehicle', backref='user')

    def __repr__(self):
        return f'{self.name}'