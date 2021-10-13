import datetime
import ephem
import pickle
import GetTLEs
from VisibilityCalc import visible


TLElist = GetTLEs.getTLEs()


def filteredGPS(observer_coord, TLEs):
    while True:
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
        print(satCoords[0])
        print(len(satCoords))

filteredGPS((40.7128, -74.0060), TLElist)