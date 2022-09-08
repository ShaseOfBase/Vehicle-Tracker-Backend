from flask_appbuilder.api import BaseApi, expose
from . import appbuilder, db
from .models import User, Route, RoutePoint, Vehicle
from flask import request
import base64
from sqlalchemy import select
from .helpers import get_route_metrics, drop_duplicate_ids

# models routes
models_route_base = '/api/models'
user_route = '/user'
vehicle_route = '/vehicle'
route_route = '/route'
route_point_route = '/route_point'

# data routes
data_route_base = '/api/data'
user_data_route = '/userData'


def user_id_is_valid(user_id):
    result = db.session.execute(select(User).where(User.id == user_id))
    first_result = result.first()

    if first_result:
        return True

    return False


class ModelsAPI(BaseApi):
    route_base = models_route_base

    @expose(user_route, methods=['POST', 'GET'])
    def user(self):
        try:
            username = request.args['username']
            b64_password = request.args['password']
            password = base64.b64decode(b64_password).decode()
            result = db.session.execute(select(User).where(User.name == username))
            first_result = result.first()

            if request.method == 'GET':
                if not first_result:
                    return self.response(404, message=f"No user found")

                if first_result[0].password != password:
                    return self.response(409, message=f"Invalid password")

                return self.response(200, user_data=first_result[0].to_dict())

            elif request.method == 'POST':
                if first_result:
                    return self.response(402, message=f"User already exists")

                new_user = User(name=username, password=password)
                db.session.add(new_user)
                db.session.commit()

                data = new_user.to_dict()

                return self.response(200, user_data=data)

        except Exception as e:
            return self.response(500, error=str(e))

    @expose(vehicle_route, methods=['POST'])
    def vehicle(self):
        try:
            user_id = request.args['user_id']
            if not user_id_is_valid(user_id):
                return self.response(409, error="Invalid user ID...")

            vehicle_name = request.args['vehicle_name']

            result = db.session.execute(select(Vehicle).where(Vehicle.name == vehicle_name)
                                        .where(Vehicle.user_id == user_id))

            if len(result.all()):
                return self.response(409, error="Vehicle name already exists for this company")

            new_vehicle = Vehicle(name=vehicle_name, user_id=user_id)
            db.session.add(new_vehicle)
            db.session.commit()

            return_obj = {'name': new_vehicle.name, 'id': new_vehicle.id,
                          'user_id': user_id}

            d = new_vehicle.to_dict()  # For some reason this becomes empty ???
            return self.response(200, user_data=return_obj)
        except Exception as e:
            return self.response(500, error=str(e))

    @expose(route_route, methods=['POST'])
    def route(self):
        try:
            user_id = request.args['user_id']
            if not user_id_is_valid(user_id):
                return self.response(409, error="Invalid user ID...")

            vehicle_id = request.args['vehicle_id']
            label = request.args['label']
            route = Route(label=label, vehicle_id=vehicle_id)
            db.session.add(route)
            db.session.commit()

            return self.response(200, user_data=route.to_dict())
        except Exception as e:
            return self.response(500, error=str(e))

    @expose(route_point_route, methods=['POST'])
    def route_point(self):
        try:
            user_id = request.args['user_id']
            if not user_id_is_valid(user_id):
                return self.response(409, error="Invalid user ID...")

            route_id = request.args['route_id']

            # todo - if route_id exists, return all route points associated with that route_id

            return self.response(200, message=f"Hello posted..")
        except Exception as e:
            return self.response(500, error=str(e))


class DataAPI(BaseApi):
    route_base = data_route_base

    # Gets all data relevant to the users tracking services
    @expose(user_data_route, methods=['GET'])
    def userData(self):
        try:
            user_id = request.args['user_id']
            if not user_id_is_valid(user_id):
                return self.response(409, error="Invalid user ID...")

            if request.method == 'GET':
                result = db.session.execute(select(Vehicle).where(Vehicle.user_id == user_id))
                result_all = result.all()

                vehicles = [v[0].to_dict() for v in result_all]

                vehicle_ids = set(v['id'] for v in vehicles)

                result = db.session.execute(select(Route).where(Route.vehicle_id.in_(vehicle_ids)))
                result_all = result.all()
                routes = [r[0].to_dict() for r in result_all]

                route_ids = set(r['id'] for r in routes)

                result = db.session.execute(select(RoutePoint).where(RoutePoint.route_id.in_(route_ids)))
                route_points = [rp[0].to_dict() for rp in result.all()]

                data = {
                    'vehicles': vehicles,
                    'routes': routes,
                    'route_points': route_points
                }

                return self.response(200, user_data=data)
        except Exception as e:
            return self.response(500, error=str(e))


appbuilder.add_api(ModelsAPI)
appbuilder.add_api(DataAPI)
