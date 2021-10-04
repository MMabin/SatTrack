import time
start = time.time()
import ephem
import time
import pickle

while True:
    satCoords = []

    with open('TLEs.txt', 'rb') as TLEs:
        TLElist = pickle.load(TLEs)
        #print(TLElist)
        for TLE in TLElist:
            name = TLE[0]
            line1 = TLE[1]
            line2 = TLE[2]
            #print(name, line1, line2)

            tle_rec = ephem.readtle(name, line1, line2)
            tle_rec.compute()

            satCoord = [name, str(tle_rec.sublong), str(tle_rec.sublat), tle_rec.elevation, tle_rec.eclipsed]

            satCoords.append(satCoord)

    print(satCoords[-1])
    with open('SatCoords.txt', 'wb') as sc:
        pickle.dump(satCoords, sc)


    time.sleep(0.77)