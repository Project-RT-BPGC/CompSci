import math
import os
import time
# (Latitude, Longitude) of MT1 lab, BITS Pilani, KK Birla Goa campus: (15.392598,82.5)
lat = float(input("Enter the Latitude (in degrees): "))
long = float(input("Enter the Longtiude (in degrees): "))
RA1 = float(input("Enter the Right angle: "))
RA = math.radians(RA1*360/24)
DEC1 = float(input("Enter the Declination: "))
DEC = math.radians(DEC1)
timedelay = int(input("Enter the time delay in seconds: "))
# refresh_rate=0

# globals
latitude = math.radians(lat)
longitude = math.radians(long)


def days_after_J2000():
    year = time.gmtime()[0]  # returns current year
    hour = time.gmtime()[3]  # returns UT hour
    minute = time.gmtime()[4]  # returns UT minutes
    seconds = time.gmtime()[5]  # returns UT seconds
    month = time.gmtime()[1]
    day = time.gmtime()[2]
    UT = (hour + minute/60 + seconds/3600)
    extra = (100.0*year + month) - 190002.5
    JD = 367.0*year-int(7.0*(year+int((month+9.0)/12.0))/4.0)+int(275.0*month/9.0) + \
        day+UT/24.0+1721013.5 - 0.5*extra/math.fabs(extra)+0.5+0.229086
    return JD


def LST(longitude):
    year = time.gmtime()[0]
    month = time.gmtime()[1]
    day = time.gmtime()[2]
    hour = time.gmtime()[3]
    minute = time.gmtime()[4]
    second = time.gmtime()[5]
    if ((month == 1) or (month == 2)):
        year = year - 1
        month = month + 12

    a = math.floor(year/100)
    b = 2 - a + math.floor(a/4)
    c = math.floor(365.25*year)
    d = math.floor(30.6001*(month + 1))

    jd = b + c + d - 730550.5 + day + \
        (hour + minute/60.0 + second/3600.0)/24.0  # Days since J2000
    jt = jd/36525.0  # julian centuries since J2000.0
    mst = 280.46061837 + 360.98564736629*jd + 0.000387933 * \
        jt*jt - jt*jt*jt/38710000 + math.degrees(longitude)
    if (mst > 0):
        while (mst > 360.0):
            mst = mst - 360.0
    else:
        while (mst < 0.0):
            mst = mst + 360.0

    return mst


def Half_Angle(RA):
    lst = LST(longitude)
    HA = lst-RA
    while HA < 0 or HA > 360:
        if HA < 0:
            HA = HA+360
        else:
            HA = HA-360
    return HA


def Main_Converter(HA, DEC, latitude):
    al1 = (math.sin(DEC)*math.sin(latitude))
    al2 = math.cos(DEC)*math.cos(latitude)*math.cos(math.radians(HA))
    ALT = math.degrees(math.asin(al1+al2))
    ALT1 = math.radians(ALT)
    a1 = math.sin(DEC) - (math.sin(ALT1)*math.sin(latitude))
    a2 = (math.cos(ALT1)*math.cos(latitude))
    A = math.degrees(math.acos(a1/a2))
    if math.sin(HA) < 0:
        AZ = A
    else:
        AZ = 360-A
    file = open("alt-az.txt", "a")
    file.write(str(ALT)+" "+str(AZ)+'\n')
    file.close()


def convert():
    i = 1
    while i <= 1800:
        HA = Half_Angle(RA)
        UT = time.gmtime()
        Main_Converter(HA, DEC, latitude)
        time.sleep(timedelay)
        i += 1
    return i


convert()
