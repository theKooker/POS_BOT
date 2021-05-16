#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sikuli import *
import imp,sys,json
from javax.swing import JFrame,JLabel
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\http_code.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\modifiable_data.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\needed_functions_for_injecting.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\result.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\alert.sikuli")
import modifiable_data
import thread
from datetime import date,datetime
today=date.today()
import logging
logging.basicConfig(format=modifiable_data.extra_infos["log_format"],filename=modifiable_data.extra_infos["error_file"]+" "+str(today)+"-log.log",filemode="a",level=modifiable_data.extra_infos["log_level"])
from needed_functions_for_injecting import getindex,search_it,item_existed
from result import show_result
setBundlePath(modifiable_data.extra_infos["images_path"])
def injecting(data_json_order,number_orders,l,time_state):
    try:
        from timeit import default_timer as timer
##============================================================================
##=============================================================================            
        summe_COD=0
        summe_PAID=0
        path=modifiable_data.extra_infos["file_path"]
        l_k=[]
        n=0
        time_b=0
        number_orders_checkedout=0
        logging.info(str(number_orders))
        for i in range (0,number_orders):
            if l[i].isSelected():
                l_k.append(l[i])
                n=n+1
        for i in range(0,n):
            if l_k[i].isSelected():
                index=getindex(l,l_k[i].getText(),data_json_order)
                l_name_order=[]
                m=0
                import alert
                thread.start_new_thread(alert.alert_pop,())
            ##====================================================
                order_description=json.loads(data_json_order[index]['source_json'])
                order_id=data_json_order[index]['order_id']
                received_time=data_json_order[index]['received_time']
                date=received_time[:received_time.index(" ")]
                date=datetime.strptime(date,"%Y-%m-%d").strftime("%d-%m-%Y")
                time=received_time[received_time.index(" ")+1:]
                if time_state=="YES":
                    stream = os.popen('date '+date)
                    output = stream.read()
                    stream = os.popen('time '+time)
                    output = stream.read()
                from timeit import default_timer as timer
                begin=timer()                
                logging.info("ORDER IR"+order_id)
                total_amount=data_json_order[index]['total_amount']
                short_code=data_json_order[index]['short_code']
                payment_type=data_json_order[index]['payment_type']
            ##===================================================
                for j in range(0,len(order_description)):
                    nam=order_description[j]["name"].rstrip()
                    sidedishes=order_description[j]["sideDishes"]
            ##====================================================  
                    import re
                    sparmenu_check=re.search("Sparmen",nam)
                    familienmenu_check=re.search("Familienmen",nam)
                    chipsmenu_check=re.search("F.*nf.T.*ten",nam)
            ##=================================================== 
                    #WE CAN ADD HERE STHG IF YOU ARE SURE OF IT :)       
                    #WE CAN ADD HERE STHG IF YOU ARE SURE OF IT :) 
            ##===================================================
                    if (sparmenu_check) or(familienmenu_check)or (chipsmenu_check)or(nam=="Cookie")or(nam=="Laugen-Snack")or(nam=="Kids Pak"):
                        nb=int(order_description[j]["count"])
                        check_var=True
                    else:
                        check_var=False
                        
                    if check_var==True:#the case when we have a Menu
                        for cpt in range(0,nb):
                            if familienmenu_check:
                                m=m+1
                                l_name_order.append("30cm|1")
                            else:                      
                                if (nam.find("30")!=-1)or(nam.find("15")!=-1):
                                    m=m+1
                                    l_name_order.append(nam[nam.index("-")+1:].rstrip()+"|1")  
                            #PROCESS OF THE SIDEDISHES                        
                            for k in range(0,len(sidedishes)):
                                coun_number=sidedishes[k]["count"]
                                if (nam=="Laugen-Snack"):
                                    m=m+1
                                    l_name_order.append("Snack"+sidedishes[k]["name"].encode('utf-8').rstrip()+"|"+str(coun_number))
                                if (nam=="Kids Pak"):
                                    m=m+1
                                    l_name_order.append("Kids' Pak"+sidedishes[k]["name"].encode('utf-8').rstrip()+"|"+str(coun_number))
                                if (str(sidedishes[k]["price"])!="0"):
                                    m=m+1
                                    l_name_order.append(sidedishes[k]["name"].encode('utf-8').rstrip()+"|"+str(coun_number))                       
                                if (check_var==True)and(str(sidedishes[k]["price"])=="0")and(item_existed(sidedishes[k]["name"],path)):
                                    if (familienmenu_check) and (sidedishes[k]["name"].find("Sub")!=-1)and(l_name_order[m-1]!="30cm|1"):
                                        m=m+1
                                        l_name_order.append("30cm|1")
                                        m=m+1
                                        l_name_order.append(sidedishes[k]["name"].encode('utf-8').rstrip()+"|1")
                                    else:
                                        m=m+1
                                        l_name_order.append(sidedishes[k]["name"].encode('utf-8').rstrip()+"|"+str(coun_number))                                        
                    ##========================================================================================================
                    else:##the case when we dont have a Menu
                        coun_number=order_description[j]["count"]                   
                        if(nam.find("[")==-1):
                            for cpt in range(0,int(coun_number)):                            
                                m=m+1
                                l_name_order.append(nam+"|1")
                        else:
                            for cpt in range(0,int(coun_number)):                            
                                m=m+1
                                l_name_order.append(nam[nam.index("[")+1:nam.index("]")]+"|1")
                                m=m+1
                                l_name_order.append(nam[:nam.index("[")]+"|1")
                    #PROCESS OF THE SIDEDISHES
                        if len(sidedishes)!=0:
                            for k in range(0,len(sidedishes)):
                                coun_number=sidedishes[k]["count"]
                                if (str(sidedishes[k]["price"])!="0"):
                                    m=m+1
                                    l_name_order.append(sidedishes[k]["name"].encode('utf-8').rstrip()+"|"+str(coun_number))                                              
                #reformating the items of the list 
                feature_list=[]
                for j in range(0,m):
                    feature_list.append(l_name_order[j])
                    ch=""
                    term=l_name_order[j]
                    for k in range(0,len(term)):
                        if term[k]!=" ":
                            ch=ch+term[k].lower().rstrip()			      
                    l_name_order[j]=ch
                #PRINTING THE LIST
                for item in l_name_order:
                    logging.debug(item)
                #PROCESSInG THE CLICKS
                J=-1
                for aktuel_item in l_name_order:
                    J=J+1
                    try:
                        logging.debug("YOUR ITEM IS "+aktuel_item)#.encode("utf-8")
                        if item_existed(aktuel_item,path):
                            search_it(path,aktuel_item)
                        else:
                            thread.exit
                            import alert
                            thread.start_new_thread(alert.help_pop,())
                            popError("Wir haben wahrscheinlich die Bilder fuer die Produkt "+feature_list[J][:feature_list[J].index("|")]+" nicht gefunden.\nBitte wahlen Sie die Bilder aus.\nAuf Ok")
                            tr=True
                            path_string=""
                            while(tr==True):
                                region=selectRegion("wahlen Sie Bilder aus")
                                
                                path_string=path_string+str(region.getX())+","+str(region.getY())+","+str(region.getW())+","+str(region.getH())+","+"|"
                                click(region)
                                answer=popAsk("sind Sie fertig ?")
                                if not answer:
                                        tr=True
                                else:
                                        tr=False
                            file=open(path,"a")
                            file.write("\n")
                            file.write(aktuel_item[:aktuel_item.index("|")].replace(",",".")+";"+path_string)
                            file.close()
                            thread.exit
                    except Exception as e:
                        er=str(e)
                        logging.error(er)
                        popError("wir haben ein Problem gefunden\nBitte gehen Sie auf die Starteseite um erneut zu versuchen \nPS:Wenn es noch mal stoppt ,dann buchen Sie Bitte die Diff und melden Sie Sich bei UNS :)")
                        import http_code
                        imp.reload(http_code)
                        http_code.put_request(order_id,"error")
                        from timeit import default_timer as timer
                        end=timer()
                        time_b=round((time_b)/60,2)
                        show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
                        return False
        ##=================================================================================================
                ##This part is for processing the checkout and showing the result in a popup
                
                try:
                    try:
                        find("gesamt.png")
                        click("gesamt.png")
                    except :
                        logging.error("gesamt.png not found !")
                        popError("Bitte clicken Sie auf gesamt\n melden Sie sich bei uns um das neue Bild zu machen")
                    try:
                        wait("ja.png",10)
                        click("ja.png")
                    except:
                        logging.error("JA.png not found")
                        popError("Bitte clicken Sie of JA\nmelden Sie sich bei uns um das neue Bild zu machen")
                    try:
                        wait("ok.png",10)
                        click("ok.png")
                    except:
                        logging.error("ok.png not found!")
                        popError("Bitte clicken Sie of OK\nmelden Sie sich bei uns um das neue Bild zu machen")
                except Exception as e:
                    er=str(e)
                    logging.error(er)
                    logging.error("IMAGE NOT FOUND")
                    popError("Wir haben ein Problem gefunden\nBitte gehen Sie auf die Startseite")
                    import http_code
                    imp.reload(http_code)
                    http_code.put_request(order_id,"error")
                    from timeit import default_timer as timer
                    end=timer()
                    time_b=round((time_b)/60,2)
                    show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
                    return False       
                if (data_json_order[index]["payment_type"]=="Paid"):##the case when we have a PAID order
                    try:
                        try:
                            wait("hauskonto.png",10)
                            click("hauskonto.png")
                        except:
                            logging.error("hauskonto.png not found")
                            popError("Bitte clicken Sie auf HausKonto\nmelden Sie sich bei uns um das neue Bild zu machen")
                        Settings.WaitScanRate
                        while not (exists("lieferando.png")):
                            import time
                            time.sleep(0.5)
                        click("lieferando.png")
                    except Exception as e:
                        er=str(e)
                        logging.error(er)
                        popError("Wir haben ein Problem gefunden\nBitte gehen Sie auf die Startseite")
                        import http_code
                        imp.reload(http_code)
                        http_code.put_request(order_id,"error")
                        from timeit import default_timer as timer
                        end=timer()
                        time_b=round((time_b)/60,2)
                        show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
                        return False       
                    Settings.WaitScanRate
                    if(exists("geldabwurf.png")):
                        click("nein.png")                
                    betrag_string=""
                    number_clicks=0
                    while (number_clicks<modifiable_data.extra_infos["times_click"])and(betrag_string==""):  
                        try:
                            if(exists("up.png"))and(not(exists("del_lieferando.png"))):  
                                click("down.png")             
                            Settings.WaitScanRate
                            wait("del_lieferando.png")                    
                            click("del_lieferando.png")
                            type("c",KEY_CTRL)
                            betrag_string=Env.getClipboard()
                            number_clicks=number_clicks+1
                        except Exception as e:
                            er=str(e)
                            logging.error(er)
                            popError("Wir haben ein Problem gefunden\nBitte gehen Sie auf die Startseite")
                            import http_code
                            imp.reload(http_code)
                            http_code.put_request(order_id,"error")
                            from timeit import default_timer as timer
                            end=timer()
                            time_b=round((time_b)/60,2)
                            show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
                            return False                            
                    if betrag_string=="":
                       logging.error("betrag_string ist leer")
                       popError("Wir haben ein Problem gefunden\nBitte gehen Sie auf die Startseite")                       
                       import http_code
                       imp.reload(http_code)
                       http_code.put_request(order_id,"error")
                       from timeit import default_timer as timer
                       end=timer()
                       time_b=round((time_b)/60,2)
                       show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
                       return False
                    import re
                    string_b=re.search(r"\d+.\d\d", betrag_string).group(0)
                    string_b=string_b.replace(".","")
                    string_b=string_b.replace(",",".")
                    betrag_PAID=float(string_b)
                    betrag=betrag_PAID
                    summe_PAID=data_json_order[index]["total_amount"]-betrag_PAID+summe_PAID
                else:#the case when we have a COD order
                    try:
                        try:
                            wait("hauskonto.png",10)
                            click("hauskonto.png")
                        except:
                            logging.error("hauskonto.png not found")
                            popError("Bitte clicken Sie auf HausKonto\nmelden Sie sich bei uns um das neue Bild zu machen")
                        Settings.WaitScanRate  
                        try:
                            wait("dellieferbar.png",10)
                            click("dellieferbar.png")
                        except Exception as e:
                            logging.error("dellieferbar.png not FOUND")
                            popError("Bitte Clicken Sie auf DEL LIEFER BAR")
                        Settings.WaitScanRate
                    except Exception as e:
                        er=str(e)
                        logging.error(er)
                        popError("Wir haben ein Problem gefunden\nBitte gehen Sie auf die Startseite")
                        import http_code
                        imp.reload(http_code)
                        http_code.put_request(order_id,"error")
                        from timeit import default_timer as timer
                        end=timer()
                        time_b=round((time_b)/60,2)
                        show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
                        return False
                    if(exists("geldabwurf.png")):
                        click("nein.png")
                    Settings.WaitScanRate                       
                    betrag_string=""
                    number_clicks=0
                    while (number_clicks<modifiable_data.extra_infos["times_click"])and(betrag_string==""): 
                        try:
                            if(exists("up.png"))and(not(exists("delbar2.png")) or not(exists("delbar.png"))):  
                                click("down.png")             
                            Settings.WaitScanRate
                            #wait("delbar.png",5)
                            if exists("delbar.png"):
                                click("delbar.png")
                            else:
                                click("delbar2.png")
                            type("c",KEY_CTRL)
                            betrag_string=Env.getClipboard()
                            number_clicks=number_clicks+1
                        except Exception as e:
                            er=str(e)
                            logging.error(er)
                            popError("Wir haben wahrscheinlich ein Problem gefunden\nBitte gehen auf die Startseite")
                            import http_code
                            imp.reload(http_code)
                            http_code.put_request(order_id,"error")
                            from timeit import default_timer as timer
                            end=timer()
                            time_b=round((time_b)/60,2)
                            show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
                            return False
                            
                    if betrag_string=="":
                       logging.error("betrag_string ist leer")
                       popError("Wir haben wahrscheinlich ein Problem gefunden\nBitte gehen auf die Startseite")
                       import http_code
                       imp.reload(http_code)
                       http_code.put_request(order_id,"error")
                       from timeit import default_timer as timer
                       end=timer()
                       time_b=round((time_b)/60,2)
                       show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
                       return False
                    import re
                    string_b=re.search(r"\d+.\d\d", betrag_string).group(0)
                    string_b=string_b.replace(".","")
                    string_b=string_b.replace(",",".")
                    betrag_COD=float(string_b)
                    betrag=betrag_COD
                    summe_COD=data_json_order[index]["total_amount"]-betrag_COD+summe_COD            
                import http_code  
                imp.reload(http_code)
                http_code.put_request(order_id,"transferred_auto")
                number_orders_checkedout=number_orders_checkedout+1
                logging.info("#"+str(short_code)+";DATENBANK "+str(total_amount)+";KASSE "+str(betrag)+"; "+payment_type)
                from timeit import default_timer as timer
                end=timer()
                time_b=time_b+(end-begin)
                print("TIME_B = "+str(time_b))
        logging.info("Total Diff: "+str(summe_COD)+";COD")
        logging.info("Total Diff: "+str(summe_PAID)+";PAID")
        logging.info("#######ORDER COMPLETED##########")
        time_b=round((time_b)/60,2)
        print(time_b)
        show_result(number_orders_checkedout,summe_COD,summe_PAID,time_b)
    except Exception as e:
        er=str(e)
        logging.error(er)
        return False