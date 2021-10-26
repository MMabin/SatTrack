from asyncio.windows_events import NULL
from geopy.distance import distance
import math
import numpy


def calc_bearing_incline(observer, sat):
    lat1 = observer['lat']
    lat2 = sat['lat']
    long1 = observer['long']
    long2 = sat['long']

    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = numpy.arctan2(x, y)
    brng = numpy.degrees(brng)
    if brng < 0:
        brng += 360
    return brng


me = {'lat':0, 'long':0}

you = {'lat': -15, 'long':0}

you1 = {'lat': 0, 'long':0}

print(not you)
if not you:

    print(calc_bearing_incline(me, you1))