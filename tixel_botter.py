from urllib.request import urlopen
import urllib
import time
from bs4 import BeautifulSoup
from bs4.element import Comment
from plyer import notification
import datetime
import configparser
from pathlib import Path

#LOGGING

import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('tixelbot.log', 'a'))
print = logger.info

print("Logging setup successful")

#CONFIG WRITING
config = configparser.ConfigParser(allow_no_value=True)
config_file = Path("./config.ini")
if not config_file.is_file():
    config.add_section('Settings')
    config.set('Settings', "Refresh Time", '10')
    config.set('Settings', "#generally, don't set this below 10 to avoid overloading tixel servers")                   
    config.set('Settings', 'Tixel URL', 'https://tixel.com/au/beyond-the-valley-tickets')
    config.set('Settings', 'Search Value', 'Car Pass')
    with open('config.ini', 'w+') as configfile:
        config.write(configfile)

config_read = configparser.ConfigParser()
config_read.read('config.ini')
try:
    x = int(config_read['Settings']['Refresh Time'])
except:
    print("Refresh time setup failed! Check numeric value is valid")
    input()
try:
    url = config_read['Settings']['Tixel URL']
except:
    print("URL setup failed! Check url is valid")
    input()
try:
    cp = config_read['Settings']['Search Value']
except:
    print("Search value setup failed! Check valid")
    input()

##########

#url = "https://tixel.com/au/beyond-the-valley-tickets"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
user_agent_2 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'

#x = 10
print("Working with refresh time: "+str(x)+", url: "+str(url)+", search value: "+str(cp))


headers={'User-Agent':user_agent,} 
headers_2={'User-Agent':user_agent_2,} 
request=urllib.request.Request(url,None,headers) #The assembled request

response = urlopen(request)
print(response)
html = response.read()
bsObj = BeautifulSoup(html, 'html.parser')
bsObjNew = bsObj

def visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_cps(bs, cp):
    texts = bs.findAll(text=True)
    visible_texts = filter(visible, texts)
    cp_list = []
    #cp = 'Car Pass'
    for t in visible_texts:
        if cp in t:
            cp_list.append(t)
    return cp_list

cp_list = get_cps(bsObj, cp)
cp_list_new = cp_list
cur_head = 1
recon = 0
ref = 0
swap = 0
try:
    while True:
        while cp_list_new == cp_list:
            if swap == 3:
                swap = 0
                headers, headers_2 = headers_2, headers
                print("Reconnecting under new header...")
                request = urllib.request.Request(url,None,headers)
                #response = urlopen(request)
            #print(str(cp_list)+"\n"+str(cp_list_new))
            print("---------"+str(datetime.datetime.now())+"---------\nWaiting "+str(x)+" seconds")
            time.sleep(x)
            try:
                #print("\n> ", end="", flush=True)
                bsObjNew = BeautifulSoup(urlopen(request).read(), 'html.parser')
                #print(" HTML doc parsed, ", end="", flush=True)
                cp_list_new = get_cps(bsObjNew, cp)
                #print("list of elements generated\n")
                print("> HTML doc parsed, list of elements generated")
                if cp_list_new != cp_list:
                    print("New Car Pass Available! "*20)

                    notification.notify(
                    title='NEW CAR PASS AVAILABLE',
                    message='Car pass may be present on tixel.com',
                    #app_name='Here is the application name'
                    #app_icon='tixel.png'
                    )

                    print(str(cp_list_new))
                    cp_list = cp_list_new
                    bsObj = bsObjNew
                else:
                    print("No change to site detected")
            except IOError:
                print("Can't open site. Connection may have been closed")
                print("Reconnecting...")
                try:
                    request = urllib.request.Request(url,None,headers)
                    response = urlopen(request)
                    print(response)
                    recon+=1
                    print("Reconnect count: "+str(recon))
                except:
                    print("Reconnection caused an error. Waiting before retrying with new agent...")
                    time.sleep(5)
                    headers, headers_2 = headers_2, headers
                    print("Reconnecting...")
                    request = urllib.request.Request(url,None,headers)
                    response = urlopen(request)
                    print(response)
                    recon+=1
                    print("Reconnect count: "+str(recon))
            ref+=1
            print("Refresh Count: " + str(ref))
            swap+=1
        print("Something happened! Retrying connection...")
        request=urllib.request.Request(url,None,headers) #The assembled request
        response = urlopen(request)
        print(response)
        html = response.read()
        bsObj = BeautifulSoup(html, 'html.parser')
        bsObjNew = bsObj
        cp_list = get_cps(bsObj, cp)
        cp_list_new = cp_list
except:
    input("FATAL ERROR OCCURRED. Press any key to continue...")