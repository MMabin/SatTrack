import requests
import configparser
import pickle

def getTLEs():

    class MyError(Exception):
        def __init___(self,args):
            Exception.__init__(self,"my exception was raised with arguments {0}".format(args))
            self.args = args

    # See https://www.space-track.org/documentation for details on REST queries
    # the "Find Starlinks" query searches all satellites with NORAD_CAT_ID > 40000, with OBJECT_NAME matching STARLINK*, 1 line per sat
    # the "OMM Starlink" query gets all Orbital Mean-Elements Messages (OMM) for a specific NORAD_CAT_ID in JSON format

    uriBase                = "https://www.space-track.org"
    requestLogin           = "/ajaxauth/login"
    requestCmdAction       = "/basicspacedata/query"
    requestFindStarlinks   = "/class/tle_latest/NORAD_CAT_ID/>40000/ORDINAL/1/OBJECT_NAME/STARLINK~~/format/json/orderby/NORAD_CAT_ID%20asc"
    requestOMMStarlink1    = "/class/omm/NORAD_CAT_ID/"
    requestOMMStarlink2    = "/orderby/EPOCH%20asc/format/json"
    requestLEOs = 'https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/>now-30/MEAN_MOTION/>11.25/format/3le'

    # Parameters to derive apoapsis and periapsis from mean motion (see https://en.wikipedia.org/wiki/Mean_motion)

    GM = 398600441800000.0
    GM13 = GM ** (1.0/3.0)
    MRAD = 6378.137
    PI = 3.14159265358979
    TPI86 = 2.0 * PI / 86400.0



    # Use configparser package to pull in the ini file (pip install configparser)
    config = configparser.ConfigParser()
    config.read("./SLTrack.ini")
    configUsr = config.get("configuration","username")
    configPwd = config.get("configuration","password")
    configOut = config.get("configuration","output")
    siteCred = {'identity': configUsr, 'password': configPwd}


    # use requests package to drive the RESTful session with space-track.org
    with requests.Session() as session:
        # run the session in a with block to force session to close if we exit

        # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
        resp = session.post(uriBase + requestLogin, data = siteCred)
        if resp.status_code != 200:
            raise MyError(resp, "POST fail on login")

        # this query requests TLES of LEOs
        resp = session.get(requestLEOs)


        # converts response TLES into a list of lists
        respLines = resp.text.splitlines()
        TLElist = []
        for i in range(0, len(respLines), 3):
            TLE = []
            for j in range(i, i+3):
                TLE.append(respLines[j])
            TLElist.append(TLE)

        # Dump TLEs to file
        with open('TLEs.txt', 'wb') as TLEs:
            pickle.dump(TLElist, TLEs)

        if resp.status_code != 200:
            print(resp)
            raise MyError(resp, "GET fail on request for Starlink satellites")

        print(len(TLElist))


        session.close()
