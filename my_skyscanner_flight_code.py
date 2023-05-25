import requests
import random
import struct
import socket

headers = {
    'authority': 'flights-cb.makemytrip.com',
    'accept': 'application/json',
    'accept-language': 'en-GB,en;q=0.9,kn-IN;q=0.8,kn;q=0.7,en-US;q=0.6',
    'access-control-allow-credentials': 'true',
    'app-ver': '8.0.0',
    'currency': 'inr',
    'device-id': 'c79cabde-fde5-4435-9718-199c8617bdf9',
    'domain': 'in',
    'language': 'eng',
    'lob': 'B2C',
    'mcid': 'c79cabde-fde5-4435-9718-199c8617bdf9',
    'mmt-auth': 'MAT10c0f2617b445e22a9219a4c922e227c8c620444793abb647a98e8957711d06e81d384e6c3b9f14aab48eaedd8fc0dc13P',
    'origin': 'https://www.makemytrip.com',
    'os': 'Android',
    'pfm': 'PWA',
    'referer': 'https://www.makemytrip.com/',
    'region': 'in',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'src': 'mmt',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'x-user-cc': 'IN',
    'x-user-ip': '',
    'x-user-rc': 'NEWDELHI',
}

params = {
    'pfm': 'PWA',
    'lob': 'B2C',
    'cur': 'INR',
    'lcl': 'en',
    'shd': 'true',
    'cc': 'E',
    'pax': 'A-1_C-0_I-0',
    'forwardFlowRequired': 'true',
    'apiTimeStamp': '1683963761190',
    'region': 'in',
    'currency': 'inr',
    'language': 'eng',
    'cmpId': '',
    'it': '',
    'crId': ''
}

url = 'https://flights-cb.makemytrip.com/api/search'

all_india_airport_codes =  ['DEL', 'HYD', 'BOM', 'CCU', 'JAI', 'BLR', 'MAA', 'SXR'] 
#['IXA','AGX','AGR','AKD','IXD','IXV','IXU','IXB','BEK','BPM','IXG','BEP','BUP','BHU','BHJ','BBI','PAB','IXR','CCJ','CBD','IXC','LKO','MAA','BOM','COK','CJB','GOI','NMB','DED','IDR','DBD','DIB','DMU','NAG','GAY','GOP','GWL','HSS','HBX','IMF','DEL','JLR','JAI','JSA','IXJ','JGA','JDH','JRH','CDP','IXH','IXY','DHM','CNN','KNU','RDP','BLR','IXK','HJR','KQH','KLH','KTU','KUU','VNS','IXL','Leh','AJL','PAT','GAU','LUH','IXM','UDR','IXE','LTU','MZU','BKB','NDC','ISK','CCU','IXI','PGH','IXP','PNY','PBD','PNQ','BHO','RJA','HYD','RAJ','RTC','REW','RRK','SXV','AMD','SXR','SHL','SAG','IXS','SSE','IXW','ATQ','PUT','STV','TEZ','TRZ','TRV','BDQ','VGA','IXZ','ZER']

def getFlightsByPriceAndDuration(SRC, DST, yyyymmdd):
    ran = random.randint(1, 0xffffffff)
    ip = socket.inet_ntoa(struct.pack('>I', ran))
    headers['x-user-ip']: ip
    params['crId'] = ran
    params['it'] = SRC+'-'+DST+'-'+str(yyyymmdd)
    response = requests.get(url, params=params, headers=headers)
    jsondata = response.json()
    hashmap = {}
    if response.status_code != 200:
        return
    if 'journeyMap' in response.json() and 'cardList' in response.json() and len(list(jsondata['journeyMap'])) >0 and len(list(jsondata['cardList'][0]))>0:
        for key in list(jsondata['journeyMap']):
            hashmap[key] = {}
            layover_minute = 0
            if  jsondata['journeyMap'][key]['layover'] != "":
                layover_pre_split = jsondata['journeyMap'][key]['layover'].replace(" Technical stop over", '').split(" Layover")[0].rstrip()
                if 'h' in layover_pre_split and 'm' in layover_pre_split:
                    layover_split = layover_pre_split.split("h")
                    layover_minute = (60 * int(layover_split[0])) + int(layover_split[1].lstrip().replace("m", ''))
                elif 'h' in layover_pre_split: # only hour
                    layover_minute = (60 * int(layover_pre_split.replace("h",'')))
                else: # only minute
                    try:
                        layover_minute = int(layover_pre_split.rstrip().replace("m", ""))
                    except Exception as e:
                        layover_minute = "Multiple Layovers"
            hashmap[key]["layover"] = layover_minute
            hashmap[key]["duration"] = int(jsondata['journeyMap'][key]['duration']["h"])*60 + int(jsondata['journeyMap'][key]['duration']["m"])
        for data in jsondata['cardList'][0]:
            key = data['journeyKeys'][0]
            hashmap[key]["fare"] = int(data['fare'])
        return hashmap
    return

def filterFlightsByLayover(flight_map, minimum_layover_time_if_any_layover, direct_flight_only_flag):
    for key in list(flight_map):
        if flight_map[key]["layover"] == "Multiple Layovers" or (direct_flight_only_flag and flight_map[key]["layover"] > 0):
            del flight_map[key]
        elif flight_map[key]["layover"] != "Multiple Layovers" and flight_map[key]["layover"] < minimum_layover_time_if_any_layover and flight_map[key]["layover"] > 0:
            del flight_map[key]
    return flight_map

def sortFlightsByPrice(flight_map, num):
    for k in [key for key in flight_map if 'fare' not in flight_map[key]]:
        del flight_map[k]
    list =[]
    for s in sorted(flight_map, key=lambda x: flight_map[x]["fare"]):
        list.append([s, flight_map[s]["fare"], flight_map[s]["duration"], flight_map[s]["layover"]])
        if len(list) == num:
            return list
    return list #in case list is smaller than 10

def getTop10FlightsSortedByPriceAboveLayoverTime(SRC, DST, yyyymmdd, minimum_layover_time_if_any_layover, direct_flight_only_flag):
    flights = getFlightsByPriceAndDuration(SRC, DST, yyyymmdd)
    if flights == None:
        return
    filtered_flights = filterFlightsByLayover(flights, minimum_layover_time_if_any_layover, direct_flight_only_flag)
    sorted_flights = sortFlightsByPrice(filtered_flights, 10)
    if sorted_flights == None:
        print("No flight found")
        return
    return sorted_flights

def printo(list):
    if list:
        print ('''flight_key, price, duration_in_minutes, layover_in_minutes''', "\n")
        for item in list:
            print(item, "\n")
    else:
        print("Nothing found")


def findCheapest10FlightsAllOverIndia(yyyymmdd, minimum_layover_time_if_any_layover, direct_flight_only_flag):
    cheapest_flight_map = {}
    for src in all_india_airport_codes:
        for dst in all_india_airport_codes:
            flights = getFlightsByPriceAndDuration(src, dst, yyyymmdd)
            if flights != None:
                filtered_flights = filterFlightsByLayover(flights, minimum_layover_time_if_any_layover, direct_flight_only_flag)
                cheapest_flight_map.update(filtered_flights)
                print(src, dst, len(filtered_flights))
    for k in [key for key in cheapest_flight_map if 'fare' not in cheapest_flight_map[key]]:
        del cheapest_flight_map[k]
    list =[]
    for s in sorted(cheapest_flight_map, key=lambda x: cheapest_flight_map[x]["fare"]):
        list.append([s, cheapest_flight_map[s]["fare"], cheapest_flight_map[s]["duration"], cheapest_flight_map[s]["layover"]])
        if len(list) == 10:
            return list
    return list #in case list is smaller than 10


if __name__ == '__main__':
    printo(getTop10FlightsSortedByPriceAboveLayoverTime('BLR', 'DEL', 20230530, 120, False))
    #printo(findCheapest10FlightsAllOverIndia(20230530,100,True))
