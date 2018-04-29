import math
from collections import OrderedDict

import matplotlib.pyplot as plt

from astropy import units as u
from astropy.time import Time
from astropy.coordinates import get_body, SkyCoord, EarthLocation, AltAz, Longitude

from astroplan import Observer


EARTH_INC = 23.4392911

# enter planet name
# planet_name = None
# while planet_name is None:
#     in_name = input('Enter name of planet: ').capitalize()
#     try:
#         planet_coord = get_body(in_name, Time.now())
#         planet_name = in_name
#     except:
#         print('Invalid planet name: "{}"'.format(in_name))

loc_name = None
while loc_name is None:
    in_name = 'Manchester' #input('Enter name of city on Earth: ').capitalize()
    try:
        raise Exception
        loc_coord = EarthLocation.of_address(in_name)
        loc_name = in_name
    except:
        print('Can not find location: "{}"'.format(in_name))
        print('Defaulting to Manchester...')
        loc_name = 'Manchester'
        loc_coord = EarthLocation(lat=53.4807593*u.deg, lon=-2.2426305*u.deg, height=0)

print(loc_coord.lat, loc_coord.lon)
obs = Observer(location=loc_coord)

tt = Time('2018-04-28 14:00:00')
print(tt)


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


#plot sun
plt.axis('equal')
plt.axis('off')

asc = get_ascendant(tt, loc_coord)
print('Ascendant \t\t{:.2f} \t{}'.format(asc, astrol_coords(asc)))

plt.scatter(35*math.cos(math.radians((asc.value+(180-asc.value))%360)),
            35*math.sin(math.radians((asc.value+(180-asc.value))%360)),
            marker='o', color='white', s=600,zorder=88)
plt.text(35*math.cos(math.radians((asc.value+(180-asc.value))%360)),
         35*math.sin(math.radians((asc.value+(180-asc.value))%360)),
         'Asc', fontsize=14, ha='center', va='center', color='0.5',zorder=89)


dsc = ((asc.value+180)%360)*u.deg
print('Descendant \t\t{:.2f} \t{}'.format(dsc, astrol_coords(dsc)))

mid = get_midheaven(tt, loc_coord)
print('Midheaven \t\t{:.2f} \t{}'.format(mid, astrol_coords(mid)))

plt.scatter(35*math.cos(math.radians((mid.value+(180-asc.value))%360)),
            35*math.sin(math.radians((mid.value+(180-asc.value))%360)),
            marker='o', color='white', s=600,zorder=88)
plt.text(35*math.cos(math.radians((mid.value+(180-asc.value))%360)),
         35*math.sin(math.radians((mid.value+(180-asc.value))%360)),
         'Mᶜ', fontsize=14, ha='center', va='center', color='0.5',zorder=89)

ic = ((mid.value+180)%360)*u.deg
print('Imum coeli \t\t{:.2f} \t{}'.format(ic, astrol_coords(ic)))



# Cycle over houses
cusps = get_cusps(asc, mid)
for i in range(len(cusps[:-1])):
    c = cusps[i]
    if i+1 in [1,4,7,10]:
        style = '-'
    else:
        style = ':'
    plt.plot([10*math.cos(math.radians(c)%360),40*math.cos(math.radians((c)%360))],
             [10*math.sin(math.radians(c)%360),40*math.sin(math.radians((c)%360))],
             linestyle=style, color='0.5')
    plt.text(20*math.cos(math.radians((c+15)%360)),
             20*math.sin(math.radians((c+15)%360)),
             int(i+1)%13, fontsize=10, ha='center', va='center', color='0.5')



# Cycle over zodiac
for i,s in zip([0,30,60,90,120,150,180,210,240,270,300,330],
               [' ♈ ',' ♉ ',' ♊ ',' ♋ ',' ♌ ',' ♍ ',' ♎ ',' ♏ ',' ♐ ',' ♑ ',' ♒ ',' ♓ ']):
    i+=180-asc.value
    plt.plot([40*math.cos(math.radians((i)%360)),60*math.cos(math.radians((i)%360))],
             [40*math.sin(math.radians((i)%360)),60*math.sin(math.radians((i)%360))],
             color='0.5')
    for j in [10,20]:
        plt.plot([40*math.cos(math.radians((i+j)%360)),44*math.cos(math.radians((i+j)%360))],
                [40*math.sin(math.radians((i+j)%360)),44*math.sin(math.radians((i+j)%360))],
                linestyle='-', color='0.5')
    for j in [5,15,25]:
        plt.plot([40*math.cos(math.radians((i+j)%360)),42*math.cos(math.radians((i+j)%360))],
                [40*math.sin(math.radians((i+j)%360)),42*math.sin(math.radians((i+j)%360))],
                linestyle='-', color='0.5')
    for j in [1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19,21,22,23,24,26,27,28,29]:
        plt.plot([40*math.cos(math.radians((i+j)%360)),41*math.cos(math.radians((i+j)%360))],
                [40*math.sin(math.radians((i+j)%360)),41*math.sin(math.radians((i+j)%360))],
                linestyle='-', color='0.5')


    if s in [' ♈ ',' ♌ ',' ♐ ']:
        element = 'tomato' # fire
    elif s in [' ♉ ',' ♍ ',' ♑ ']:
        element = 'darkseagreen' # earth
    elif s in [' ♊ ',' ♎ ',' ♒ ']:
        element = 'goldenrod' # air
    elif s in [' ♋ ',' ♏ ',' ♓ ']:
        element = 'royalblue' # water

    plt.text(50*math.cos(math.radians((i+15)%360)),
             50*math.sin(math.radians((i+15)%360)),
             s, fontsize=30, ha='center', va='center', color=element)


# circles
plot_circle(10)
plot_circle(40)
plot_circle(60)



#planets = ['☉ Sun', '☾ Moon', '☿ Mercury', '♀ Venus', '♂ Mars', '♃ Jupiter', '♄ Saturn', '⛢ Uranus', '♆ Neptune']

planets = {'Sun':{'symbol':' ☉ ', 'pos':1},
           'Moon':{'symbol':' ☾ ', 'pos':2},
           'Mercury':{'symbol':' ☿ ', 'pos':3},
           'Venus':{'symbol':' ♀ ', 'pos':4},
           'Mars':{'symbol':' ♂ ', 'pos':5},
           'Jupiter':{'symbol':' ♃ ', 'pos':6},
           'Saturn':{'symbol':' ♄ ', 'pos':7},
           'Uranus':{'symbol':' ♅ ', 'pos':8},
           'Neptune':{'symbol':' ♆ ', 'pos':9},
            }

planets = OrderedDict(sorted(planets.items(), key=lambda t: t[1]['pos']))

# Cycle over planets
for name in planets:
    coord = get_body(name, tt)
    coord.equinox = tt

    planets[name]['coord'] = coord
    planets[name]['ang'] = coord.geocentrictrueecliptic.lon
    planets[name]['sign'] = get_zodiac(planets[name]['ang'])
    planets[name]['astrol'] = astrol_coords(planets[name]['ang'])
    planets[name]['house'] = get_house(planets[name]['ang'],asc, mid)

txt = ''
for name in planets:
    print('{: >10}\t\t{:.2f} \t{} \t{:.0f}'.format(name,
                                              planets[name]['ang'],
                                              planets[name]['astrol'],
                                              planets[name]['house']))

    planets[name]['x_pos'] = math.cos(math.radians(planets[name]['ang'].deg+(180-asc.value)))
    planets[name]['y_pos'] = math.sin(math.radians(planets[name]['ang'].deg+(180-asc.value)))


    plt.scatter(40*planets[name]['x_pos'],
                40*planets[name]['y_pos'],
                marker='o', color='white', s=300,zorder=99)
    # plt.text(40*planets[name]['x_pos']+2,
    #          40*planets[name]['y_pos'],
    #          name+'\n'+planets[name]['astrol']+'\n'+str(planets[name]['house']),
    #          zorder=999)
    plt.text(40*planets[name]['x_pos'],
             40*planets[name]['y_pos'],
             planets[name]['symbol'], fontsize=15, color='orange',
             ha='center', va='center', zorder=999)

    #txt += planets[name]['symbol']+' '+name+'\t'+planets[name]['astrol']+'\t'+str(planets[name]['house'])+'\n'
    txt += '{} {: <10}  {}  H{:.0f}\n'.format(planets[name]['symbol'],
                                        name,
                                        planets[name]['astrol'],
                                        planets[name]['house'])


plt.text(50, 40,txt,zorder=999,fontname='DejaVu Sans Mono')


# Aspects
aspects = {'conjunction':{'angle':0, 'color':'green'},
           'sextile':{'angle':60, 'color':'lightseagreen'},
           'square':{'angle':90, 'color':'red'},
           'trine':{'angle':120, 'color':'blue'},
           'opposition':{'angle':180, 'color':'purple'},
           }
aspects = OrderedDict(sorted(aspects.items(), key=lambda t: t[1]['angle']))
all_aspects = []
for name in planets:
    ang = planets[name]['ang']
    for name2 in planets:
        if name2 == name:
            continue
        ang2 = planets[name2]['ang']
        aspect = abs(ang.value-ang2.value)
        if aspect > 180:
            aspect = 360 - aspect
        olim = 8
        if name in ['Sun','Moon'] or name2 in ['Sun','Moon']:
            olim = 10

        for aname in aspects:
            if aspects[aname]['angle']-olim <= abs(aspect) <= aspects[aname]['angle']+olim:
                n1, n2 = sorted([name,name2])

                string = '{} and {} in {} orb {:.0f}°'.format(n1,
                                                           n2,
                                                           aname,
                                                           aspect-aspects[aname]['angle'])

                if string not in all_aspects:
                    print(string)

                    plt.plot([40*planets[name]['x_pos'],40*planets[name2]['x_pos']],
                            [40*planets[name]['y_pos'],40*planets[name2]['y_pos']],
                            color=aspects[aname]['color'])

                    all_aspects += [string]

asp_txt = '\n'.join(sorted(all_aspects))

plt.text(50, -70, asp_txt, zorder=999, fontname='DejaVu Sans Mono')


plt.tight_layout()
plt.show()


dict = {'Sun': ('Taurus', 3),
        'Moon': ('Virgo', 4),
        }