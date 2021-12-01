import ephem
from VisibilityCalc import get_bearings_visible_sats
import json


def filteredSatBearings(observer_coord, TLEs):    
    sats = []

    for TLE in TLEs:
        name = TLE[0]
        line1 = TLE[1]
        line2 = TLE[2]

        tle_rec = ephem.readtle(name, line1, line2)
        tle_rec.compute()

        try:
            satCoord = {'name': name, 'lat': 57.2958*tle_rec.sublat, 'long': 57.2958*tle_rec.sublong,
                        'height': tle_rec.elevation, 'eclipsed': tle_rec.eclipsed}
        except:
            pass

        bearing = get_bearings_visible_sats(observer_coord, satCoord)

        if bearing:
            sats.append(bearing)       

    sats = json.dumps(sats)
    return sats