from geopy.distance import distance
import math

observer = (41.2565, -95.9345)

sat = ['0 TBA - TO BE ASSIGNED', '-47:50:13.1', '-14:28:25.4', 31.7683, 10.2137, 510000000000000, False]



def calc_dist(observer, sat):
    sat_coords = (sat[1], sat[2])

    d = distance(observer, sat_coords).m
    return d

def calc_angle(observer, sat):

    return calc_dist(observer, sat)/6371000


def visible(observer, sat):
    angle = calc_angle(observer, sat)

    if angle >= math.pi/2:
        return False

    minimumVisibleHeight = 6371000 * ((1 / math.cos(angle)) - 1)
    los = sat[3] > minimumVisibleHeight
    return los and not sat[4] and sat[3] < 800000


