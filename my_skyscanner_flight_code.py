import requests

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
    'x-user-ip': '125.16.129.65',
    'x-user-rc': 'NEWDELHI',
}

params = {
    'pfm': 'PWA',
    'lob': 'B2C',
    'crId': '12425bn1382-a503-5cb9-9075-e9f5e03d7f44',
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
    'it': ''
}

url = 'https://flights-cb.makemytrip.com/api/search'

def getFlightsByPriceAndDuration(SRC, DST, yyyymmdd):
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

def filterFlightsByLayover(flight_map, minimum_layover_minutes_if_any_layover, direct_flight_only_flag):
    for key in list(flight_map):
        if flight_map[key]["layover"] == "Multiple Layovers" or (direct_flight_only_flag and flight_map[key]["layover"] > 0):
            del flight_map[key]
        elif flight_map[key]["layover"] != "Multiple Layovers" and flight_map[key]["layover"] < minimum_layover_minutes_if_any_layover and flight_map[key]["layover"] > 0:
            del flight_map[key]
    return flight_map

def sortFlightsByPrice(flight_map):
    for k in [key for key in flight_map if 'fare' not in flight_map[key]]:
        del flight_map[k]
    list =[["flight_key", "price", "duration_in_minutes", "layover_in_minutes"]]
    for s in sorted(flight_map, key=lambda x: flight_map[x]["fare"]):
        list.append([s, flight_map[s]["fare"], flight_map[s]["duration"], flight_map[s]["layover"]])
        if len(list) ==11:
            return list

def printTop10FlightsSortedByPriceAboveLayoverTime(SRC, DST, yyyymmdd, minimum_layover_time_if_any_layover, direct_flight_only_flag):
    flights = getFlightsByPriceAndDuration(SRC, DST, yyyymmdd)
    if flights == None:
        print ("Error: REPEAT_HIT_WITH_SAME_CRID. Try changing crId..")
        return
    filtered_flights = filterFlightsByLayover(flights, minimum_layover_time_if_any_layover, direct_flight_only_flag)
    sorted_flights = sortFlightsByPrice(filtered_flights)
    if sorted_flights == None:
        print("No flight found")
        return
    for flight in sorted_flights:
        print(flight, "\n")

if __name__ == '__main__':
    printTop10FlightsSortedByPriceAboveLayoverTime('DEL', 'HYD', 20230528, 120, False)
