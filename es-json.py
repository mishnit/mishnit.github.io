import requests
import simplejson
from elasticsearch import Elasticsearch

r = requests.get('http://publicproxy.ias.redbus.in:8001/IASPublic/getAvRoutesObject/122/124/2019-03-29').json()

es = Elasticsearch()

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
		'depTime' : c['depTime'],
		'arrTime' : c['arrTime'],
		'amount' : c['fareList'][0]['amount']
		})
	idt+=1

	
es.search(index='busdata', q='Bengaluru to Hyderabad sleeper', 'sort': [{'sourceName': {'destinationName': {'amount': 'avSeats'}}}],)

	
