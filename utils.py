import math

import matplotlib.pyplot as plt

from astropy import units as u
from astropy.coordinates import Longitude

EARTH_INC = 23.4392911

def get_ascendant(time, location):
    lat = math.radians(location.lat.value)
    lst = math.radians(time.sidereal_time('apparent', longitude=location.lon).deg)
    inc = math.radians(EARTH_INC)
    A = -1*math.cos(lst)
    B = math.sin(lst)*math.cos(inc)
    C = math.tan(lat)*math.sin(inc)
    ascendant = math.degrees(math.atan2(A,(B+C)))

    if ascendant < 180:
        ascendant += 180
    else:
        ascendant -= 180
    return ascendant*u.deg


def get_midheaven(time, location):
    lst = math.radians(time.sidereal_time('apparent', longitude=location.lon).deg)
    inc = math.radians(EARTH_INC)
    A = math.tan(lst)
    B = math.cos(inc)
    midheaven = math.degrees(math.atan(A/B))
    return midheaven*u.deg


def get_cusps(ascendant, midheaven):
    try:
        ascendant = ascendant.value
    except:
        ascendant = float(ascendant)
    try:
        midheaven = midheaven.value
    except:
        midheaven = float(midheaven)

    asc_deg = ascendant+(180-ascendant)
    mid_deg = midheaven+(180-ascendant)

    # nb asc_dec == 180
    d1 = (asc_deg-mid_deg)/3.
    d2 = (mid_deg-(180-asc_deg))/3.

    c1 = asc_deg

    c2 = (c1 + d2)%360
    c3 = (c2 + d2)%360
    c4 = (c3 + d2)%360

    c5 = (c4 + d1)%360
    c6 = (c5 + d1)%360
    c7 = (c6 + d1)%360

    c8 = (c7 + d2)%360
    c9 = (c8 + d2)%360
    c10 = (c9 + d2)%360

    c11 = (c10 + d1)%360
    c12 = (c11 + d1)%360
    c13 = (c12 + d1)%360

    return [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13]



def get_house(deg, ascendant, midheaven):
    try:
        deg = deg.value
    except:
        deg = float(deg)
    try:
        ascendant = ascendant.value
    except:
        ascendant = float(ascendant)
    try:
        midheaven = midheaven.value
    except:
        midheaven = float(midheaven)

    c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13 = get_cusps(ascendant, midheaven)

    if c1 <= (deg+(180-ascendant))%360 < c2:
        house = 1
    elif c2 <= (deg+(180-ascendant))%360 < c3:
        house = 2
    elif c3 <= (deg+(180-ascendant))%360 < c4:
        house = 3
    elif c4 <= (deg+(180-ascendant))%360 < c5:
        house = 4
    elif c5 <= (deg+(180-ascendant))%360 < c6:
        house = 5
    elif c6 <= (deg+(180-ascendant))%360 < c7:
        house = 6
    elif c7 <= (deg+(180-ascendant))%360 < c8:
        house = 7
    elif c8 <= (deg+(180-ascendant))%360 < c9:
        house = 8
    elif c9 <= (deg+(180-ascendant))%360 < c10:
        house = 9
    elif c10 <= (deg+(180-ascendant))%360 < c11:
        house = 10
    elif c11 <= (deg+(180-ascendant))%360 < c12:
        house = 11
    elif c12 <= (deg+(180-ascendant))%360 < c13:
        house = 12
    else:
        raise ValueError
    return house


def get_zodiac(deg):
    try:
        deg = deg.value
    except:
        deg = float(deg)

    if 0 <= deg < 30:
        sign = 'Aries'
    elif 30 <= deg < 60:
        sign = 'Taurus'
    elif 60 <= deg < 90:
        sign = 'Gemini'
    elif 90 <= deg < 120:
        sign = 'Cancer'
    elif 120 <= deg < 150:
        sign = 'Leo'
    elif 150 <= deg < 180:
        sign = 'Virgo'
    elif 180 <= deg < 210:
        sign = 'Libra'
    elif 210 <= deg < 240:
        sign = 'Scorpio'
    elif 240 <= deg < 270:
        sign = 'Sagittarius'
    elif 270 <= deg < 300:
        sign = 'Capricorn'
    elif 300 <= deg < 300:
        sign = 'Aquarius'
    elif 330 <= deg < 360:
        sign = 'Pisces'
    else:
        raise ValueError
    return sign


def astrol_coords(deg):
    try:
        deg = deg.value
        lon = Longitude(deg)
    except:
        deg = float(deg)
        lon = Longitude(deg*u.deg)

    d,m,s = lon.dms
    sign = get_zodiac(deg)

    return '{: >2.0f} {} {: >2.0f}′ {: >2.0f}″'.format(d%30,sign[0:3],m,s)
    #return '{:.0f} {} {:.0f}′ {:.0f}″'.format(d%30,sign[0:3],m,s)









def plot_circle(r):

    x = []
    y = []

    for i in range(360+1):
        x.append(r*math.cos(math.radians(i)))
        y.append(r*math.sin(math.radians(i)))

    plt.plot(x, y, color='k')
    return