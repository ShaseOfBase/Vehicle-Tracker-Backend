import datetime
from random import random, uniform
from app import db
from app.models import Route, RoutePoint, Vehicle, User
from test_data import get_random_id


def add_user(name, password):
    user = User(name=name, password=password)
    db.session.add(user)
    db.session.commit()
    return user.id


def add_vehicles(user_id, count):
    vehicle_ids = set()
    for _ in range(count):
        name = f'TestSubaru{get_random_id(5)}'
        vehicle = Vehicle(name=name, user_id=user_id)
        db.session.add(vehicle)
        db.session.commit()
        vehicle_ids.add(vehicle.id)

    return vehicle_ids


def add_routes(vehicle_ids, count):
    route_ids = set()
    for vehicle_id in vehicle_ids:
        for _ in range(count):
            route = Route(label=f'Route_{random()}', vehicle_id=vehicle_id)
            db.session.add(route)
            db.session.commit()
            route_ids.add(route.id)

    return route_ids


def add_route_points(route_ids, count):
    for route_id in route_ids:
        for _ in range(count):
            route_point = RoutePoint(timestamp=datetime.datetime.now(),
                                     route_id=route_id, lng=uniform(10, 70),
                                     lat=uniform(10, 70))
            db.session.add(route_point)

    db.session.commit()


def add_dev_data(user_id=None, new_user_name='', password=''):
    if not user_id and not new_user_name:
        raise ValueError('need either user_id or new_user_name')
    if new_user_name:
        user_id = add_user(new_user_name, password)

    vehicle_ids = add_vehicles(user_id, 5)
    route_ids = add_routes(vehicle_ids, 5)
    add_route_points(route_ids, 3)


if __name__ == '__main__':
    add_dev_data(new_user_name='dev', password='abc123')