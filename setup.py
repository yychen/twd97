#!/usr/bin/env python
from distutils.core import setup

setup(name='twd97',
      version='0.1.0',
      description='Python converter between TWD97 and WGS84',
      license='MIT',
      author='Tom Chiung-ting Chen',
      author_email='ctchen@gmail.com',
      url='https://github.com/yychen/twd97',
      download_url='https://github.com/yychen/twd97',
      packages=['twd97'],
      keywords=[
          'lat', 'lng', 'latitude', 'longitude', 'x', 'y', 'xy', 'latlng',
          'twd97', 'wgs84', 'universal transverse mercator', 'UCM',
      ],
      classifiers=[
          'Topic :: Scientific/Engineering :: GIS',
          'Topic :: Software Development :: Libraries :: Python Modules'
          'Programming Language :: Python :: 2.7',
          'Intended Audience :: Developers',
      ],
      scripts=[
          'twd97/bin/twd97conv.py',
      ],
     )
