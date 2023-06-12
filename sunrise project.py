import math
import time
import requests
from datetime import datetime,date


###Model for calculating sunrise/sunset times- includes arctic circle handling
### Assumptions
### 24h =360 degree turn - (slightly more due to Earth mvmt)
### All coords are at sea level - higher vantage points have longer days in reality
### Years have 365 days

#test cases
geocodes=[[42.0967107, -70.9678569], [42.1210441, -71.0300905], [42.0981889, -71.056849]]
timezones=[-5 for i in range(len(geocodes))]  
# #key
# with open(r"C:\Users\cege\Documents\R\problem.txt") as f:
#     lines=f.readlines()
# #addresses
# with open(r"C:\Users\cege\Pictures\gistfile1.txt") as f:
#     lines2=f.readlines()    

# #run first 3 through API
# test=lines2[0:3]


# #generates geocodes from addresses
# geocodes=[]
# l=[]
# for address in test:
#   address_data= requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+t).json()
#   l.append(address_data)
#   address_data=address_data['results']
#   if address_data!=[]:
#     lat, lng= address_data[0]['geometry']['location']['lat'], address_data[0]['geometry']['location']['lng']
#     geocodes.append([lat,lng])

curtime=int(time.time()) #default curtime, making the date to determine sunrise/sunset
def customdate(yyyy,mm,dd):
    return int(datetime.timestamp(datetime(yyyy,mm,dd)))
    
def dpsgetter(time=curtime): #allows custom dates, dps=days past solstice
    x=datetime.date(datetime.fromtimestamp(time))
    dps=(abs(date(x.year,6,21)-x).total_seconds()/86400)%182.5
    return dps

dps=dpsgetter() 


# for lat,long in geocodes:
#     j=requests.get("https://maps.googleapis.com/maps/api/timezone/json?location="+str(lat)+"%2C"+str(long)+"&timestamp="+str(curtime)+"&key="+t).json()
#     if j['status']=="OK":
#         timezones.append(j['rawOffset']/3600)

#now do the geometry
tilt=23.44 #base axial tilt

#relative tilt=
def reltilt(dps): #days past sum solst
    dailytilt=tilt*math.cos(math.pi*dps/182.5)
    return dailytilt

def daylength(lat,dps):
    dailytilt=tilt*math.cos(math.pi*dps/182.5)
    if 90-lat<dailytilt:
        return 24
    if lat+90<dailytilt:
        return 0
    dl=math.degrees((2/15)*math.acos(-math.tan(math.radians(dailytilt))*(math.tan(math.radians(lat)))))
    return dl

def sunrise(lat,long,timezone,dps):
    dtilt=tilt*math.cos(math.pi*dps/182.5)
    try:
        srangle=math.degrees(math.asin(math.tan(math.radians(lat))*math.tan(math.radians(dtilt))))
        sunrisetime=6+timezone-long/15-srangle/15

    except:
        if math.tan(math.radians(lat))*math.tan(math.radians(dtilt))>0:
            sunrisetime=-1
        else:
            sunrisetime=13
    if sunrisetime<0:
        return "Up all day"
    if sunrisetime>12:
        return "Down all day"
    return sunrisetime

def timeconverter(num):
    if str(int(round(math.modf(num)[0]*300/5)))!="60":
        timestring=str(str(int(num))+":"+str(int(round(math.modf(num)[0]*300/5))).zfill(2))
    else:
        timestring=str(str(int(num)+1)+":00")
    
    return timestring

def facts(lat,longitude,tz,dps):
    if type(sunrise(lat,long,tz,dps))==float:
        print("Sunrise is at "+ timeconverter(sunrise(lat,long,tz,dps)))
        print("Day length is " + timeconverter(daylength(lat,dps)))
    if type(sunrise(lat,long,tz,dps))!=float:
        print(sunrise(lat,long,tz,dps))
    else:   
        print("Sunset is at "+ timeconverter(sunrise(lat,long,tz,dps)+daylength(lat,dps)))

for i in range(len(geocodes)):
    dps=dpsgetter() #insert custom date if necessary
    timezone=timezones[i]
    lat=geocodes[i][0]
    long=geocodes[i][1]
    facts(lat,long,timezone,dps)
    
    
#########Sundries for rising/setting angle###############
risingangle=90-math.degrees(math.asin(math.tan(math.radians(abs(lat)))*math.tan(math.radians(tilt))))
settingangle=360-risingangle

sunset=sr+daylength(69.6,50)
longitude=19
timezone=1
sunrise=6+timezone*60-longitude*4-srangle/15
print(sunrise)
#rising angle? longitudinally invariant. 
#nice not sure about abs val
risingangle=90-math.degrees(math.asin(math.tan(math.radians(abs(lat)))*math.tan(math.radians(tilt))))
settingangle=360-risingangle
print(risingangle)
print(settingangle)
    
    
    
