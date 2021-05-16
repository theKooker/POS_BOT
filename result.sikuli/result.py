#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sikuli import *
import modifiable_data
import sys,os,imp
from datetime import date
today=date.today()
import http_code
import logging,thread
logging.basicConfig(format=modifiable_data.extra_infos["log_format"],filename=modifiable_data.extra_infos["error_file"]+" "+str(today)+"-log.log",filemode='a',level=modifiable_data.extra_infos["log_level"])
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\modifiable_data.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\main.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\http_code.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\alert.sikuli")

try:
    nb=0
    cod_diff=0
    paid_diff=0
    def show_result(number,cod,paid,time_b):
        global nb,cod_diff,paid_diff
        nb=number
        cod_diff=cod
        paid_diff=paid     
        cod_s=str(cod_diff)
        cod_s=cod_s.replace(".",",")
        paid_s=str(paid_diff)
        paid_s=paid_s.replace(".",",")
        path=modifiable_data.extra_infos["diff_file"]
        f=open(path,"w")
        f.write(str(nb))
        f.write("\n")
        f.write(cod_s)
        f.write("\n")
        f.write(paid_s)
        f.close()
        popup("Wir haben "+str(number)+" Bestellungen durchgefuhrt.\nDie Differenz zur Online Bezahlungen betragt "+paid_s+" Euro.\nDie Differenz zur Bar Bezahlungen betragt "+cod_s+" Euro.\nBitte buchen Sie die Differenz.\nOK um weiterzumachen.")
        popup("Zeitersparnis: "+str(time_b)+" Min")
        popup("Bitte gehen Sie auf die Startseite um weiterzumachen")
        while not(exists("zeiterfassung.png")):
            wait(0.1)
        popup("Warten Sie...\nBitte clicke auf OK")
        import alert
        thread.start_new_thread(alert.loading_pop,())
        imp.reload(http_code)
        data=http_code.get_request()
        import main
        main.gui_display(data,len(data))
        

except Exception as e:
    er=str(e)
    logging.error(er)
    popError("Bitte starten Sie den POS_BOT neu ")
        