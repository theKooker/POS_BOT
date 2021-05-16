#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sikuli import *
from javax.swing import JFrame,JProgressBar
import time
import sys
import imp
import os
import thread
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\http_code.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\main.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\modifiable_data.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\alert.sikuli")
import modifiable_data
from main import gui_display
from datetime import date
import http_code
today=date.today()
import logging
print("WELCOME TO THE POS_BOT OF EVERESTO")
logging.basicConfig(format=modifiable_data.extra_infos["log_format"],filename=modifiable_data.extra_infos["error_file"]+" "+str(today)+"-log.log",filemode="a",level=modifiable_data.extra_infos["log_level"])
#GET THE DATA
try:
    frame=JFrame("LOADING")
    frame.setSize(300,100)
    frame.setLocation(300,300)
    BAR=JProgressBar(0,100)
    BAR.setValue(0)
    BAR.setStringPainted(True)
    frame.add(BAR)
    frame.setVisible(True)
    for i in range(0,101):
        time.sleep(0.005)
        BAR.setValue(i)    
    frame.dispose()
    import alert
    thread.start_new_thread(alert.loading_pop,())
    data_json_order=http_code.get_request()
    length_order=len(data_json_order)
    import main
    main.gui_display(data_json_order,length_order)
except Exception as e:
    er=str(e)
    logging.error(er)
    popError("Starten Sie erneut den POS_BOT\nWenn dieses POPError noch mal gezeigt ist,dann melden Sie sich bei uns")
while True:
    import time
    time.sleep(0.01)
