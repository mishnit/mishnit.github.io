import requests
import simplejson
from elasticsearch import Elasticsearch
from datetime import datetime

r = requests.get('http://publicproxy.ias.redbus.in:8001/IASPublic/getAvRoutesObject/122/124/2019-03-29').json()

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

idt=1
for c in r['SearchResponse']:
	# travelsName to multiple buses
	if "fareList" in c.keys() and "busType" in c.keys() and "avSeats" in c.keys() and len(c['fareList'])>0 and c['avSeats']>0:
		es.index(index='busdata', doc_type='travel', id=idt, body={
		'travelsName' : c['travelsName'],
		'sourceName' : "Bus From "+c['sourceName'],
		'destinationName' : "Bus To "+c['destinationName'],
		'busType' : c['busType'],
		'serviceName' : c['serviceName'],
		'depDay' : datetime.strptime(c['depTime'],"%Y-%m-%d %H:%M:%S").strftime("%d %B, %Y"),
		'depTime' : datetime.strptime(c['depTime'],"%Y-%m-%d %H:%M:%S").strftime("%I:%M %p"),
		'arrDay' : datetime.strptime(c['arrTime'],"%Y-%m-%d %H:%M:%S").strftime("%d %B, %Y"),
		'arrTime' : datetime.strptime(c['arrTime'],"%Y-%m-%d %H:%M:%S").strftime("%I:%M %p"),
		'avSeats' : c['avSeats'],
		'avWindowSeats' : c['avWindowSeats'],
		'amount' : c['fareList'][0]['amount']
		})
		idt=idt+1
		print(idt)


#print (es.get(index='busdata', doc_type='travel', id=5))

q='cheapest bus at 9PM'

if 'AM' in q or 'PM' in q:
	print (es.search(index='busdata', q=q)['hits'])

elif "fast" in q:
	print (es.search(index='busdata', q=q)['hits'])

elif "cheap" in q:
	print (es.search(index='busdata', q=q, sort= '_score,amount:desc,avSeats:asc')['hits'])

elif "window" in q: 
	print (es.search(index='busdata', q=q)['hits'])

Todo:
#cheapest bus at 9PM
#fastest bus at 9PM
#windows seat available at 9PM
#from bangalore
#to hyderabad
#No false positive
