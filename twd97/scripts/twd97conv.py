#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from twd97.converter import towgs84, fromwgs84, presentations

def main():
    parser = argparse.ArgumentParser(description='The TWD97 and WGS84 converter')
    parser.add_argument('-w', help='TWD97 to WGS84, format: E,N', metavar='EAST,NORTH')
    parser.add_argument('-t', help='WGS84 to TWD97, format: lat,lng (DDD.ddddd, DDD°MM\'SSS.SSSSS" or DDD°MMM.MMMMM\')', metavar='lat,lng')
    parser.add_argument('-p', help='presentation for returned WGS84', metavar='presentation', choices=[x[2:] for x in presentations if x[-3:] == 'str'])
    parser.add_argument('-pkm', help='Penghu, Kinmen or Matsu coordinates', action='store_true')

    args = parser.parse_args()

    if args.w:
        E, N = args.w.split(',')
        lat, lng = towgs84(float(E), float(N), pkm=args.pkm, presentation=args.p)

        if args.p:
            print u'%s,%s' % (lat, lng)
        else:
            print u'%f,%f' % (lat, lng)

    elif args.t:
        nospaces = args.t.decode('utf-8').replace(' ', '')
        lat, lng = nospaces.split(',')
        E, N = fromwgs84(lat, lng, pkm=args.pkm)

        print u'%f,%f' % (E, N)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
