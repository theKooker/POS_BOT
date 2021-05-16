#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sikuli import *
import json
import urllib
import urllib2
import sys 
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\logger_code.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\modifiable_data.sikuli")
import modifiable_data
from datetime import date
today=date.today()
import logging
logging.basicConfig(format=modifiable_data.extra_infos["log_format"],filename=modifiable_data.extra_infos["error_file"]+" "+str(today)+"-log.log",filemode="a",level=modifiable_data.extra_infos["log_level"])
counter_error=1
times=1
string_code=""
def get_request(): 
    global times,counter_error,logger1
    while (counter_error==1)and(times<=modifiable_data.extra_infos["times_http"]):
        times=times+1
        try:
            global string_code
            #fetching the code of authentification :) 
            login_url=modifiable_data.network_infos["login_url"]
            logging.debug(login_url)
            values = {'userName' : modifiable_data.network_infos["username"],
                      'password' : modifiable_data.network_infos["passwort"]}
            content_header = {'content-type':'application/x-www-form-urlencoded'} 
            login_data = urllib.urlencode(values)
            login_req = urllib2.Request(login_url, login_data)
            login_response = urllib2.urlopen(login_req)
            the_page_login =login_response.read()
            data_json =json.loads(the_page_login)
            #fetching the orders :)
            
            order_url=modifiable_data.network_infos["order_url"]+modifiable_data.network_infos["store_id"]
            string_code='Bearer '+data_json["data"]["auth_code"]
            order_req=urllib2.Request(order_url)
            order_req.add_header('Authorization',string_code)
            order_response=urllib2.urlopen(order_req)
            the_page_order=order_response.read()
            data_json_order=json.loads(the_page_order)
            length_order=len(data_json_order)
            return data_json_order
            counter_error=0
        except Exception as e:
            er=str(e)
            popError("HTTP ERROR\nWir veruschen erneut\nBitte nichts beruhre")
            counter_error=1
            logging.error(er)
    if times>modifiable_data.extra_infos["times_http"]:
        popError("es tut uns Leid\nWir haben ein Problem mit der Internetverbindung\nClicken Sie auf Ok\nGehen Sie auf die Starteseite")
counter_error=1
times=1
def put_request(order_id,status):
    global times,counter_error
    while (counter_error==1)and(times<=modifiable_data.extra_infos["times_http"]):
        times=times+1
        try:
            login_url=modifiable_data.network_infos["login_url"]
            logging.debug(login_url)
            values = {'userName' : modifiable_data.network_infos["username"],
                      'password' : modifiable_data.network_infos["passwort"]}
            content_header = {'content-type':'application/x-www-form-urlencoded'} 
            login_data = urllib.urlencode(values)
            login_req = urllib2.Request(login_url, login_data)
            login_response = urllib2.urlopen(login_req)
            the_page_login =login_response.read()
            data_json =json.loads(the_page_login)
            #fetching the orders :)
            
            order_url=modifiable_data.network_infos["order_url"]+modifiable_data.network_infos["store_id"]
            string_code='Bearer '+data_json["data"]["auth_code"]
            put_url=modifiable_data.network_infos["put_url"]+order_id
            content_header = {'content-type':'application/json',
                 'accept':'application/json,application/json',
                 'Authorization':string_code}    
            data={"pos_status":status}
            data = json.dumps(data)
            req=urllib2.Request(put_url,data,headers=content_header)
            req.get_method=lambda: 'PUT'
            response = urllib2.urlopen(req,timeout=5) 
            counter_error=0
        except Exception as e:
            er=str(e)
            logging.error(er)
            popError("PUT ERROR\nWir veruschen erneut\nBitte nichts beruhren")
            counter_error=1
            logging.error("CONNECTION ERROR WITH THE PUT REQUEST "+str(times-1))
    if times>modifiable_data.extra_infos["times_http"]:
        popError("es tut uns Leid\nWir haben ein Problem mit der Internetverbindung\nClicken Sie auf Ok\nGehen Sie auf die Starteseite")
if __name__=="get_request":
    
    get_request()
if __name__=="put_request":
   put_request(order_id,status)