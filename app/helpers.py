from geopy import distance


def get_distance(point_a, point_b):
    return distance.distance(point_a, point_b).km


def get_route_metrics(route_points):
    sorted_route_points = sorted(route_points, key=lambda x: x['timestamp'])

    distances = []
    for i in range(len(sorted_route_points)-1):
        point_a_lat = sorted_route_points[i]['lat']
        point_a_long = sorted_route_points[i]['long']

        point_b_lat = sorted_route_points[i+1]['lat']
        point_b_long = sorted_route_points[i+1]['long']

        point_a = point_a_lat, point_a_long
        point_b = point_b_lat, point_b_long
        distance = get_distance(point_a, point_b)
        distances.append(distance)

    total_distance = sum(distances)
    total_time_taken = (sorted_route_points[-1]['timestamp'] - sorted_route_points[0]['timestamp']).total_seconds()

    avg_speed = total_distance / total_time_taken * 3600  # for Km/hour

    return {
        'total_distance': total_distance,
        'total_time': total_time_taken,
        'avg_speed': avg_speed
    }