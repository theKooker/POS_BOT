#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sikuli import *
import sys,imp
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\needed_functions_for_injecting.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\inject_code.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\modifiable_data.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\the_main.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\result.sikuli")
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\alert.sikuli")
import modifiable_data
from needed_functions_for_injecting import getindex
setBundlePath(modifiable_data.extra_infos["images_path"])
from datetime import date
today=date.today()
import logging
logging.basicConfig(format=modifiable_data.extra_infos["log_format"],filename=modifiable_data.extra_infos["error_file"]+" "+str(today)+"-log.log",filemode="a",level=modifiable_data.extra_infos["log_level"])
from javax.swing import JFrame,JCheckBox,JButton,JLabel,JTextField,ImageIcon,JPasswordField
from java.awt import Color,Font
print("THE POS_BOT IS NEARLY READY!\nPLEASE WAIT")
import thread
number_orders=0
l=[]
frame=JFrame()
page=1
begin_counter=0
Benutzer_field=JTextField(1)
Passwort_field=JTextField(1)
number_orders=0
data={}
def gui_display(data_json_order,length_order):
    try:
###################
        global data
        data=data_json_order
        global number_orders
        global l
        global frame,page
        global begin_counter
        page=1
        global Benutzer_field,Passwort_field
        popup("Wir empfehlen Ihnen, den Drucker auszuschalten")
        popup("Ziehe den orangen Dashboard-Regler in die linke obere Ecke")
        import alert
        #CREATING THE FRAME OF THE GUI 
        img2=ImageIcon(modifiable_data.extra_infos["everesto_icon"])
        frame=JFrame(modifiable_data.extra_infos["frame_name"])
        frame.setLocation(150,10)
        frame.setSize(650,710)
        frame.setBackground(Color.blue)
        frame.setLayout(None) 
        frame.getContentPane().setBackground(Color.yellow)
        frame.setIconImage(img2.getImage())
        def thread_starting(event):
            thread.start_new_thread(btn_pressed,(event,))
        try:
            def btn_pressed(event):
                global number_orders
                global l
                global frame
                global Benutzer_field,Passwort_field
                pos = App(modifiable_data.extra_infos["app_name"])
                pos.open()
                pos.focus()
                counter_list=0
                for i in range(0,number_orders):
                    if l[i].isSelected():
                        counter_list=counter_list+1
                if (Benutzer_field.getText()=="")or (Passwort_field.getText()==""):
                    popError("die Daten sind ungultig")
                elif counter_list==0:
                    popError("Sie haben nichts ausgewahlt")
                else:
                    try:
                        frame.setExtendedState(JFrame.ICONIFIED)
                        if not(exists("grosskassieren.png")):
                            popError("Bitte SubwayPOS offnen")
                        while not(exists("grosskassieren.png")):
                            wait(0.1)
                        wait("grosskassieren.png",5)
                        click("grosskassieren.png")
                        click("benutzer_field.png")
                        type(Passwort_field.getText())
                        click("passwort_field.png")
                        type(Benutzer_field.getText())
                        click("o.k.png")    
                        if (exists("datenungultig.png")):
                            click("okgrun.png")
                            click("abbrechen.png")
                            frame.setExtendedState(JFrame.NORMAL)
                            popError("die Daten sind ungultig \nBitte,prufen Sie Ihrer Daten!!")                            
                            return False
                        while not(exists("productsscreen.png")):
                            time.sleep(0.02)
                            if exists("abgeschlossen.png"):
                                click("kleinkassieren.png")
                        if check_time.isSelected():
                            time_state="YES"
                        else:
                            time_state="NO"
                        frame.dispose()
                        import inject_code
                        imp.reload(inject_code)
                        inject_code.injecting(data_json_order,number_orders,l,time_state)
                    except Exception as e:
                        er=str(e)
                        popError("FEHLER")
                        logging.error(er)
        except Exception as e:
            er=str(e)
            logging.error(er)
        btn=JButton(modifiable_data.extra_infos["ubertragen"],actionPerformed = thread_starting)
        btn.setBounds(400,400,200,30)
        def manual(event):
            global data
            for i in range(0,number_orders):
                if l_manuel[i].isSelected():
                    index=getindex(l,l[i].getText(),data)
                    order_id=data_json_order[index]['order_id']
                    import http_code
                    imp.reload(http_code)
                    http_code.put_request(order_id,"transferred_manual")
            frame.dispose()
            import alert
            thread.start_new_thread(alert.loading_pop,())
            import http_code
            imp.reload(http_code)
            data=http_code.get_request()
            length_order=len(data)
            import main
            main.gui_display(data,length_order)            
        btn_manual=JButton(modifiable_data.extra_infos["manuel_buchung"],actionPerformed = manual)
        btn_manual.setBounds(400,450,200,30)
        img=ImageIcon(modifiable_data.extra_infos["kasse_icon"])
        back=JLabel(img)
        back.setBounds(316,363,100,100)
        frame.add(back) 
 
        #display of the version
        version_text=JLabel(modifiable_data.extra_infos["version"])
        version_text.setBounds(400,600,200,50)
        from result import nb,cod_diff,paid_diff
        #the button to refresh the orders :)
        def refresh_func(event):
            frame.dispose()
            #import the_main
            import alert
            thread.start_new_thread(alert.loading_pop,())
            import http_code
            imp.reload(http_code)
            data_json_order=http_code.get_request()
            length_order=len(data_json_order)
            import main
            main.gui_display(data_json_order,length_order)
        refresh_btn=JButton(modifiable_data.extra_infos["aktualisieren"],actionPerformed = refresh_func)#,actionPerformed =main)
        refresh_btn.setBounds(400,355,200,30)
        img=ImageIcon(modifiable_data.extra_infos["refresh_icon"])
        back=JLabel(img)
        back.setBounds(316,323,100,100)
        frame.add(back) 
        #function to select all the checklist 
        def selectall(event):
            if alles_auswahlen.isSelected():
                
                for i in range(0,number_orders):
                    l[i].setSelected(True)   
            else: 
                for i in range(0,number_orders):
                    l[i].setSelected(False)
        
        #creating the list of checkboxes                
        l=[]
        l_manuel=[]
        icon_pos=90
        var_untouchable2=100
        var_untouchable=100
        number_orders=0
        number_manual_orders=0
        displayed_orders=0
        begin_counter=6
        for i in range(0,length_order):
            if ((data_json_order[i]["pos_status"]=="open"))and(data_json_order[i]["order_source"]=="Takeaway")and(data_json_order[i]["received_time"]>"2020-08-08"):        
                l.append(JCheckBox("#"+str(data_json_order[i]["short_code"])+"-"+str(data_json_order[i]["received_time"])+"-"+str(data_json_order[i]["total_amount"])+"Euro")) 
                l[number_orders].setBackground(Color(24,222,192))
                l[number_orders].setForeground(Color.blue)
                l_manuel.append(JCheckBox(str(data_json_order[i]["short_code"])))
                number_orders=number_orders+1
        print(number_orders)
        for i in range(0,number_orders):
            l[i].setBounds(0,var_untouchable,230,80)
            l_manuel[i].setBounds(235,var_untouchable2,50,20)
            img=ImageIcon(modifiable_data.extra_infos["burger_icon"])
            back=JLabel(img)
            back.setBounds(195,icon_pos,100,100)
            displayed_orders=displayed_orders+1
            frame.add(l[i])
            frame.add(back) 
            frame.add(l_manuel[i])
            if i>=6:
                l_manuel[i].setVisible(False)
                l[i].setVisible(False)
                back.setVisible(False)
            icon_pos=icon_pos+90
            var_untouchable=var_untouchable+90
            var_untouchable2=var_untouchable2+90
        def next_orders(event):
            global begin_counter,number_orders,page
            if (number_orders-begin_counter<6)and(number_orders-begin_counter>0):
                for i in range(0,begin_counter):
                    l[i].setVisible(False)
                    l_manuel[i].setVisible(False)
                var_untouchable_next=100
                for i in range(begin_counter,number_orders):
                    l[i].setBackground(Color(24,222,192))
                    l[i].setForeground(Color.blue)
                    l[i].setBounds(0,var_untouchable_next,230,80)
                    l[i].setVisible(True)
                    l_manuel[i].setBounds(235,var_untouchable_next,50,20)
                    l_manuel[i].setVisible(True)
                    var_untouchable_next=var_untouchable_next+90
            else:
                begin_counter=begin_counter+6
                if begin_counter<number_orders:
                    for i in range(0,begin_counter-6):
                        if i<=len(l):
                            l[i].setVisible(False)
                            l_manuel[i].setVisible(False)
                
                var_untouchable_next=100
                if begin_counter<=number_orders:
                    page=page+1
                    pages_txt.setText(str(page)+"/"+str(int(round(number_orders/6))))
                    for i in range(begin_counter-6,begin_counter):
                        if i<len(l):
                            l[i].setBackground(Color(24,222,192))
                            l[i].setForeground(Color.blue)
                            l[i].setBounds(0,var_untouchable_next,230,80)
                            l[i].setVisible(True)
                            l_manuel[i].setBounds(235,var_untouchable_next,50,20)
                            l_manuel[i].setVisible(True)                            
                            var_untouchable_next=var_untouchable_next+90    
                    
                else:
                    begin_counter=number_orders
                    popError("Sie konnen nicht mehr weiter")
        next_btn=JButton(">>",actionPerformed=next_orders)
        next_btn.setBounds(100,640,60,40)
        frame.add(next_btn)
        def back_orders(event):
            global begin_counter,number_orders,page
            print("begin_counter = "+str(begin_counter))
            if begin_counter+6>number_orders:
                final=number_orders
            else:
                final=begin_counter
            for i in range(begin_counter,final):
                if i<=len(l):
                    l[i].setVisible(False)
                    l_manuel[i].setVisible(False)
            begin_counter=begin_counter-6
            var_untouchable_next=100
            if begin_counter>0:
                page=page-1
                pages_txt.setText(str(page)+"/"+str(int(round(number_orders/6))))
                for i in range(begin_counter-6,begin_counter):
                    l[i].setBackground(Color(24,222,192))
                    l[i].setForeground(Color.blue)
                    l[i].setBounds(0,var_untouchable_next,230,80)
                    l[i].setVisible(True)
                    l_manuel[i].setBounds(235,var_untouchable_next,50,20)
                    l_manuel[i].setVisible(True)
                    var_untouchable_next=var_untouchable_next+90    
            else:
                begin_counter=6
                popError("Sie konnen nicht weiter vorwarts")
            print("begin_counter = "+str(begin_counter))
        back_btn=JButton("<<",actionPerformed=back_orders)
        back_btn.setBounds(20,640,60,40)
        frame.add(back_btn)
        #the form of login
        pages_txt=JLabel("")
        pages_txt.setText(str(page)+"/"+str(int(round(number_orders/6))))
        pages_txt.setBounds(180,640,60,40)
        frame.add(pages_txt)
        Passwort_name=JLabel(modifiable_data.extra_infos["benutzer"])
        Passwort_name.setBounds(300,20,300,15)
        Passwort_name.setForeground(Color.red);
        Passwort_field=JTextField(10)
        Passwort_field.setBounds(300,40,150,30)
        Benutzer_name=JLabel(modifiable_data.extra_infos["passwort"])
        Benutzer_name.setForeground(Color.red);
        Benutzer_name.setBounds(300,80,150,10)
        Benutzer_field=JPasswordField(10)
        Benutzer_field.setBounds(300,100,150,30)
        #differnece text
        def auto_buch(event):
            #thread.exit()
            thread.start_new_thread(auto,(event,))
            
        def auto(event):
            if nb==0:
                popError("Es gibt keine moglichen Buchungen")
            elif (Benutzer_field.getText()=="")or (Passwort_field.getText()==""):
                popError("die Daten sind ungultig")
            else:
                
                frame.setExtendedState(JFrame.ICONIFIED)
                if not(exists("grosskassieren.png")):
                    popError("Bitte SubwayPOS offnen")
                while not(exists("grosskassieren.png")):
                    wait(0.1)
                wait("grosskassieren.png",5)
                click("grosskassieren.png")
                click("benutzer_field.png")
                type(Passwort_field.getText())
                click("passwort_field.png")
                type(Benutzer_field.getText())
                click("o.k.png")    
                if (exists("datenungultig.png")):
                    click("okgrun.png")
                    click("abbrechen.png")
                    frame.setExtendedState(JFrame.NORMAL)
                    popError("die Daten sind ungultig \nBitte, prufen Sie Ihre Daten!!")                            
                    return False
                while not(exists("productsscreen.png")):
                    time.sleep(0.02)
                    if exists("abgeschlossen.png"):
                        click("kleinkassieren.png")
                cod=str(cod_diff).replace(".","")
                paid=str(paid_diff).replace(".","")
                if cod_diff >0:
                    wait("nonfood.png")
                    click("nonfood.png")
                    wait("lb1.png")
                    click("lb1.png")
                    wait("rabat.png")
                    click("rabat.png")
                    wait("preisuber.png")
                    click("preisuber.png")
                    find("calc.png")
                        
                    for c in cod:
                        click(c+".png") 
                    wait("eingabe.png")
                    click("eingabe.png")
                    find("gesamt.png")
                    click("gesamt.png")
                    wait("ja.png")
                    click("ja.png")
                    wait("ok.png")
                    click("ok.png")
                    wait("hauskonto.png")
                    click("hauskonto.png")
                    wait("dellieferbar.png")
                    click("dellieferbar.png")
                if paid_diff>0:
                    wait("nonfood.png")
                    click("nonfood.png")
                    wait("lb1.png")
                    click("lb1.png")
                    wait("rabat.png")
                    click("rabat.png")
                    wait("preisuber.png")
                    click("preisuber.png")
                    find("calc.png")
                    for c in paid:
                        click(c+".png") 
                    wait("eingabe.png")
                    click("eingabe.png")
                    find("gesamt.png")
                    click("gesamt.png")
                    wait("ja.png")
                    click("ja.png")
                    wait("ok.png")
                    click("ok.png")
                    wait("hauskonto.png")
                    click("hauskonto.png")
                    wait("lieferando.png")
                    click("lieferando.png")
                    
                
        path=modifiable_data.extra_infos["diff_file"]
        f=open(path)
        try:            
            nb=f.readline()
            print(nb)
        except:
            nb=None
        try:
            cod_diff=f.readline()
            print(cod_diff)
        except:
            cod_diff=None
        try:
            paid_diff=f.readline()
            print(paid_diff)
        except:
            paid_diff=None
        f.close()
        if nb=="":
            nb="0"
        if cod_diff=="":
            cod_diff="0,00"
        if paid_diff=="":
            paid_diff="0,00"
        def set_null(event):
            diff_text1.setText("fuer 0 Euro Bestellungen: ")
            diff_text2.setText("Sie haben 0,00 Euro Differenz von Online Bestellungen.")
            diff_text3.setText("Sie haben 0,00 Euro Differenz von Bar Bezahlten Bestellungen.")
            open(path,"w").close()
            
        btn_buchen=JButton(modifiable_data.extra_infos["manuel"],actionPerformed=set_null)
        
        btn_buchen.setBounds(270,320,150,20)
        btn_auto=JButton(modifiable_data.extra_infos["auto"],actionPerformed=auto_buch)
        btn_auto.setBounds(450,320,150,20)
        btn_auto.setEnabled(False)
        
        diff_text1=JLabel("fuer "+nb+" Bestellungen: ")
        diff_text1.setBounds(285,200,700,70)
        diff_text2=JLabel("Sie haben "+paid_diff+" Euro Differenz von Online Bestellungen.")
        diff_text2.setBounds(285,220,700,70)
        diff_text3=JLabel("Sie haben "+cod_diff+" Euro Differenz von Bar Bezahlten Bestellungen.")
        diff_text3.setBounds(285,240,700,70)
        buchen_text=JLabel("BITTE BUCHEN SIE DIE DIFFERENZ")
        buchen_text.setBounds(285,280,300,30)
        check_time=JCheckBox(modifiable_data.extra_infos["bestellzeit"])
        check_time.setBounds(285,500,220,80)
        check_time.setBounds(285,500,220,80)
        check_time.setBackground(Color(116,128,126))
        check_time.setForeground(Color.black)
        #checkbox for selecting all                
        alles_auswahlen=JCheckBox("Alle auswahlen("+str(number_orders)+" Bestellungen)", actionPerformed =selectall)
        alles_auswahlen.setBounds(0,10,230,80)
        alles_auswahlen.setBackground(Color(24,222,192))
        alles_auswahlen.setForeground(Color.red)                  
        back=JLabel(img2)
        back.setBounds(520,570,100,100)
        #setting the GUI objects
        frame.add(back)
        frame.add(Passwort_name)
        frame.add(Benutzer_name)
        frame.add(Benutzer_field)
        frame.add(Passwort_field)
        frame.add(btn)
        frame.add(btn_manual)
        frame.add(alles_auswahlen)
        frame.add(refresh_btn)
        frame.add(version_text)
        frame.add(diff_text1)
        frame.add(diff_text2)
        frame.add(diff_text3)
        frame.add(buchen_text)
        frame.add(btn_buchen)
        frame.add(check_time)
        frame.add(btn_auto)
        frame.setVisible(True)
    except Exception as e:
            er=str(e)
            logging.error(er)
            popError("Bitte starten Sie den POS_BOT neu")
