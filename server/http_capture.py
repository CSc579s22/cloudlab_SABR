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
				 
#MAX_CACHE_SIZE =  2491081032

				 
				 
hit_count={"89283":0,"262537":0,"791182":0,"2484135":0,"4219897":0}
current_cache_size=0
estimated_cache_size = current_cache_size
'''
mpd_name = "/var/www/html/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/"
for i in range (1,51):
	f_name = mpd_name + "BigBuckBunny_2s_mod" + str(i) + ".mpd"
	#print f_name
	mpd_insert.read_mpd(f_name)
'''

def http_header(packet):
        http_packet=str(packet)
        if http_packet.find('GET'):
                return GET_print(packet)
#This API will read a list of MPDs and parse them into data structures
def GET_print(packet):
	
	'''
	 Performing MongoDB initialization here

	'''    
	http_layer = packet.getlayer(http.HTTPRequest)
	http_packet = http_layer.fields
	print'\n%s'%http_packet["Path"]
			
	try:
		client=pymongo.MongoClient()
		print( "Connected successfully again!!!")
	except pymongo.errors.ConnectionFailure, e:
		print("Could not connect to MongoDB sadly: %s" % e)
	db = client.cachestatus
	table = db.cache1
	f_path = (str(http_packet["Path"])[1:])
	res = table.find_one({"urn": f_path})
	try:
		client=pymongo.MongoClient()
		print( "Connected successfully again!!!")
	except pymongo.errors.ConnectionFailure, e:
		print("Could not connect to MongoDB sadly: %s" % e)
	db2 = client.cachestatus
	table2 = db2.cache1
	mpdinfo2 = db2.mpdinfo
	get_mpd = mpdinfo2.find_one({"urn":(str(f_path))})
	if get_mpd is not None:
		hit_count[str(get_mpd['quality'])]+=1
	print hit_count
	#for res in table.find({"urn": str(http_packet["Path"])}).limit(1):
	if "init" not in f_path and "mpd" not in f_path:
		
		if res is None:
			print('Generating a cache miss\n')
			cache_miss(f_path)
		else: 
			print('**************************Generating a cache hit\n**********************')
			cache_hit(res)

		
def cache_hit(res):
		try:
			client=pymongo.MongoClient()
			print( "Connected successfully again!!!")
		except pymongo.errors.ConnectionFailure, e:
			print("Could not connect to MongoDB sadly: %s" % e)
		db = client.cachestatus
		table = db.cache1
		curr_hit = int(res['hit_rate'])
		res2 = table.find_one({'$query': {}, '$orderby': {"date": -1}})
		if res2 is not None:
			print "**********HIT \t Get cache_size\n"
			#print res2['cache_size']
			#print res2['qual_no']
			
		up_date = table.update_one({'urn': res['urn']}, {'$inc': {"hit_rate": 1}})
		up_date = table.update_one({'urn': res['urn']}, {'$set': {'date': datetime.utcnow(), 'cache_size':res2['cache_size']}})
		#print "Cache hit\n"
		
		
		'''
	return "\n".join((
		stars(40) + "GET PACKET" + stars(40),
		"\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n")),
		stars(90)))
	sniff(
	iface='eth1',
	prn=GET_print,
	lfilter=lambda p: "GET" in str(p),
	filter="tcp port 80")
	'''
'''
def find_between_r( s, first, last ):
try:
	start = s.rindex( first ) + len( first )
	end = s.rindex( last, start )
	return s[start:end]
except ValueError:
	return ""
	
def parse_urn(urn):
	seg_info = []
	urnparse=urn.split("/")
	bw_str=urnparse[length(urnparse)-2]
	seg_info[0] = int(find_between(bw_str,"_","bps"))
	seg_info[1] = int(find_between(bw_str,"_2s",".m4s"))
	
'''
def cache_miss(f_path):
	
	global current_cache_size, estimated_cache_size 
	try:
		client=pymongo.MongoClient()
		print( "Connected successfully again!!!")
	except pymongo.errors.ConnectionFailure, e:
		print("Could not connect to MongoDB sadly: %s" % e)
	db = client.cachestatus
	table = db.cache1
	mpdinfo = db.mpdinfo
	print "Cache miss\n"
	evict_ids = []
	cache_size_res = table.find_one()
	#current_cache_size = int(cache_size_res['cache_size'])
	print ("Cache key\n")
	print f_path
	get_mpd = mpdinfo.find_one({"urn":(str(f_path))})
	if get_mpd is None:
		print "File not found\n"
	new_seg_size = get_mpd['seg_size'] 
	evict = False
	evict_seg_size = 0
	
	res = table.find_one({'$query': {}, '$orderby': {"date": -1}})
	if res is not None:
		#print "Get cache_size\n"
		#print res['cache_size']
		estimated_cache_size = res['cache_size'] + new_seg_size
	else:
		estimated_cache_size+=new_seg_size
		
				
	# Perform Cache Eviction
	while evict is False:
		for res in table.find().sort([("date", pymongo.ASCENDING)]).limit(1):
			print "Non empty cache\n"
			if res['date'] is not None: 
				if estimated_cache_size > MAX_CACHE_SIZE:
					table.remove({"date": res["date"]})
					estimated_cache_size-=res['seg_size']
				else:
					evict = True
		if table.find_one() is None:
			break
	# Update New Entry to MongoDB
	#estimated_cache_size+=new_seg_size
	if(table.find_one({"urn": f_path})) is None:
		post = {"urn": f_path, "seg_no": get_mpd['seg_no'], "qual_no": get_mpd['quality'], "seg_size": new_seg_size, "cache_size":estimated_cache_size, "hit_rate":1, "date": datetime.utcnow()}
		#print "Inserting URN: %s \n New cache Size %d "%(f_path,estimated_cache_size)
		post_id = table.insert_one(post).inserted_id
	else:
		print "Content present in Cache. Don't insert\n"
	
	return  hit_count
sniff(iface='eth1', prn=http_header, store=0,lfilter=lambda p: "GET" in str(p), filter="tcp[32:4] = 0x47455420")
#sniff(iface='eth1', prn=http_header, lfilter=lambda p: "GET" in str(p), filter="tcp dst port 80")

