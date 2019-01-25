# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     lgeopy.py
   Description :
   Author :       charl
   date：          2018/9/25
-------------------------------------------------
   Change Activity: 2018/9/25:
-------------------------------------------------
"""

from geopy.geocoders import Nominatim

geolocator = Nominatim()
location = geolocator.geocode("浙江大学")
print(location.address)