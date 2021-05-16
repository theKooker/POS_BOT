from javax.swing import JFrame,JLabel
from java.awt import Color
import sys
from sikuli import *
sys.path.append("C:\Everesto\Everersto-POS-Bot\POS_Bot\modifiable_data.sikuli")
import modifiable_data
setBundlePath(modifiable_data.extra_infos["images_path"])
import time
def alert_pop():
    frame=JFrame("ALERT")
    frame.setSize(200,100)
    txt=JLabel(modifiable_data.extra_infos["alert_txt"])
    txt.setBounds(100,100,200,10)
    frame.add(txt)
    frame.setVisible(True)
    frame.setAlwaysOnTop(True)
    tr=True
    while tr==True :
        frame.getContentPane().setBackground(Color.white)
        time.sleep(0.5)
        frame.getContentPane().setBackground(Color.red)
        time.sleep(0.5)
        if exists("lieferando.png"):
            tr=False
    frame.dispose()
def help_pop():
    frame=JFrame("ALERT")
    frame.setSize(200,100)
    txt=JLabel(modifiable_data.extra_infos["help_txt"])
    txt.setBounds(100,100,200,10)
    frame.add(txt)
    frame.setVisible(True)
    frame.setAlwaysOnTop(True)
    tr=True
    while tr==True :
        frame.getContentPane().setBackground(Color.yellow)
        if exists("lieferando.png"):
            tr=False
    frame.dispose()
def loading_pop():
    frame=JFrame("LOADING")
    frame.setSize(200,100)
    frame.setLocation(150,100)
    txt=JLabel("warten Sie ...")
    txt.setBounds(100,100,200,10)
    frame.add(txt)
    frame.getContentPane().setBackground(Color.yellow)
    txt.setBackground(Color.red)
    frame.setVisible(True)
    tr=True
    while tr==True:
        txt.setVisible(False)
        time.sleep(0.3)
        txt.setVisible(True)
        if exists("loading_indice.png"):
            tr=False
    frame.dispose()
