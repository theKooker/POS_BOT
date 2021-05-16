#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sikuli import *
import re
import sys
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\modifiable_data.sikuli")
import modifiable_data
from datetime import date
today=date.today()
import logging
logging.basicConfig(format=modifiable_data.extra_infos["log_format"],filename=modifiable_data.extra_infos["error_file"]+" "+str(today)+"-log.log",filemode="a",level=modifiable_data.extra_infos["log_level"])
#sys.stdout=open(modifiable_data.extra_infos["activity_file"]+" "+str(today)+"-log.log","a")
#sys.stderr=open(modifiable_data.extra_infos["error_file"]+" "+str(today)+"-log.log","a")
setBundlePath(modifiable_data.extra_infos["images_path"])
try:
    def getindex(l,ch,data_json_order):#this function is to get the index of the actual item in the list in order to get into the data like them price
        i=0
        ch2="#"+str(data_json_order[0]["short_code"])+"-"+str(data_json_order[0]["received_time"])+"-"+str(data_json_order[0]["total_amount"])+"Euro"
        while(ch2 !=ch):
            i=i+1
            ch2="#"+str(data_json_order[i]["short_code"])+"-"+str(data_json_order[i]["received_time"])+"-"+str(data_json_order[i]["total_amount"])+"Euro"
        return i 
except Exception as e:
    er=str(e)
    logging.error(er)
#=================================
#####DONT MODIFY PLEASE THANK YOU :)#######
import re
try:
    def search_it(path,aktuel_item):
        count=0
        #this function is to proceed the clicks on the screen
        try:
            logging.info("ENTERING THE FUNCTION OF THE CLicK")
            file=open(path)
            ch=file.readline()
            item=ch[:ch.index(";")].strip()
            check_item=re.search(item,aktuel_item)
            if check_item:#we check if the item is really our actual item
                Bool=True
            else:
                Bool=False
            while(Bool==False):#in this while loop you can see that we are going in the text file line after line until we found the right item 
                ch=file.readline()
                item=ch[:ch.index(";")].rstrip()
                check_item=re.search(item,aktuel_item)
                if check_item:#we check if the item is really our actual item
                    Bool=True
                else:
                    Bool=False
            count=int(aktuel_item[aktuel_item.index("|")+1:])
            logging.info("count = "+str(count))
            file.close()
            ch=ch[ch.index(";")+1:]#ch is the string which contains the item and his adresses of images
            if ch.find(".png")!=-1:
                nb_images=ch.count(";")
            else:
                nb_images=ch.count("|")
                print(nb_images)
        except Exception as e:
            er=str(e)
            logging.error(er)
            #popError("Wir haben wahrscheinlich die Bilder fuer die Produkt "+aktuel_item+" nicht gefunden.\nBitte wahlen Sie die Bilder aus.\nAuf Ok")

        for i in range(0,int(count)):  #here we are in for loop to get into the number of times the product will be chosen
            for c in range(0,nb_images):#we are now in the for loop to get into all the adresses of images 
                try:
                    if ch.find(".png")==-1:
                        adresse=ch[:ch.index("|")].rstrip()
                        x=int(adresse[:adresse.index(",")])
                        adresse=adresse[adresse.index(",")+1:]
                        y=int(adresse[:adresse.index(",")])
                        adresse=adresse[adresse.index(",")+1:]
                        w=int(adresse[:adresse.index(",")])
                        adresse=adresse[adresse.index(",")+1:]
                        h=int(adresse[:adresse.index(",")])
                        logging.debug("region = "+adresse)
                        reg=Region(x,y,w,h)
                        click(reg)
                        ch=ch[:ch.index("|")+1:].rstrip()
                    else:
                        adresse=ch[:ch.index(";")].rstrip()
                        logging.info(adresse+" is the adresse")
                        while not(exists(adresse.rstrip())):
                            popError("Wir suchen nach "+item)
                            logging.error(adresse.rstrip()+" NOT FOUND")
                        find(adresse.rstrip())
                        logging.debug("FOUND "+adresse.rstrip())
                        click(adresse.rstrip())  
                        logging.debug("CLICKED ON "+adresse.rstrip())
                        ch=ch[ch.index(";")+1:].rstrip()
                        
                except Exception as e:
                    er=str(e)
                    logging.error(er)
                    popError("Wir haben wahrscheinlich die Bilder fuer die Produkt "+aktuel_item+" nicht gefunden.\nBitte wahlen Sie die Bilder aus.\nAuf Ok")
except Exception as e:
    er=str(e)
    logging.error(er)
    
#=================================
#####DONT MODIFY PLEASE THANK YOU :)#######
try:
    def item_existed(item,path):
        string_item=""
        for c in range(0,len(item)):
            if (item[c]!=" "):
                string_item=string_item+item[c].lower()
        length_file=0 
        f=open(path)
        line=f.readline()
        while line:
            line=f.readline()
            length_file=length_file+1
        f.close() 
        try:
            f=open(path)
            ch=f.readline()
            file_item=ch[:ch.index(";")].rstrip()
            check_var=re.search(file_item,string_item)
            if check_var:
                bool_var=True
            else:
                bool_var=False    
        
            i=0
            while (bool_var==False)and(i<length_file-1):
                ch=f.readline()
                i=i+1
                file_item=ch[:ch.index(";")].rstrip()
                check_var=re.search(file_item,string_item)
                if check_var:
                    bool_var=True
                else:
                    bool_var=False    
            f.close()
        except Exception as e :
            er=str(e)
            logging.error(er)
            return True
        if bool_var==True:
            return True
        else:
            return False
except Exception as e:
    er=str(e)
    logging.error(er)
    popError("ERROR1")