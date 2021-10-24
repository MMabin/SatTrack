import ephem
from VisibilityCalc import visible
import json


def filteredGPS(observer_coord, TLEs):
    
    satCoords = []

    #print(TLElist[1])

    for TLE in TLEs:
        name = TLE[0]
        line1 = TLE[1]
        line2 = TLE[2]
        # print(name, line1, line2)

        tle_rec = ephem.readtle(name, line1, line2)
        tle_rec.compute()

        try:
            satCoord = [name, 57.2958*tle_rec.sublat, 57.2958*tle_rec.sublong,
                        tle_rec.elevation, tle_rec.eclipsed]
        except:
            pass

        if visible(observer_coord, satCoord):
            satCoords.append(satCoord)
    satCoords = json.dumps(satCoords)
    return satCoords
    # print(satCoords[0])
    # print(len(satCoords))

#print(len(filteredGPS((40.7128, -96.7026))))