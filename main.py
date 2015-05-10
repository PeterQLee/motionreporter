import cv2
import threading
from network import *
import sys
from detection import *
class Main:
    LANintense={}
    Azureintense={}
    
    def __init__(self,azureip,azureport,password,handleport,debugflag=False,camnum=0):
        self.azureip=azureip
        self.azureport=azureport
        self.debugflag=debugflag
        self.devnum=camnum
        #self.commclass=Communications(azureip,azureport)
        #self.servclass=Server(self,self.commclass,handleport,azureip,azureport,password)

        #start server
        #self.servclass.serve()
        self.LANintense["ayy@lmao.com"]=5
    def addAzure(aid,intens):
        if not self.Azureintense[aid]:
            self.Azureintense[aid]=intens
        else:
            print("aid already exists!")

    def addLAN(address,intens):
        if not self.LANintense[address]:
            self.LANintense[address]=intens
        else:
            print("LAN address already exists!")
    
    def removeAzure(self,aid):
        if self.Azureintense[aid]:del self.Azureintense[aid]
    def removeLAN(self,address):
        if self.LANintense[aid]:del self.LANintense[aid]
    
    def captureMotion(self):
        try:
            cam=cv2.VideoCapture(self.devnum)
            
            while True:
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
                
                for i in self.LANintense:
                    if self. LANintense[i]<=meanconst[0]: #these will be scaled by something ofcourse
                        #start a new thread for this, so it doesn't clog GUI
                        #self.commclass.sendLANAlert(i)
                        print("BREAK IN IN PROCESS!")
                """
                for i in self.Azureintense:
                    if self.Azureintense[i]<=meanconst: #these will be scaled by something ofcourse
                        #start a new thread for this, so it doesn't clog GUI
                        self.commclass.sendAzureAlert(i)
                """
                if self.debugflag:
                    cv2.imshow('frame',disp)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                        
            #if 
        except:
            #if this fails for some reason, send signal to all dependent devices
            print("Error in main capture")
            cam.release()
            cv2.destroyAllWindows()
            raise
#initialize main
passw=input("Enter your desired password:")
print(sys.argv)
m=Main(sys.argv[1],int(sys.argv[2]),passw,sys.argv[3],True,int(sys.argv[4]))
m.captureMotion()
