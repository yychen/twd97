twd97
=====

An easy converter between the different coordinate systems TWD97 and WGS84.
The algorithm used in this implementation is from [Universal Transverse Mercator coordinate system (wikipedia page)](http://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system), with the parameters specified from [Satellite Survey Center, Department of Land Administration, MOI](http://www.gps.moi.gov.tw/SSCenter/Introduce/IntroducePage.aspx?Page=GPS9).

twd97 is a MIT Licensed library, written in Python.

    >>> twd97.towgs84(248170.787, 2652129.936)
    (23.97387462949248, 120.98202461950673)

    >>> twd97.fromwgs84(23.973875, 120.982025)
    (248170.82582552364, 2652129.9773471127)


Installation
------------

To install twd97, simply type:

    $ pip install twd97

Documentation
-------------

### Convert coordinates from TWD97 to WGS84
#### Different formats returned
There are 5 types of formats that can be returned.

-  degdec (default) Decimal degrees.
-  dms - A tuple with degrees, minutes and seconds.
-  dmsstr - A string presentation of degrees, minutes and seconds. (DDD°MM'SSS.SSSSS")
-  mindec - A tuple with degrees and minutes.
-  mindecstr - A string presentation of degrees and minutes. (DDD°MMM.MMMMM")

#### Penghu, Kinmen and Matsu
The base longitude (lng0) is different for Penghu, Kinmen and Matsu, which is 119 degrees. Set the pkm parameter to True if the coordinates are in this area.

#### Sample codes

    >>> import twd97
    >>> twd97.towgs84(248170.787, 2652129.936)
    (23.97387462949248, 120.98202461950673)
    
    >>> twd97.towgs84(248170.787, 2652129.936, presentation='dms')
    ((23, 58, 25.94866617293377), (120, 58, 55.28863022423252))
    
    >>> twd97.towgs84(248170.787, 2652129.936, pkm=True, presentation='dms')
    ((23, 58, 25.94866617293377), (118, 58, 55.28863022423252))
    
    >>> twd97.towgs84(248170.787, 2652129.936, presentation='dmsstr')
    (u'23\xb058\'25.948666"', u'120\xb058\'55.288630"')


### Convert coordinates from WGS84 to TWD97
You can use the following presentation of WGS84 for the input:

- DDD°MM'SSS.SSSSS" (unicode)
- DDD°MMM.MMMMM' (unicode)
- DDD.DDDDD (unicode or float)

#### Penghu, Kinmen and Matsu
The base longitude (lng0) is different for Penghu, Kinmen and Matsu, which is 119 degrees. Set the pkm parameter to True if the coordinates are in this area.

#### Sample codes

    >>> import twd97
    >>> twd97.fromwgs84(23.973875, 120.982025)
    (248170.82582552364, 2652129.9773471127)
    
    >>> twd97.fromwgs84(23.973875, 120.982025, pkm=True)
    (451587.6591322426, 2653547.9133169423)

    >>> twd97.fromwgs84(u"25° 0.899'", u"121° 32.037'")
    (303888.3088162089, 2767543.3314042403)

### Command line tool
A handy command line tool is also included. You can use it to have a quick conversion between the two coordinate systems.

    usage: twd97conv.py [-h] [-w EAST,NORTH] [-t lat,lng] [-p presentation] [-pkm]
    
    The TWD97 and WGS84 converter
    
    optional arguments:
      -h, --help       show this help message and exit
      -w EAST,NORTH    TWD97 to WGS84, format: E,N
      -t lat,lng       WGS84 to TWD97, format: lat,lng (DDD.ddddd,
                       DDD°MM'SSS.SSSSS" or DDD°MMM.MMMMM')
      -p presentation  presentation for returned WGS84
      -pkm             Penghu, Kinmen or Matsu coordinates
    
    $ twd97conv.py -t "25° 0.899', 121° 32.037'"
    303888.308816,2767543.331404
    
    $ twd97conv.py -t 25.014983,121.533925
    303885.786058,2767543.284539
    
    $ twd97conv.py -w 303888.308816,2767543.331404
    25.014983,121.533925
    
    $ twd97conv.py -w 303888.308816,2767543.331404 -p dmsstr
    25°0'53.940338",121°32'2.128396"
    
    $ twd97conv.py -w 303888.308816,2767543.331404 -p mindecstr
    25°0.899006',121°32.035473'
