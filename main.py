import cv2
import threading
from network2 import *
import sys
from detection import *
from mailer import *
import time
#import Queue
class Main:
    LANintense={}
    Azureintense={}
    cooladdr=[]
    cooldowns=[]
    halt=False
    #intensities={}
    def __init__(self,azureip,azureport,password,handleport,mailname,mailpass,name,debugflag=False,camnum=0):
        self.azureip=azureip
        self.azureport=azureport
        self.debugflag=debugflag
        self.devnum=camnum
        self.cooldowns=[]
        self.cooladdr=[]
        self.mail=Mailer(mailname,mailpass)
        #selfcommclass=Communications(azureip,azureport)
        self.azcomm=AzureComm(self,handleport,azureip,azureport,password,name)#
        
        self.LANcomm=LANComm(self,handleport,password) #need to make handleports different
        
        try:
            pass
            self.azcomm.validateNode()#
            self.azcomm.start()#
        except:
            
            print("Could not validate node on azure")
            
       
        self.LANcomm.start()
        #start two new thread, addnewuser and 
        
        #self.servclass=Server(self,self.commclass,handleport,azureip,azureport,password)

        #start server
        #self.servclass.serve()
        #self.intensities["ayy@lmao.com"]=5

    #def addAddress(addres,intens):
    #    if not addres in self.intensities:
    #        self.intensities[addres]=intens
    #    else:
    #        print("address "+addres+" already exists")
    def addAzure(self,aid,intens):
        #will either update, or create address with intense
        self.Azureintense[aid]=intens
        
        #if not self.Azureintense[aid]:
        #    self.Azureintense[aid]=intens
        #else:
        #    print("aid already exists!")

    def addLAN(self,address,intens):
    #    if not self.LANintense[address]:
         self.LANintense[address]=intens
    #    else:
    #        print("LAN address already exists!")
    
    def removeAddress(self,address):
        if address in self.LANintense:del self.LANintense[address]
        if address in self.Azureintense:del self.Azureintense[address]
    #def removeAzure(self,aid):
    #    if self.Azureintense[aid]:del self.Azureintense[aid]
    #def removeLAN(self,address):
    #    if self.LANintense[aid]:del self.LANintense[aid]
    def haltCapture(self):
        self.halt=True
    def resumeCapture(self):
        self.halt=False
    def captureMotion(self):
        try:
            cam=cv2.VideoCapture(self.devnum)
            
            while True:

                if self.halt:
                    print("Halted")
                while self.halt:
                    time.sleep(10)
                
                #capture video
                ret,frame=cam.read()


                gray1=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #gray1=cv2.fastNlMeansDenoising(gray1)
                ret,frame=cam.read()
                gray2=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #gray2=cv2.fastNlMeansDenoising(gray2)
                ret,frame=cam.read()
                gray3=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #gray3=cv2.fastNlMeansDenoising(gray3)
                #get summated greyscale
                
                disp=getConstantMotionValue((gray1,gray2,gray3))
                meanconst=cv2.mean(disp)
                #need to save timelapsed values as well
                #meanlapse=
                print(meanconst)
                
                for i in self.LANintense:#LANintense:
                    if self.LANintense[i]<=meanconst[0] and i not in self.cooladdr: #these will be scaled by something ofcourse
                        #start a new thread for this, so it doesn't clog GUI
                        #self.LANcomm.sendLANAlert(i)
                        
                        #self.cooldown.append(time.time())#+5 minutes
                        self.cooladdr.append(i)
                        threading.Timer(30,self.removeCooldown,(i,)).start() #300 seconds
                        #send email
                        
                        threading.Thread(target=self.mail.send_email,args=(i,frame)).start()
                        print("BREAK IN IN PROCESS!")
                
                for i in self.Azureintense:
                    print( "az"+str(i))
                    if self.Azureintense[i]<=meanconst[0] and i not in self.cooladdr: #these will be scaled by something ofcourse

                        
                        #start a new thread for this, so it doesn't clog GUI

                        #make sure ample time after detection
                        #also make sure email hasn't been sent in last 5 minutes 
                        
                        self.azcomm.sendAlert(i) 

                        
                        #send email
                        #self.cooldown.append(time.time())#+5 minutes deprecated
                        self.cooladdr.append(i)
                        threading.Timer(30,self.removeCooldown,(self.cooladdr)).start()
                        threading.Thread(target=self.mail.send_email,args=(i,frame)).start()
                        print("BREAK IN IN PROGRESS")
                
                if self.debugflag:
                    cv2.imshow('frame',disp)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
            cam.release()
            if self.debugflag:
                cv2.destroyAllWindows()
            #self.azcomm.kill()
            self.LANcomm.kill()
            self.azcomm.kill()            
            #if 
        except:
            #if this fails for some reason, send signal to all dependent devices
            print("Error in main capture")
            cam.release()
            if self.debugflag:
                cv2.destroyAllWindows()
            self.LANcomm.kill()
            self.azcomm.kill()
            raise
    def removeCooldown(self,addr):
        #multithreaded, handles Queue for when to send emails
        #once current time is 5 minutes past expirey, remove time index as well as respective cooladdr
        self.cooladdr.remove(addr)
        
#initialize main
#if (len(sys.argv)<5):
#    print( "Usage: python3 main.py azureip azureport handleport,cameranumber")
#else:    
passw=input("Enter your desired password:")
    #instead of using args, read from config file
f=open("settings","r")
ars=f.read()

ars=ars.split(",")
for i in range(len(ars)):
    #remove whitespaces
    ars[i]=ars[i].replace("\n","")
    ars[i]=ars[i].replace(" ","")
    ars[i]=ars[i].replace("\r","")
    ars[i]=ars[i].replace("\t","")

print(ars)
print(sys.argv)
#m=Main(sys.argv[1],int(sys.argv[2]),passw,sys.argv[3],True,int(sys.argv[4]))
m=Main(ars[0],int(ars[1]),passw,int(ars[2]),ars[4],ars[5],ars[6],True,int(ars[3]))
m.captureMotion()
