import json
import urllib.request
import time
import numpy as np
from datetime import datetime
from datetime import datetime, timedelta, date
import os.path
from os import path
import math
import requests
import haversine as hs
import sys
import pytz
import requests

class windyWeather():
    def __init__(self, inputOrg, inputLon, inputLat):
        self.org = inputOrg
        self.lon = inputLon
        self.lat = inputLat
        
        self.verticalInfo = []
        if self.org.upper() != 'EC' and self.org.upper() != 'GFS':
            print('Error: Organization should be \'EC\' or \'GFS\'')
        else:
            try:
                tmplon = float(self.lon)
                tmplat = float(self.lat)
                try:
                    self.JSON = self.updateWeatherData()
                    self.getTimeSeriesVerticalWeather()
                except:
                    print('Error: Weather data attempt to access failed.')
            except:
                print('Error: Longitude and Latitude should be float type.')

    def updateInfo(self, inputOrg, inputLon, inputLat):
        self.org = inputOrg
        self.lon = inputLon
        self.lat = inputLat
        self.JSON = ''
        self.verticalInfo = []
        if self.org.upper() != 'EC' and self.org.upper() != 'GFS':
            print('Error: Organization should be \'EC\' or \'GFS\'')
        else:
            try:
                tmplon = float(self.lon)
                tmplat = float(self.lat)
                try:
                    self.JSON = self.updateWeatherData()
                    self.getTimeSeriesVerticalWeather()
                except:
                    print('Error: Weather data attempt to access failed.')
            except:
                print('Error: Longitude and Latitude should be float type.')

    def updateWeatherData(self):
        try:
            if self.org == 'EC' or self.org == 'ec' or self.org == 'Ec':
                url = "https://node.windy.com/forecast/meteogram/ecmwf/" + str(self.lat) +'/' + str(self.lon)
                #print(url)
                data = requests.get(url).text
                #print(data)
            #record = data.decode('UTF-8')
            data = json.loads(data)
            return data
        except:
            return {'Wrong input parameter or Internet problem, please check if weather source is EC'}

    def analyzeDetailT(self):
        JSON = self.JSON
        model = JSON['header']['model']
        reftime = JSON['header']['refTime']
        T1000 = JSON['data']['temp-1000h']
        T950 = JSON['data']['temp-950h']
        T900 = JSON['data']['temp-900h']
        T850 = JSON['data']['temp-850h']
        T800 = JSON['data']['temp-800h']
        T700 = JSON['data']['temp-700h']
        T600 = JSON['data']['temp-600h']
        T500 = JSON['data']['temp-500h']
        T400 = JSON['data']['temp-400h']
        T300 = JSON['data']['temp-300h']
        T200 = JSON['data']['temp-200h']

        T750 = []
        T650 = []
        T550 = []
        T450 = []
        T350 = []
        T250 = []
        count = 0
        for i in T800:
            T750.append((T700[count] + T800[count])/2.0)
            T650.append((T600[count] + T700[count]) / 2.0)
            T550.append((T500[count] + T600[count]) / 2.0)
            T450.append((T400[count] + T500[count]) / 2.0)
            T350.append((T300[count] + T400[count]) / 2.0)
            T250.append((T200[count] + T300[count]) / 2.0)
            count += 1

        # print('T analyzed.')
        return [T1000,T950,T900,T850,T800,T750,T700,T650,T600,T550,T500,T450,T400,T350,T300,T250,T200]

    def analyzeDetailRH(self):
        JSON = self.JSON
        model = JSON['header']['model']
        reftime = JSON['header']['refTime']
        RH1000 = JSON['data']['rh-1000h']
        RH950 = JSON['data']['rh-950h']
        RH900 = JSON['data']['rh-900h']
        RH850 = JSON['data']['rh-850h']
        RH800 = JSON['data']['rh-800h']
        RH700 = JSON['data']['rh-700h']
        RH600 = JSON['data']['rh-600h']
        RH500 = JSON['data']['rh-500h']
        RH400 = JSON['data']['rh-400h']
        RH300 = JSON['data']['rh-300h']
        RH200 = JSON['data']['rh-200h']

        RH750 = []
        RH650 = []
        RH550 = []
        RH450 = []
        RH350 = []
        RH250 = []
        count = 0
        for i in RH800:
            RH750.append((RH700[count] + RH800[count])/2.0)
            RH650.append((RH600[count] + RH700[count]) / 2.0)
            RH550.append((RH500[count] + RH600[count]) / 2.0)
            RH450.append((RH400[count] + RH500[count]) / 2.0)
            RH350.append((RH300[count] + RH400[count]) / 2.0)
            RH250.append((RH200[count] + RH300[count]) / 2.0)
            count += 1

        # print('RH analyzed.')
        return [RH1000,RH950,RH900,RH850,RH800,RH750,RH700,RH650,RH600,RH550,RH500,RH450,RH400,RH350,RH300,RH250,RH200]

    def analyzeDetailwindV(self):
        JSON = self.JSON
        model = JSON['header']['model']
        reftime = JSON['header']['refTime']
        WV1000 = JSON['data']['wind_v-1000h']
        WV950 = JSON['data']['wind_v-950h']
        WV900 = JSON['data']['wind_v-900h']
        WV850 = JSON['data']['wind_v-850h']
        WV800 = JSON['data']['wind_v-800h']
        WV700 = JSON['data']['wind_v-700h']
        WV600 = JSON['data']['wind_v-600h']
        WV500 = JSON['data']['wind_v-500h']
        WV400 = JSON['data']['wind_v-400h']
        WV300 = JSON['data']['wind_v-300h']
        WV200 = JSON['data']['wind_v-200h']

        WV750 = []
        WV650 = []
        WV550 = []
        WV450 = []
        WV350 = []
        WV250 = []
        count = 0
        for i in WV800:
            WV750.append((WV700[count] + WV800[count]) / 2.0)
            WV650.append((WV600[count] + WV700[count]) / 2.0)
            WV550.append((WV500[count] + WV600[count]) / 2.0)
            WV450.append((WV400[count] + WV500[count]) / 2.0)
            WV350.append((WV300[count] + WV400[count]) / 2.0)
            WV250.append((WV200[count] + WV300[count]) / 2.0)
            count += 1

        # print('WV analyzed.')
        return [WV1000,WV950,WV900,WV850,WV800,WV750,WV700,WV650,WV600,WV550,WV500,WV450,WV400,WV350,WV300,WV250,WV200]

    def analyzeDetailwindU(self):
        JSON = self.JSON
        model = JSON['header']['model']
        reftime = JSON['header']['refTime']
        WU1000 = JSON['data']['wind_u-1000h']
        WU950 = JSON['data']['wind_u-950h']
        WU900 = JSON['data']['wind_u-900h']
        WU850 = JSON['data']['wind_u-850h']
        WU800 = JSON['data']['wind_u-800h']
        WU700 = JSON['data']['wind_u-700h']
        WU600 = JSON['data']['wind_u-600h']
        WU500 = JSON['data']['wind_u-500h']
        WU400 = JSON['data']['wind_u-400h']
        WU300 = JSON['data']['wind_u-300h']
        WU200 = JSON['data']['wind_u-200h']

        WU750 = []
        WU650 = []
        WU550 = []
        WU450 = []
        WU350 = []
        WU250 = []
        count = 0
        for i in WU800:
            WU750.append((WU700[count] + WU800[count]) / 2.0)
            WU650.append((WU600[count] + WU700[count]) / 2.0)
            WU550.append((WU500[count] + WU600[count]) / 2.0)
            WU450.append((WU400[count] + WU500[count]) / 2.0)
            WU350.append((WU300[count] + WU400[count]) / 2.0)
            WU250.append((WU200[count] + WU300[count]) / 2.0)
            count += 1

        # print('WU analyzed.')
        return [WU1000,WU950,WU900,WU850,WU800,WU750,WU700,WU650,WU600,WU550,WU500,WU450,WU400,WU350,WU300,WU250,WU200]

    def analyzeDetailPressure(self):
        JSON = self.JSON
        T800 = JSON['data']['temp-800h']
        P = []
        for row in range(0, 17):
            P.append([])
            for i in range(0, len(T800)):
                P[row].append(1000 - 50 * row)
        return P

    def getTimeSeriesVerticalWeather(self):
        iodata = self.JSON
        try:
            hourspoint = iodata['data']['hours']
        except:
            return ('Retrieved JSON is not valid json type, please run getJSON() to check.')

        for i in range(0, len(hourspoint)):
            hourspoint[i] = hourspoint[i] / 1000.0

        dates = [time.strftime('%d%Hz', time.localtime(ts)) for ts in hourspoint]
        newdates = []
        ticks = []
        count = 1
        for i in dates:
            if count % 2 == 0:
                newdates.append(i)
                ticks.append(count)
            count += 1

        wind_U = self.analyzeDetailwindU()
        wind_V = self.analyzeDetailwindV()

        wind_amplitudes = np.sqrt(np.add(np.square(wind_U), np.square(wind_V))) * 1.94384449
        wind_directions  = np.arctan2(wind_U,wind_V)/np.pi*180 + 180 % 360

        self.verticalInfo = [dates, self.analyzeDetailPressure(), self.analyzeDetailT(), self.analyzeDetailRH(), wind_amplitudes, wind_directions]

    def getCertainTimeVerticalWeather(self, timePoint):
        iodata = self.verticalInfo
        if timePoint < len(iodata[0]) and timePoint >= 0:
            timeStr = iodata[0][timePoint]
            Pressure = []
            Temperature = []
            Humidity= []
            windUcomponent= []
            windVcomponent= []

            for j in range(0, 17):
                Pressure.append(iodata[1][j][timePoint])
                Temperature.append(iodata[2][j][timePoint])
                Humidity.append(iodata[3][j][timePoint])
                windUcomponent.append(iodata[4][j][timePoint])
                windVcomponent.append(iodata[5][j][timePoint])
            return [timeStr, Pressure, Temperature, Humidity,windUcomponent, windVcomponent]
        else:
            return ('Requested time point is out of forecast period, please check.')
        #except:
        #    return ('Retrieved JSON is not valid json type, please run getJSON() to check.')

    def getVerticalWeather(self):
        return self.verticalInfo

    def getNumberOfData(self, timeStr):
        for i in range(0, len(self.verticalInfo[0])):
            if self.verticalInfo[0][i].find(timeStr) != -1:
                return i
        return -1

    def getInfo(self):
        iodata = self.JSON
        print(self.org)
        print(self.lon)
        print(self.lat)
        print(iodata['header']['refTime'])
        #print(iodata)
        return [self.org, self.lon, self.lat, iodata['header']['refTime']]

    def getJSON(self):
        return self.JSON

def Locations():
    locations = {
    "DVR"    :   [51.160,1.331],
    "KOK"    :   [51.103,2.623],
    "FERDI"  :   [50.877,3.591],
    "BUB"    :   [50.888,4.516],
    "TUTSO"  :   [50.506,5.207],
    "LENDO"  :   [50.606,6.239],
    "DIK"    :   [50.063,5.983],
    "MTZ"    :   [49.339,6.299],
    "POGOL"  :   [48.651,6.262],
    "FAMEN"  :   [49.912,5.146],
    "BELDI"  :   [50.032,2.931],
    "COA"    :   [51.359,2.889],
    "HELEN"  :   [51.197,3.758],
    "EBAW"   :   [51.187,4.462],
    "BROGY"  :   [51.164,5.469],
    "EHRD"   :   [51.809,4.712],
    "EDDL"   :   [51.255,6.684],
    "FLEXS"  :   [49.790,6.973]
}
    return locations

def Summer():
    now = datetime.utcnow()
    utc = now.strftime("%Y-%m-%d %H:%M:%S")

    zone = pytz.timezone('Europe/London')
    london = datetime.now(zone)
    london = london.strftime("%Y-%m-%d %H:%M:%S")

    if utc == london:
        SummerTime = False
    else:
        SummerTime = True

    print("Summer Time is",SummerTime)
    return SummerTime

def Londontime():
    zone = pytz.timezone('Europe/London')
    london = datetime.now(zone)
    return london
    
def Update(newdate):

    end_result = {}
    a = windyWeather('ec',4.484,50.901)
    info = a.getInfo()

    datestring = newdate
    end_result["info"] = {
            "date" : info[3],
            "datestring" : datestring
        }

    end_result["data"] = {}
    
    locations = Locations()
    FL = [0,1,30,50,64,2,100,3,140,4,180,5,240,6,300,340,390]


    for location in locations:
        print("Weather from the %s at %s o' clock at location: %s" % (datestring[:2],datestring[2:],location))
        location_data = {}
        a = windyWeather('ec',locations[location][1],locations[location][0])

        time = a.getNumberOfData(newdate)
        data = a.getCertainTimeVerticalWeather(time) # get data from our specific time
        counter = 0
        for flightlevel in FL:
            #print(data)
            #print(location, flightlevel)
            #out = "Geoheight = {:>4}   Temperature = {:<20} K    Humidity = {:<20}   Speed = {:<20} knots      Heading = {:<20} °".format(str(data[1][counter]), str(data[2][counter]), str(data[3][counter]), str(data[4][counter]), str(data[5][counter]))
            #out = "Geoheight = %s   °" % (str(data[1][counter]))
            #print(out)
            location_data[str(flightlevel)] = {
                'T(K)' : str(data[2][counter]),
                'windspeed' : str(data[4][counter]),
                'windhdg': str(data[5][counter])
            }
            counter += 1
            #print(location_data)
        end_result["data"][str(location)] = location_data

  

    with open(weatherFile,'w') as file:
        json.dump(end_result,file)
        file.close()

def Updatetime(time,day):
    # round UTC to nearest next hour
    if time < 23:
        next = time + 1
    else: 
        if not SummerTime:
            next = 1
        else:
            next = 23

    # find the nearest possible hour of UTC
    if not SummerTime:
        possiblehour = [1,4,7,10,13,16,19,22]
    else:
        possiblehour = [2,5,8,11,14,17,20,23]
    nexthour = min(possiblehour, key=lambda x:abs(x-next))

    if len(str(nexthour))==1:
        nexthour = "0%d"%(nexthour) #make sure hour is always two digits

    newtime = nexthour

    newdate = "%s%s"% (day,newtime)

    print("New dayhour string is:", newdate)
    Update(newdate)

def MakeNew():
    time = int(UKtime.strftime("%H"))
    day = UKtime.strftime("%d")
    Updatetime(time,day)





#Run script  
global weatherFile 
weatherFile = path.dirname(os.path.abspath(sys.argv[0])) + "/weather.json"

global SummerTime
SummerTime = Summer()

global UKtime
UKtime = Londontime()

MakeNew()
