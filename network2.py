import socket
import threading

class LANComm(threading.Thread):
    def __init__(self,mclass,handleport,password):
        threading.Thread.__init__(self)
        self.mclass=mclass

        #self.handleport=handleport                                                                                                   
        self.password=password
        self.killflag=False
        try:
            self.LANsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #self.LANsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.LANsock.bind(("127.0.0.1",handleport))
            self.LANsock.listen(5)
        except:
            print("stuff went wrong")
            raise
       
    def addLANUser(self): #may be deprecated
        
        while not self.killflag:
            (csck,ip)=self.LANsock.accept()
            addorremove=csck.recv(128).decode()
            csck.send(bytes("1","utf-8"))
            dat=csck.recv(128).decode()#listens for password                                                   
            if dat==self.password:
                csck.send(bytes("1","utf-8")) #byte this [1 means success else failure                       
                #check semd error                                                                                                    
                dat=csck.recv(128).decode()
                csck.send(bytes("1","utf-8"))
                #send confirmation                                                                                                   
                sens=float(csck.recv(128).decode()) #decode to int
                if addorremove=="add":                                                                         
                    self.mclass.addLAN(dat,sens)
                else:
                    self.mclass.removeAddress(dat)
            csck.close()
       
        self.LANsock.close()
    def run(self):
        self.addLANUser()
    def kill(self):
        #send blank copies to self, in order to stop loop
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.killflag=True
        s.connect(("127.0.0.1",6102))
        s.send(bytes(1))
        s.close()
       
        #sock.send(byte(0))->localhost
class AzureComm(threading.Thread):
    delegport=6000
    ndcom=None
    addsock=None
    LANsock=None
    def __init__(self,mclass,handleport,azureip,azureport,password):
        threading.Thread.__init__(self)
        self.mclass=mclass
        
        #self.handleport=handleport
        self.password=password
        self.azureip=azureip
        self.killflag=False
        #self.valdiateNode() #maybe add in??
        try:
            #self.LANsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.addsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #self.LANsock.bind(("127.0.0.1",6100))
        except:
            print("Cannot make azure socket")
            raise
    def validateNode(self):
        #sends a request to azure server to be added
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.azureip,self.delegport))
        #s.send(bytes(password)) #send password,name,maxclients
        s.send("jerry".encode('utf-8'))
        s.recv(128)
        #s.send(str(6).encode('utf-8'))
        #while True:
        #num1=int(s.recv(128).decode())
#keep sending negatives to client until appopriate port is selected
            #pass
        #s.send(("1").encode('utf-8'))
        #num2=int(s.recv(128).decode())
        #self.ndcom=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #self.num1=num1
        #self.ndcom.connect((self.azureip,num1)) ## for alerts
        
        #self.num2=num2
        #keep trying until it works
        self.ndcom=s #new
        
        while True:
            try:
                self.addsock.connect((self.azureip,self.azureport+1))## for adding users
                break
            except OSError:
                continue
        
        
        
        #s.close()
    """def addLANUser(self): #may be deprecated
        while True:
            dat=self.LANsock.recv(128)#listens for password                                                   
            if dat==self.password:
                self.LANsock.send(1) #byte this [1 means success else failure                       
                #check semd error                                                                                                    
                dat=self.LANsock.recv(128)
                #send confirmation                                                                                                   
                sens=self.LANsock.recv(128) #decode to int                                                                           
                mclass.addAddress(dat.decode(),sens)
            else:
                self.LANsock.send(0)"""
    def reconnect(self,sk,ip,num):
        print("Lost connection, reconnecting to azure")
        while True:
            try:
                sk.connect((ip,num))
            except:
                #add in sleep
                continue
        
    def listenForUsers(self): #multithread
        while not self.killflag:

            try:
                addorremove=self.addsock.recv(128).decode()
                self.addsock.send(bytes("1","utf-8"))
                dat=self.addsock.recv(128)#listens for password
            except:
                self.validatenode()
                #reconnect(self.addsock,self.azureip,self.num2)
                                                  
            if dat==self.password:
                self.addsock.send(bytes("1","utf-8")) #byte this [1 means success else failure 
                #check semd error
                dat=self.addsock.recv(128) #Email
                #send confirmation
                self.addsock.send(bytes("1","utf-8"))
                sens=float(self.addsock.recv(128).decode()) #sensitivy
                if addorremove=="add":
                    mclass.addAzure(dat.decode(),sens)
                else:
                    mclass.removeAddress(dat.decode())
                
            else:
                self.addsock.send(0)
                
            #if these are correct
            #add them to the list through the main class
            #and send success
            #otherwise, send failure
    def sendAlert(self,addre,img=None): #will use port 6000
        #self.ndcom.connect((self.azureip,self.num1)) ## for alerts
        self.ndcom.send(addre) #send address (convert)
        
        #self.ndcom.recv(1)

        
        #convert, ensure it exists and stuff
        #self.ndcom.send(img)
        #send image, if applicable
        #server should append timestamp
        #self.ndcom.close()
    def kill(self):
        self.killflag=False
        self.cleanup()
        #sock.send(0) localhost
    def cleanup(self):
        self.ndcom.close()
        self.addsock.close()
    def run(self):
        self.listenForUsers()
    
    ##note, all these functions should be executed on a seperate thread
