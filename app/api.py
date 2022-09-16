from datetime import datetime
from flask_appbuilder.api import BaseApi, expose
from . import appbuilder, db
from .models import User, Route, RoutePoint, Vehicle
from flask import request
import base64
from sqlalchemy import select


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
                    return self.response(400, message="No user found")

                if first_result[0].password != password:
                    return self.response(400, message="Invalid password")

                return self.response(200, **first_result[0].to_dict())

            elif request.method == 'POST':
                if first_result:
                    return self.response(400, message="User already exists")

                new_user = User(name=username, password=password)
                db.session.add(new_user)
                db.session.commit()

                data = {'id': new_user.id}

                return self.response(200, **data)

        except Exception as e:
            return self.response(500, error=str(e))

    @expose(vehicle_route, methods=['POST'])
    def vehicle(self):
        try:
            user_id = request.args['user_id']
            if not user_id_is_valid(user_id):
                return self.response(400, error="Invalid user ID...")

            vehicle_name = request.args['vehicle_name']

            result = db.session.execute(select(Vehicle).where(Vehicle.name == vehicle_name)
                                        .where(Vehicle.user_id == user_id))

            if len(result.all()):
                return self.response(400, error="Vehicle name already exists for this company")

            vehicle_data = {'name': vehicle_name, 'user_id': user_id}
            new_vehicle = Vehicle(**vehicle_data)
            db.session.add(new_vehicle)
            db.session.commit()

            vehicle_data['id'] = new_vehicle.id

            return self.response(200, **vehicle_data)
        except Exception as e:
            return self.response(500, error=str(e))

    @expose(route_route, methods=['POST'])
    def route(self):
        try:
            user_id = request.args['user_id']
            if not user_id_is_valid(user_id):
                return self.response(400, error="Invalid user ID...")

            route_data = {
                'label': request.args['label'],
                'vehicle_id': int(request.args['vehicle_id'])
            }

            route = Route(**route_data)
            db.session.add(route)
            db.session.commit()

            route_data['id'] = route.id

            return self.response(200, **route_data)
        except Exception as e:
            return self.response(500, error=str(e))

    @expose(route_point_route, methods=['POST'])
    def route_point(self):
        try:
            user_id = request.args['user_id']
            if not user_id_is_valid(user_id):
                return self.response(400, error="Invalid user ID...")

            rp_data = {
                'lat': float(request.args['lat']),
                'lng': float(request.args['lng']),
                'timestamp': datetime.strptime(request.args['timestamp'], '%Y-%m-%dT%H:%M'),
                'route_id': int(request.args['route_id'])
            }
            route_point = RoutePoint(**rp_data)
            db.session.add(route_point)
            db.session.commit()

            rp_data['id'] = route_point.id

            return self.response(200, **rp_data)
        except Exception as e:
            return self.response(500, error=str(e))


class DataAPI(BaseApi):
    route_base = data_route_base

    # Gets all data relevant to the users tracking services
    @expose(user_data_route, methods=['GET'])
    def user_data(self):
        try:
            user_id = request.args['user_id']
            if not user_id_is_valid(user_id):
                return self.response(400, error="Invalid user ID...")

            if request.method == 'GET':
                result = db.session.execute(select(Vehicle).where(Vehicle.user_id == user_id))
                result_all = result.all()

                vehicles = [v[0].to_dict() for v in result_all]
                vehicles.sort(key=lambda x: x['name'].lower())

                vehicle_ids = {v['id'] for v in vehicles}

                result = db.session.execute(select(Route).where(Route.vehicle_id.in_(vehicle_ids)))
                result_all = result.all()
                routes = [r[0].to_dict() for r in result_all]
                routes.sort(key=lambda x: x['label'].lower())

                route_ids = {r['id'] for r in routes}

                result = db.session.execute(select(RoutePoint).where(RoutePoint.route_id.in_(route_ids)))
                route_points = [rp[0].to_dict() for rp in result.all()]

                route_points.sort(key=lambda x: x['timestamp'])

                data = {
                    'vehicles': vehicles,
                    'routes': routes,
                    'route_points': route_points
                }

                return self.response(200, **data)
        except Exception as e:
            return self.response(500, error=str(e))


appbuilder.add_api(ModelsAPI)
appbuilder.add_api(DataAPI)
