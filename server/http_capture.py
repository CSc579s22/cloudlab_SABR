#!/usr/bin/env python

from __future__ import division
from scapy.all import *

from scapy.layers import http
import pymongo
import mpd_insert
from collections import defaultdict
from datetime import datetime

stars = lambda n: "*" * n

MAX_CACHE_SIZE = 4982162063

# MAX_CACHE_SIZE =  2491081032


hit_count = {"89283": 0, "262537": 0, "791182": 0, "2484135": 0, "4219897": 0}
current_cache_size = 0
estimated_cache_size = current_cache_size


def http_header(packet):
    http_packet = str(packet)
    if http_packet.find('GET'):
        return GET_print(packet)


# This API will read a list of MPDs and parse them into data structures
def GET_print(packet):
    """
     Performing MongoDB initialization here
    """
    http_layer = packet.getlayer(http.HTTPRequest)
    http_packet = http_layer.fields
    # print'\n%s'%http_packet["Path"]
    print("\n%s" % http_packet["Path"])

    try:
        client = pymongo.MongoClient()
        print("Connected successfully again!!!")
    except pymongo.errors.ConnectionFailure, e:
        print("Could not connect to MongoDB sadly: %s" % e)
    db = client.cachestatus
    table = db.cache1
    f_path = (str(http_packet["Path"])[1:])
    res = table.find_one({"urn": f_path})
    try:
        client = pymongo.MongoClient()
        print("Connected successfully again!!!")
    except pymongo.errors.ConnectionFailure, e:
        print("Could not connect to MongoDB sadly: %s" % e)
    db2 = client.cachestatus
    table2 = db2.cache1
    mpdinfo2 = db2.mpdinfo
    get_mpd = mpdinfo2.find_one({"urn": (str(f_path))})
    if get_mpd is not None:
        hit_count[str(get_mpd['quality'])] += 1
    print hit_count
    # for res in table.find({"urn": str(http_packet["Path"])}).limit(1):
    if "init" not in f_path and "mpd" not in f_path:
        if res is None:
            print('Generating a cache miss\n')

        else:
            print('**************************Generating a cache hit\n**********************')
            cache_hit(res)


def cache_hit(res):
    try:
        client = pymongo.MongoClient()
        print("Connected successfully again!!!")
    except pymongo.errors.ConnectionFailure, e:
        print("Could not connect to MongoDB sadly: %s" % e)
    db = client.cachestatus
    table = db.cache1
    curr_hit = int(res['hit_rate'])
    res2 = table.find_one({'$query': {}, '$orderby': {"date": -1}})
    if res2 is not None:
        print "**********HIT \t Get cache_size\n"
        # print res2['cache_size']
        # print res2['qual_no']

    up_date = table.update_one({'urn': res['urn']}, {'$inc': {"hit_rate": 1}})
    up_date = table.update_one({'urn': res['urn']},
                               {'$set': {'date': datetime.utcnow(), 'cache_size': res2['cache_size']}})
    # print "Cache hit\n"


sniff(iface='eth1', prn=http_header, store=0, lfilter=lambda p: "GET" in str(p), filter="tcp[32:4] = 0x47455420")
# sniff(iface='eth1', prn=http_header, lfilter=lambda p: "GET" in str(p), filter="tcp dst port 80")
