#!/usr/bin/python
# encoding=utf8

import sys
import time
import os
import json
import requests
from optparse import OptionParser

#crc_url = 'http://www.whattomine.com/coins/226.json'
influx_url = 'http://54.95.191.117:8086/write?db=mydb'
#54.95.191.117
wtt_id_list = [1, 4, 5, 6, 8, 15, 27, 28, 29, 32, 34, 40, 45, 48, 49, 52, 53, 54, 56, 64, 66, 67, 70, 71, 72, 73, 101, 103, 104, 107, 112, 113, 114, 115, 119, 122, 124, 132, 137, 143, 144, 147, 148, 149, 150, 151, 152, 154, 157, 161, 162, 164, 165, 166, 167, 168, 169, 172, 173, 174, 175, 176, 177, 178, 180, 184, 185, 187, 188, 190, 192, 193, 194, 195, 196, 197, 199, 200, 201, 202, 203, 206, 207, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 238, 239, 240, 241, 242]

def refresh_coin(coin_no):

    name = ''
    algorithm = ''
    data = ''

    coin_url = 'http://www.whattomine.com/coins/'+str(coin_no)+'.json'
#    print('coin_url:',coin_url)
    try:
        resp = requests.get(coin_url)
        resp.raise_for_status()
    except requests.RequestException as e:
#        print(e)
        return None

    data = resp.json()    
#    print(resp.text.encode('utf-8'))
#    print(',')

    name = data['name']
    nethash = data['nethash']
    btc_revenue = data['btc_revenue']
    algorithm = data['algorithm']
    exchange_rate = data['exchange_rate']
    profit = data['profit']

    if name == '':
        print("data end!")
        return None

 #   print(name, algorithm, nethash, exchange_rate, btc_revenue, profit)

 #   put_url = 'curl -i -XPOST \''+influx_url+'\' --data-binary '+'\'mineprofit,name='+name+',algorithm='+algorithm+' nethash='+str(nethash)+',btc_revenue='+btc_revenue+'\''

#    print(put_url)

#    os.system(put_url)

    return data

def refresh_all_coins():
    # read wtt id from wtt_coin_id.json
    coin_file = open("./wtt_coin_id.json", "rb")  
    coin_json = json.load(coin_file)

    print('{\ncoins:[')
    for num in wtt_id_list:
        refresh_coin(num)
        time.sleep(1)

    print(']\n}\n')
    coin_file.close()
    return

def scan_coins():
    print('[')
    for num in range(300):
        coin_json = refresh_coin(num)
        if (coin_json):
            name = coin_json['name']
            tag = coin_json['tag']
            algorithm = coin_json['algorithm']
            print('{')
            print('    \"WttId\": %d,'%(num))
            print('    \"CoinName\": \"%s\",'%(name.encode('utf-8')))
            print('    \"CoinAb\": \"%s\",'%(tag))
            print('    \"AlgoName\": \"%s\"'%(algorithm))
            print('},')
        time.sleep(1)
    print(']')


    return

def import_to_spreadsheet():

    for num in wtt_id_list:
        coin_url = 'http://www.whattomine.com/coins/'+str(num)+'.json'
        importstr = '=importJson(\"'+coin_url+'\", \"\", \"noHeaders\")'
        print(importstr)

    return

if __name__ == '__main__':

    # avoid 'max retries' error
    s = requests.session()
    s.keep_alive = False

    parser = OptionParser()
    parser.add_option("-i", "--import_sheet", dest="import_sheet", action="store_true", default=False, help="generate string in google spreadsheet")
    parser.add_option("-a", "--all_coins", dest="all_coins", action="store_true", default=False, help="get info of all known wtm coins, which come from wtt_coin_id.json")
    parser.add_option("-s", "--scan_coins", dest="scan_coins", action="store_true", default=False, help="scan all coins at wtm, write out formatted as wtt_coin_id.json")
    (options, args) = parser.parse_args()

    if (not options.import_sheet) and (not options.all_coins) and (not options.scan_coins):
        parser.error("must have one option, use -h to help!")
        sys.exit(-1)

    if (options.import_sheet):
        import_to_spreadsheet()
    if (options.all_coins):
        refresh_all_coins()
    if (options.scan_coins):
        scan_coins()





    

