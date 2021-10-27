from asyncio.windows_events import NULL
from geopy.distance import EARTH_RADIUS, distance
import math
import numpy

observer = (41.2565, -95.9345)

sat = ['0 TBA - TO BE ASSIGNED', '-47:50:13.1', '-14:28:25.4', 31.7683, 10.2137, 510000000000000, False]



def calc_dist(observer, sat):
    observer_coords = (observer['lat'], observer['long'])
    sat_coords = (sat['lat'], sat['long'])


    d = distance(observer_coords, sat_coords).m
    return d

def calc_angle(observer, sat):

    return calc_dist(observer, sat)/6371000


def get_bearings_visible_sats(observer, sat):
    if sat['height'] > 700000 or sat['eclipsed']:
        return False

    angle = calc_angle(observer, sat)

    if angle >= math.pi/2:
        return False

    earth_rad = 1000*EARTH_RADIUS
    minimumVisibleHeight = earth_rad * ((1 / math.cos(angle)) - 1)
    fov = sat['height'] > minimumVisibleHeight

    if fov:
        lat1= observer['lat']
        lat2= sat['lat']
        long1= observer['long']
        long2= sat['long']

        dLon = (long2 - long1)
        x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
        y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
        brng = numpy.arctan2(x,y)
        brng = numpy.degrees(brng)
        
        if brng <0:
            brng += 360
        
        A = math.sin(angle)*(earth_rad + minimumVisibleHeight)
        B = sat['height']-minimumVisibleHeight
        D = math.sqrt(A**2+B**2+2*A*B*math.sin(angle))
        incline= numpy.degrees(math.asin(B*math.cos(angle)/D))

        if incline<15:
            return False

        return {'name': sat['name'], 'bearing': brng, 'incline': incline}

def calc_bearing_incline(observer, sat, min_height):
    lat1= observer['lat']
    lat2= sat['lat']
    long1= observer['long']
    long2= sat['long']

    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = numpy.arctan2(x,y)
    brng = numpy.degrees(brng)
    
    if brng <0:
        brng += 360
    
    
    
    