import datetime
from random import randint, random
import pytest
from app import db
from app.models import User, Route, RoutePoint, Vehicle


def get_random_id(length):
    return ''.join([str(randint(0, 9)) for _ in range(length)])


@pytest.fixture
def test_users():
    name = f'TestBob{get_random_id(5)}'
    user = User(name=name, password='abc123')
    db.session.add(user)
    db.session.commit()
    return user.id


@pytest.fixture
def test_vehicles(test_users):
    name = f'TestSubaru{get_random_id(5)}'
    vehicle = Vehicle(name=name, user_id=test_users)
    db.session.add(vehicle)
    db.session.commit()
    return vehicle.id


@pytest.fixture
def test_routes(test_vehicles):
    route = Route(vehicle_id=test_vehicles)
    db.session.add(route)
    db.session.commit()
    return route.id


def test_route_points(test_routes):
    rp_length = 3
    route_points = set()
    for _ in range(rp_length):
        route_point = RoutePoint(timestamp=datetime.datetime.now(),
                                 route_id=test_routes, long=randint(5, 50) + random(),
                                 lat=randint(5, 50) + random())
        db.session.add(route_point)

    db.session.commit()

    ids = {rp.id for rp in route_points}

    return len(ids) == rp_length



