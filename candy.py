#! /usr/bin/env python
import requests
import json
import time

url = 'http://192.168.1.24/http-read.json?encrypted=1'
key = 'fhaihbiklhjdlmga'
request_timeout = 10
retries = 3
retry_delay = 2
candyOff = {'WiFiStatus':'1', 'Err':None, 'MachMd':None, 'Pr':None, 'PrPh':None, 'Temp':None, 'SpinSp':None, 'RemTime':'0', 'DryT':'0', 'DelVal':0, 'TotalTime':'0'}
tries = 0
candy = {}

#extract data
def fetchHex(xurl, xrequest_timeout):
    try:
        candyhex = requests.get(xurl, timeout=xrequest_timeout).text
        return candyhex
    except:
        return None

# convert data to readable text
def convText():
    hexText = fetchHex(url, request_timeout)
    if hexText == None:
        return None
    bytes_object = bytes.fromhex(hexText)
    coded = bytes_object.decode("ASCII")
    return coded

#decode data
def decode(xkey):
    xored = str()
    codedText = convText()
    if codedText == None:
        return None
    repeated_key = (xkey)*((len(codedText) // len(xkey)) + 1)
    for x in range(len(codedText)):
        xored += chr(ord(codedText[x]) ^ ord(repeated_key[x]))
    return xored

# strip and print data
while tries < retries:
    decoded = decode(key)
    if decoded != None:
        decodedDict = json.loads(decoded)
        candyData = decodedDict.get('statusLavatrice')
        for k, v in candyData.items():
            if k[0:3] != "Opt" and k[0:3] != "Rec" and k[0:3] != "Ste" and k[0:3] != "SLe" and k[0:3] != "Che":
                if k == 'DelVal' and candyData[k] == '255':
                    candy['DelVal'] = '0'
                else:
                    candy[k] = candyData[k]
        TotalTime = int(candy['DelVal']) * 60 + int(candy['RemTime'])
        candy['TotalTime'] = str(TotalTime)
        candyJson = json.dumps(candy, indent = 4)
        break
    tries += 1
    time.sleep(retry_delay)
if tries == retries:
    candyJson = json.dumps(candyOff, indent = 4)
print(candyJson)

