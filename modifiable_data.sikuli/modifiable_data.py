#!/usr/bin/env python
# -*- coding: utf-8 -*-
mode={"mode":"staging"}
network_infos={
              "login_url":"https://"+mode["mode"]+".everesto.net/api/user/login",
              "store_id":"dc0bc4a9-034e-4aef-a908-080e458b9a92",
              "order_url":"https://"+mode["mode"]+".everesto.net/api/orders?order_by=received_time&is_active=false&store_id=",
              "put_url":"https://"+mode["mode"]+".everesto.net/api/orders/",
              "username":"dhia@everesto.net",
              "passwort":"M123456!"}

extra_infos={"login_file":"C:\Everesto\Everersto-POS-Bot\POS_Bot\login.txt",
             "file_path":r"C:\Everesto\Everersto-POS-Bot\POS_Bot\items_with_pictures_adresses.txt",
             "images_path":"C:\Everesto\Everersto-POS-Bot\POS_Bot\pics",
             "times_http":5,
             "times_click":5,
             "error_file":r"C:\\Everesto\\Everersto-POS-Bot\\POS_Bot\\traceback_LOG\\",
             "log_level":5,
             "log_format":"%(asctime)s:%(levelname)s:%(process)d:%(module)s:%(message)s",
             "refresh_icon":"C:\Everesto\Everersto-POS-Bot\icons8-wiederkehrender-termin-50.png",
             "kasse_icon":"C:\Everesto\Everersto-POS-Bot\POS_Bot\kasse.png",
             "burger_icon":"C:\Everesto\Everersto-POS-Bot\POS_Bot\icon.png",
             "everesto_icon":"C:\Everesto\Everersto-POS-Bot\POS_Bot\everesto.jpg",
             "alert_txt":"POS_BOT IS RUNNING!",
             "help_txt":"WIR BRAUCHEN IHRE HILFE",
             "ubertragen":"Ubertragen",
             "version":"VERSION 0.9.7",
             "benutzer":"POS Benutzekennung",
             "passwort":"POS Passwort",
             "aktualisieren":"Aktualisieren",
             "bestellzeit":"Echte Bestellzeit verwenden",
             "manuel":"manuel gebucht",
             "auto":"auto Buchung",
             "app_name":"Dashboard.exe",
             "frame_name":"POS_BOT Everesto",
             "diff_file":r"C:\\Everesto\\Everersto-POS-Bot\\POS_Bot\\diff.txt",
             "manuel_buchung":"(POS) man. gebucht"}
##NOTICE: THERE ARE SOME TEXTS IN MAIN.SIKULI AND RESULT.SIKULI WHICH YOU CAN EDIT :)
