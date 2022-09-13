import datetime
import random
from random import uniform, randint
import pytest
from app import db
from app.models import User, Route, RoutePoint, Vehicle

route_point_count = 3


def get_random_id(length):
    return ''.join([str(randint(0, 9)) for _ in range(length)])


@pytest.fixture
def test_users():
    try:
        name = f'test_{random.random()}'
        user = User(name=name, password='abc123')
        db.session.add(user)
        db.session.commit()

        yield user.id

        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(1)
    #    db.session.delete(user)
    #    db.session.commit()


@pytest.fixture
def test_vehicles(test_users):
    name = f'TestSubaru{get_random_id(5)}'
    vehicle = Vehicle(name=name, user_id=test_users)
    db.session.add(vehicle)
    db.session.commit()

    yield vehicle.id

    db.session.delete(vehicle)
    db.session.commit()


@pytest.fixture
def test_routes(test_vehicles):
    route = Route(label=f'Route_{random.random()}', vehicle_id=test_vehicles)
    db.session.add(route)
    db.session.commit()

    yield route.id

    db.session.delete(route)
    db.session.commit()


@pytest.fixture
def test_route_points(test_routes):
    rp_length = route_point_count
    route_points = set()
    for _ in range(rp_length):
        route_point = RoutePoint(timestamp=datetime.datetime.now(),
                                 route_id=test_routes, lng=uniform(10, 70),
                                 lat=uniform(10, 70))
        route_points.add(route_point)
        db.session.add(route_point)

    db.session.commit()

    yield route_points

    for rp in route_points:
        db.session.delete(rp)

    db.session.commit()


def test_data_inserts(test_route_points):
    assert len(test_route_points) == route_point_count


