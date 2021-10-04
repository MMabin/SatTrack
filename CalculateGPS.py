import ephem
import time
import pickle

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

        satCoord = [str(tle_rec.sublong), str(tle_rec.sublat), tle_rec.elevation, tle_rec.eclipsed]

        satCoords.append(satCoord)

print(satCoords[500])
with open('SatCoords.txt', 'wb') as sc:
    pickle.dump(satCoords, sc)

with open('SatCoords.txt', 'rb') as sc:
    a = pickle.load(sc)
    print(a[500])


name = "0 NOAA 16 DEB"
line1 = "1 41156U 00055CP  21275.35560669  .00001951  00000-0  76556-3 0  9992"
line2 = "2 41156  98.9504  54.1969 0058241  55.8025 304.8657 14.29625153303998"

tle_rec = ephem.readtle(name, line1, line2)
tle_rec.compute()

#print(tle_rec.sublong, tle_rec.sublat, tle_rec.elevation, tle_rec.eclipsed)

