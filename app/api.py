from flask_appbuilder.api import BaseApi, expose
from . import appbuilder, db
from .models import User, Route, RoutePoint, Company, Vehicle
from flask import request
import base64
from sqlalchemy import select
from helpers import get_route_metrics


def user_id_is_valid(user_id):
    result = db.session.execute(select(User).where(User.id == user_id))
    first_result = result.first()

    if first_result:
        return True

    return False


def get_route_points_from_query_result(result):
    route_points = []
    for row in result:
        route_points.append(
            {
                'route_id': row.RoutePoint.route_id,
                'timestamp': row.RoutePoint.timestamp,
                'lat': row.RoutePoint.lat,
                'long': row.RoutePoint.long
            }
        )

    return route_points


class AllPurposeAPI(BaseApi):

    route_base = '/api'

    @expose('/user', methods=['POST', 'GET'])
    def user(self):
        try:
            username = request.args['username']
            b64_password = request.args['password']
      #      password = base64.b64decode(b64_password) todo - re-enable b64
            password = b64_password
            result = db.session.execute(select(User).where(User.name == username))
            first_result = result.first()

            if request.method == 'GET':
                if not first_result:
                    return self.response(404, message=f"No user found")

                if first_result[0].password != password:
                    return self.response(409, message=f"Invalid password")

                return self.response(200, user_id=first_result[0].id)

            elif request.method == 'POST':
                if first_result:
                    return self.response(402, message=f"User already exists")

                new_user = User(name=username, password=password)
                db.session.add(new_user)
                db.session.commit()

                return self.response(200, user_id=new_user.id)

        except Exception as e:
            return self.response(500, error=str(e))

    @expose('/company', methods=['POST', 'GET'])
    def company(self):
        try:
            user_id = request.args['user_id']

            if not user_id_is_valid(user_id):
                return self.response(409, error="Invalid user ID...")

            if request.method == 'GET':
                result = db.session.execute(select(Company).where(Company.user_id == user_id))
                first_result = result.first()

                if not first_result:
                    data = {}

                else:
                    data = {
                        'company_name': first_result[0].name,
                        'company_id': first_result[0].id
                    }

                return self.response(200, data=data)

            elif request.method == 'POST':
                company_name = request.args['company_name']
                result = db.session.execute(select(Company).where(Company.name == company_name))
                first_result = result.first()
                if first_result:
                    return self.response(409, error='Company already exists')

                new_company = Company(name=company_name, user_id=user_id)
                db.session.add(new_company)
                db.session.commit()

                data = {
                    'company_name': company_name,
                    'company_id': new_company.id
                }

                return self.response(200, data=data)
        except Exception as e:
            return self.response(500, error=str(e))

    @expose('/vehicle', methods=['POST', 'GET'])
    def vehicle(self):
        try:
            user_id = request.args['user_id']

            if not user_id_is_valid(user_id):
                return self.response(409, error="Invalid user ID...")

            company_id = request.args['company_id']

            if request.method == 'GET':
                result = db.session.execute(select(Vehicle).where(Vehicle.company_id == company_id))

                vehicles = []
                for row in result:
                    vehicle = {
                        'id': row.Vehicle.id,
                        'name': row.Vehicle.name
                    }
                    vehicles.append(vehicle)

                return self.response(200, data=vehicles)
            elif request.method == 'POST':
                vehicle_name = request.args['vehicle_name']

                result = db.session.execute(select(Vehicle).where(Vehicle.name == vehicle_name)
                                            .where(Vehicle.company_id == company_id))

                if not len(result.all()):
                    return self.response(409, error="Vehicle name already exists for this company")

                new_vehicle = Vehicle(name=vehicle_name, company_id=company_id)
                db.session.add(new_vehicle)
                db.session.commit()

                return self.response(200, name=vehicle_name, company_id=company_id)
        except Exception as e:
            return self.response(500, error=str(e))

    @expose('/route', methods=['POST', 'GET'])
    def route(self):
        try:
            user_id = request.args['user_id']

            if not user_id_is_valid(user_id):
                return self.response(409, error="Invalid user ID...")

            vehicle_id = request.args['vehicle_id']

            if request.method == 'GET':

                result = db.session.execute(select(Route).where(Route.vehicle_id == vehicle_id))

                routes = []
                route_ids = set()
                for row in result:
                    route_ids.add(row.Route.id)
                    routes.append({
                        'route_id': row.Route.id,
                        'route_points': []
                    })

                rp_result = db.session.execute(select(RoutePoint).where(RoutePoint.route_id.in_(route_ids)))

                route_points = get_route_points_from_query_result(rp_result)

                indexed_route_points = {x['route_id']: i for i, x in enumerate(routes)}
                for route_point in route_points:
                    routes[indexed_route_points['route_id']]['route_points'].append(route_point)

                return self.response(200, data=routes)
            elif request.method == 'POST':

                # todo - if vehicle_id exists, create route with given vehicle_id

                return self.response(200, message=f"Hello {name}, posted..")
        except Exception as e:
            return self.response(500, error=str(e))

    @expose('/route_point', methods=['POST', 'GET'])
    def route_point(self):
        try:
            user_id = request.args['user_id']

            if not user_id_is_valid(user_id):
                return self.response(409, error="Invalid user ID...")

            route_id = request.args['route_id']
            if request.method == 'GET':

                # Cant we return these in the route request?

                return self.response(200, message=f"Hello {name}, got..")
            elif request.method == 'POST':

                # todo - if route_id exists, return all route points associated with that route_id

                return self.response(200, message=f"Hello {name}, posted..")
        except Exception as e:
            return self.response(500, error=str(e))

        @expose('/travel_metrics', methods=['GET'])
        def travel_metrics(self):
            try:
                route_id = request.args['route_id']

                result = db.session.execute(select(RoutePoint).where(RoutePoint.route_id == route_id))

                route_points = get_route_points_from_query_result(result)

                route_metrics = get_route_metrics(route_points)

                return self.response(200, data=route_metrics)

            except Exception as e:
                return self.response(500, error=str(e))

appbuilder.add_api(AllPurposeAPI)