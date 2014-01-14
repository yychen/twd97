# -*- coding: utf-8 -*- 
presentations = ['todegdec', 'todms', 'todmsstr', 'tomindec', 'tomindecstr']
__all__ = ['towgs84', 'fromwgs84'] + presentations
from math import radians, degrees, pow, sin, cos, sinh, cosh, asin, acos, atan, atanh

import argparse
import re
import sys

"""
Based on http://www.gps.moi.gov.tw/SSCenter/Introduce/IntroducePage.aspx?Page=GPS9
TWD97 has E0 = 250000m, k0 = 0.9999, a = 6378137m, lng0 = 121 and f = 1 / 298.257222101
If it is in Penghu, Kinmen or Matsu, lng0 should be 119

The formulas are based on http://en.wikipedia.org/wiki/Universal_transverse_Mercator
"""

a = 6378.137
f = 1 / 298.257222101
k0 = 0.9999
N0 = 0
E0 = 250.000
lng0 = radians(121)
lng0pkm = radians(119)

n = f / (2-f)
A = a / (1+n) * (1 + pow(n,2)/4.0 + pow(n,4)/64.0)
alpha1 = n/2 - 2*pow(n,2)/3.0 + 5*pow(n,3)/16.0
alpha2 = 13*pow(n,2)/48.0 - 3*pow(n,3)/5.0
alpha3 = 61*pow(n,3)/240.0
beta1 = n/2 - 2*pow(n,2)/3.0 + 37*pow(n,3)/96.0
beta2 = pow(n,2)/48.0 + pow(n,3)/15.0
beta3 = 17*pow(n,3)/480.0
delta1 = 2*n - 2*pow(n,2)/3.0 - 2*pow(n,3)
delta2 = 7*pow(n,2)/3.0 - 8*pow(n,3)/5.0
delta3 = 56*pow(n,3)/15.0

dms_re = re.compile(u'(?P<degrees>[\+\-]?[0-9]+)°\s?(?P<minutes>\d+)\'\s?(?P<seconds>[0-9.]+)"')
mindec_re = re.compile(u'(?P<degrees>[\+\-]?[0-9]+)°\s?(?P<minutes>[0-9.]+)\'')

def todegdec(origin):
    """
    Convert from [+/-]DDD°MMM'SSS.SSSS" or [+/-]DDD°MMM.MMMM' to [+/-]DDD.DDDDD
    """

    # if the input is already a float (or can be converted to float)
    try:
        return float(origin)
    except ValueError:
        pass

    # DMS format
    m = dms_re.search(origin)
    if m:
        degrees = int(m.group('degrees'))
        minutes = float(m.group('minutes'))
        seconds = float(m.group('seconds'))

        return degrees + minutes / 60 + seconds / 3600

    # Degree + Minutes format
    m = mindec_re.search(origin)
    if m:
        degrees = int(m.group('degrees'))
        minutes = float(m.group('minutes'))

        return degrees + minutes / 60

def tomindec(origin):
    """
    Convert [+/-]DDD.DDDDD to a tuple (degrees, minutes)
    """

    origin = float(origin)
    degrees = int(origin)
    minutes = (origin % 1) * 60

    return degrees, minutes

def tomindecstr(origin):
    """
    Convert [+/-]DDD.DDDDD to [+/-]DDD°MMM.MMMM'
    """

    degrees, minutes = tomindec(origin)
    return u'%d°%f\'' % (degrees, minutes)

def todms(origin):
    """
    Convert [+/-]DDD.DDDDD to a tuple (degrees, minutes, seconds)
    """

    degrees, minutes = tomindec(origin)
    seconds = (minutes % 1) * 60

    return degrees, int(minutes), seconds

def todmsstr(origin):
    """
    Convert [+/-]DDD.DDDDD to [+/-]DDD°MMM'DDD.DDDDD"
    """

    degrees, minutes, seconds = todms(origin)
    return u'%d°%d\'%f"' % (degrees, minutes, seconds)

def towgs84(E, N, pkm=False, presentation=None):
    """
    Convert coordintes from TWD97 to WGS84

    The east and north coordinates should be in meters and in float
    pkm true for Penghu, Kinmen and Matsu area
    You can specify one of the following presentations of the returned values:
        dms - A tuple with degrees (int), minutes (int) and seconds (float)
        dmsstr - [+/-]DDD°MMM'DDD.DDDDD" (unicode)
        mindec - A tuple with degrees (int) and minutes (float)
        mindecstr - [+/-]DDD°MMM.MMMMM' (unicode)
        (default)degdec - DDD.DDDDD (float)
    """

    _lng0 = lng0pkm if pkm else lng0

    E /= 1000.0
    N /= 1000.0
    epsilon = (N-N0) / (k0*A)
    eta = (E-E0) / (k0*A)

    epsilonp = epsilon - beta1*sin(2*1*epsilon)*cosh(2*1*eta) - \
                         beta2*sin(2*2*epsilon)*cosh(2*2*eta) - \
                         beta3*sin(2*3*epsilon)*cosh(2*3*eta)
    etap = eta - beta1*cos(2*1*epsilon)*sinh(2*1*eta) - \
                 beta2*cos(2*2*epsilon)*sinh(2*2*eta) - \
                 beta3*cos(2*3*epsilon)*sinh(2*3*eta)
    sigmap = 1 - 2*1*beta1*cos(2*1*epsilon)*cosh(2*1*eta) - \
                 2*2*beta2*cos(2*2*epsilon)*cosh(2*2*eta) - \
                 2*3*beta3*cos(2*3*epsilon)*cosh(2*3*eta)
    taup = 2*1*beta1*sin(2*1*epsilon)*sinh(2*1*eta) + \
           2*2*beta2*sin(2*2*epsilon)*sinh(2*2*eta) + \
           2*3*beta3*sin(2*3*epsilon)*sinh(2*3*eta)

    chi = asin(sin(epsilonp) / cosh(etap))

    latitude = chi + delta1*sin(2*1*chi) + \
                     delta2*sin(2*2*chi) + \
                     delta3*sin(2*3*chi)

    longitude = _lng0 + atan(sinh(etap) / cos(epsilonp))

    func = None
    presentation = 'to%s' % presentation if presentation else None
    if presentation in presentations:
        func = getattr(sys.modules[__name__], presentation)

    if func and func != 'todegdec':
        return func(degrees(latitude)), func(degrees(longitude))

    return (degrees(latitude), degrees(longitude))

def fromwgs84(lat, lng, pkm=False):
    """
    Convert coordintes from WGS84 to TWD97

    pkm true for Penghu, Kinmen and Matsu area
    The latitude and longitude can be in the following formats:
        [+/-]DDD°MMM'SSS.SSSS" (unicode)
        [+/-]DDD°MMM.MMMM' (unicode)
        [+/-]DDD.DDDDD (string, unicode or float)
    The returned coordinates are in meters
    """

    _lng0 = lng0pkm if pkm else lng0

    lat = radians(todegdec(lat))
    lng = radians(todegdec(lng))

    t = sinh((atanh(sin(lat)) - 2*pow(n,0.5)/(1+n)*atanh(2*pow(n,0.5)/(1+n)*sin(lat))))
    epsilonp = atan(t/cos(lng-_lng0))
    etap = atan(sin(lng-_lng0) / pow(1+t*t, 0.5))

    E = E0 + k0*A*(etap + alpha1*cos(2*1*epsilonp)*sinh(2*1*etap) + 
                          alpha2*cos(2*2*epsilonp)*sinh(2*2*etap) +
                          alpha3*cos(2*3*epsilonp)*sinh(2*3*etap))
    N = N0 + k0*A*(epsilonp + alpha1*sin(2*1*epsilonp)*cosh(2*1*etap) +
                              alpha2*sin(2*2*epsilonp)*cosh(2*2*etap) +
                              alpha3*sin(2*3*epsilonp)*cosh(2*3*etap))

    return E*1000, N*1000
