import math


def linear_distance_between_two_points(point_from: tuple, point_to: tuple):
    if len(point_from) != len(point_to):
        return False

    delta_list = []
    for direction in range(len(point_from)):
        delta_list.append(point_to[direction] - point_from[direction])

    return round(math.hypot(*delta_list), 3)


def linear_distance_between_many_points(*points):
    result = 0
    for i in range(len(points)-1):
        distance = linear_distance_between_two_points(points[i], points[i+1])
        if distance:
            result += distance
        else:
            return False

    return result