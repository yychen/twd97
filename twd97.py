#!/usr/bin/env python
from math import radians, degrees, pow, sin, cos, sinh, cosh, asin, acos, atan, atanh

import argparse

"""
Based on http://www.gps.moi.gov.tw/SSCenter/Introduce/IntroducePage.aspx?Page=GPS9
TWD97 has E0 = 250000m, k0 = 0.9999, a = 6378137m and f = 1 / 298.257222101

The formulas are based on http://en.wikipedia.org/wiki/Universal_transverse_Mercator
"""

a = 6378.137
f = 1 / 298.257222101
k0 = 0.9999
N0 = 0
E0 = 250.000
lng0 = radians(121)

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

def towgs84(E, N):
    """
    Convert coordintes from TWD97 to WGS84

    The east and north coordinates should be in meters
    Returned latitude and longitude are in decimal degrees (DDD.ddddd)
    """

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

    longitude = lng0 + atan(sinh(etap) / cos(epsilonp))
    return degrees(latitude), degrees(longitude)

def fromwgs84(lat, lng):
    """
    Convert coordintes from WGS84 to TWD97

    The latitude and longitude should be in decimal degrees format (DDD.ddddd)
    The returned coordinates are in meters
    """

    t = sinh((atanh(sin(lat)) - 2*pow(n,0.5)/(1+n)*atanh(2*pow(n,0.5)/(1+n)*sin(lat))))
    epsilonp = atan(t/cos(lng-lng0))
    etap = atan(sin(lng-lng0) / pow(1+t*t, 0.5))

    E = E0 + k0*A*(etap + alpha1*cos(2*1*epsilonp)*sinh(2*1*etap) + 
                          alpha2*cos(2*2*epsilonp)*sinh(2*2*etap) +
                          alpha3*cos(2*3*epsilonp)*sinh(2*3*etap))
    N = N0 + k0*A*(epsilonp + alpha1*sin(2*1*epsilonp)*cosh(2*1*etap) +
                              alpha2*sin(2*2*epsilonp)*cosh(2*2*etap) +
                              alpha3*sin(2*3*epsilonp)*cosh(2*3*etap))

    return E*1000, N*1000

def main():
    parser = argparse.ArgumentParser(description='The TWD97 and WGS84 converter')
    parser.add_argument('-w', help='TWD97 to WGS84, format: E,N', metavar='EAST,NORTH')
    parser.add_argument('-t', help='WGS84 to TWD97, format: lat,lng (in decimal degrees DDD.ddddd)', metavar='lat,lng')

    args = parser.parse_args()

    if args.w:
        E, N = args.w.split(',')
        lat, lng = towgs84(float(E), float(N))

        print u'%f,%f' % (lat, lng)
    elif args.t:
        lat, lng = args.t.split(',')
        E, N = fromwgs84(radians(float(lat)), radians(float(lng)))

        print u'%f,%f' % (E, N)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
