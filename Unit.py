import os
import sys
import PyQt5
import random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
import time
import datetime
from init import *
#broker.hivemq.com
# Creating Client name - should be unique 
global clientname
r=random.randrange(1,10000000)
clientname="IOT_client-Id1234-"+str(r)
unit_topic = 'pr/SmartHome/Light/main'
global ON
ON = False

class Mqtt_client():
    
    def __init__(self):
        # broker IP adress:
        self.broker=''
        self.topic=''
        self.port='' 
        self.clientname=''
        self.username=''
        self.password=''        
        self.subscribeTopic=''
        self.publishTopic=''
        self.publishMessage=''
        self.on_connected_to_form = ''
        
    # Setters and getters
    def set_on_connected_to_form(self,on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form
    def get_broker(self):
        return self.broker
    def set_broker(self,value):
        self.broker= value         
    def get_port(self):
        return self.port
    def set_port(self,value):
        self.port= value     
    def get_clientName(self):
        return self.clientName
    def set_clientName(self,value):
        self.clientName= value        
    def get_username(self):
        return self.username
    def set_username(self,value):
        self.username= value     
    def get_password(self):
        return self.password
    def set_password(self,value):
        self.password= value         
    def get_subscribeTopic(self):
        return self.subscribeTopic
    def set_subscribeTopic(self,value):
        self.subscribeTopic= value        
    def get_publishTopic(self):
        return self.publishTopic
    def set_publishTopic(self,value):
        self.publishTopic= value         
    def get_publishMessage(self):
        return self.publishMessage
    def set_publishMessage(self,value):
        self.publishMessage= value 
        
        
    def on_log(self, client, userdata, level, buf):
        print("log: "+buf)
            
    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("connected OK")
            self.on_connected_to_form();            
        else:
            print("Bad connection Returned code=",rc)
            
    def on_disconnect(self, client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
            
    def on_message(self, client, userdata, msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message from:"+topic, m_decode)
        mainwin.connectionDock.update_btn_state(m_decode)

    def connect_to(self):
        # Init paho mqtt client class        
        self.client = mqtt.Client(self.clientname, clean_session=True) # create new client instance        
        self.client.on_connect=self.on_connect  #bind call back function
        self.client.on_disconnect=self.on_disconnect
        self.client.on_log=self.on_log
        self.client.on_message=self.on_message
        self.client.username_pw_set(self.username,self.password)        
        print("Connecting to broker ",self.broker)        
        self.client.connect(self.broker,self.port)     #connect to broker
    
    def disconnect_from(self):
        self.client.disconnect()                   
    
    def start_listening(self):        
        self.client.loop_start()        
    
    def stop_listening(self):        
        self.client.loop_stop()    
    
    def subscribe_to(self, topic):        
        self.client.subscribe(topic)
              
    def publish_to(self, topic, message):
        self.client.publish(topic,message)        
      
class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self,mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput=QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)
        
        self.ePort=QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)
        
        self.eClientID=QLineEdit()
        global clientname
        self.eClientID.setText(clientname)
        
        self.eUserName=QLineEdit()
        self.eUserName.setText(username)
        
        self.ePassword=QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)


        self.eBrightness=QPushButton()
        self.eBrightness.setStyleSheet(f"""
            background-color: #FFFFFF;  /* White background color */
            color: black;  /* Text color (black) */
            border: 2px solid #DDDDDD;  /* Border style (a light gray) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
        self.eBrightness.setToolTip("1")
        
        self.eConnectbtn=QPushButton("Connect", self)
        self.eConnectbtn.setToolTip("Click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet(f"""
        background-color: #f5f5f5;  /* Light gray background color */
        color: #333333;  /* Text color (dark gray) */
        border: 2px solid #dcdcdc;  /* Border style (light gray) */
        padding: 5px 10px;  /* Padding (adjust as needed) */""")
        
        self.eSubscribeTopic=QLineEdit("")
        self.eSubscribeTopic.setText(unit_topic)

        self.ePushtbtn=QPushButton()
        self.ePushtbtn.setStyleSheet(f"""
            background-color: #FFFFFF;  /* White background color */
            color: black;  /* Text color (black) */
            border: 2px solid #DDDDDD;  /* Border style (a light gray) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
        self.ePushtbtn.setToolTip("OFF")

        formLayot=QFormLayout()
        formLayot.addRow("Connect",self.eConnectbtn)
        formLayot.addRow("Host",self.eHostInput )
        formLayot.addRow("Port",self.ePort )
        formLayot.addRow("Client ID", self.eClientID)
        formLayot.addRow("Sub topic",self.eSubscribeTopic)
        formLayot.addRow("Brightness",self.eBrightness)
        formLayot.addRow("Mode",self.ePushtbtn)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Light") 
        
    def on_connected(self):
        self.eConnectbtn.setStyleSheet(f"""
        background-color: #4CAF50;  /* Green background color */
        color: white;  /* Text color (white) */
        border: 2px solid #45a049;  /* Border style (a darker green) */
        padding: 5px 10px;  /* Padding (adjust as needed) */""")
                    
    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())        
        self.mc.connect_to()        
        self.mc.start_listening()
        self.mc.subscribe_to(self.eSubscribeTopic.text())
    
    def update_btn_state(self,text):
        if(text.isdigit()):
            self.eBrightness.setText(text)
            brightlevel = int(text)
            text_color = "white" if brightlevel < 8 else "black"
            if(brightlevel == 10):
                backcolor = 255
            elif(brightlevel == 1):
                backcolor = 0
            else:
                brightlevel = 10 - brightlevel
                backcolor = 255 - (brightlevel-1) * 25
            self.eBrightness.setStyleSheet(f"""
            background-color: rgb({backcolor}, {backcolor}, {backcolor});
            color: {text_color};
            border: 2px solid rgb({backcolor - 25}, {backcolor - 25}, {backcolor - 25});  /* Border style (a darker gray) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
            
        global ON
        if "OFF" in text:
            print("Turn off...")
            self.ePushtbtn.setStyleSheet("background-color: black")
            self.ePushtbtn.setToolTip("OFF")
            self.mc.disconnect_from()        
            self.mc.stop_listening()
            ON = False
        elif "Red" in text:
            print("Red mode is activated...")
            self.ePushtbtn.setStyleSheet(f"""
            background-color: #FF0000;  /* Red background color */
            color: white;  /* Text color (white) */
            border: 2px solid #CC0000;  /* Border style (a darker red) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
            self.ePushtbtn.setToolTip("Red")
            self.ePushtbtn.setText("Red")
            ON = True 
        elif "Green" in text:
            print("Green mode is activated...")
            self.ePushtbtn.setStyleSheet(f"""
            background-color: #4CAF50;  /* Green background color */
            color: white;  /* Text color (white) */
            border: 2px solid #45a049;  /* Border style (a darker green) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
            self.ePushtbtn.setToolTip("Green")
            self.ePushtbtn.setText("Green")
            ON = True    
        elif "Blue" in text:
            print("Blue mode is activated...")
            self.ePushtbtn.setStyleSheet(f"""
            background-color: #0074cc;  /* Blue background color */
            color: white;  /* Text color (white) */
            border: 2px solid #005aa3;  /* Border style (a darker blue) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
            self.ePushtbtn.setToolTip("Blue")
            self.ePushtbtn.setText("Blue")
            ON = True    
        elif "Yellow" in text:
            print("Yellow mode is activated...")
            self.ePushtbtn.setStyleSheet(f"""
            background-color: #FFFF00;  /* Yellow background color */
            color: black;  /* Text color (black) */
            border: 2px solid #FFD700;  /* Border style (a darker yellow) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
            self.ePushtbtn.setToolTip("Yellow")
            self.ePushtbtn.setText("Yellow")
            ON = True    
        elif "White" in text:
            print("White mode is activated...")
            self.ePushtbtn.setStyleSheet(f"""
            background-color: #FFFFFF;  /* White background color */
            color: black;  /* Text color (black) */
            border: 2px solid #DDDDDD;  /* Border style (a light gray) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
            self.ePushtbtn.setToolTip("White")
            self.ePushtbtn.setText("White")
            ON = True
        elif "Pink" in text:
            print("Pink mode is activated...")
            self.ePushtbtn.setStyleSheet(f"""
            background-color: #FF69B4;  /* Pink background color */
            color: white;  /* Text color (white) */
            border: 2px solid #FF1493;  /* Border style (a darker pink) */
            padding: 5px 10px;  /* Padding (adjust as needed) */
            """)
            self.ePushtbtn.setToolTip("Pink")
            self.ePushtbtn.setText("Pink")
            ON = True
        else:
            print("=========================")   
      
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
                
        # Init of Mqtt_client class
        self.mc=Mqtt_client()
        
        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(1200, 600, 450, 300)
        self.setWindowTitle('Light Unit')

        # Init QDockWidget objects        
        self.connectionDock = ConnectionDock(self.mc)        
        
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)       

app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()