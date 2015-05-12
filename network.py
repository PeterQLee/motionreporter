import socket
import threading

class Server(threading.Thread):
    ##handles all incoming clients
    nextport=0
    handleport=0 #port used for delegating
    def __init__(self,mclass,commclass,handleport,azureip,azureport,password):
        self.mclass=mclass
        self.commclass=commclass
        self.handleport=handleport
        self.password=password
    def getNextPort(self):
        #note, beware possible infinite loop here if it tries to reuse the same one
        
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(("",0))
        port=s.getsockname()[1]
        s.close()
        return port
    
    #Assuming Azure port is already configured
    
    def serve(self):
        #delegates ports for communication as well as desired sensitvity
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((socket.gethostname(),self.handleport))
        while True:
            (sendsock,address)=s.accept()
            
            #check if it is an azure thing too
            #if address==self.azureaddress:
            #    aid=sendsock.recv(4)
            #    self.commclass.addAzureID(aid)
                #get and add sensitvity value
            #xs    sendsock.close()
                
                
            #do authentication yadda yadda
            nextport=getNextPort()            
            sendsock.send(nextport)

            chk=sendsock.recv(2) #arbitrary value
            while (chk==0):
                nextport=getNextPort()
                sendsock.send(nextport)

                chk=sendsock.recv(2) #arbitrary value
           
            self.commclass.addLANSocket(address,nextport)
            #get and add sensitvity to mainclass
            sendsock.close()

            
    
#class Outgoing(threading.Thread):
#    def __init__(self,address):
def connectAzure():pass

class Communications(threading.Thread):
    LANsock={}
    Azureid=[]
    AzureSock=None
    LANports={}
    Azureport=0
    nextport=0
    def __init__(self,azureip,azureport):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((azureip,azureport))
            self.AzureSock=s
            self.Azureport=azureport
        except:
            print("bad")
            raise
    def addAzureID(aID):
        self.Azureid.append(aID)
    def addLANSocket(address,port):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((address,port))
            #            nextport=findnextport(nextport)#
            self.LANsock[address]=s
            self.LANports[address]=port
        except:
            print("trouble connecting port")
    def removeAzureID(aID):
        try:
            self.Azureid.remove(aID)
        except:
            print("id does not exist")
    def removeLanAddress(address):
        try:
            LANsock[address].close()
            del LANsock[address]
            del LANports[address]
        except:
            print("Error removing lan address")
    
        
    def sendLANAlert(address):
        #if a high enough motion detected, will send alert to client
        try: 
            line=self.LANsock[address]
            line.send(self.ALERT)
        except:
            print("ERROR SENDING DATA TO "+address)
    def sendAzureAlert(AID):
        #send id to azure server
        try:
            line=AzureSock.send(AID)
        except:
            print("ERROR SENDING DATA TO AZURE!!!")
    
