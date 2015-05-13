import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

addorremove=input("add, remove, address, halt or resume?: ")
ip=input("Enter ip of the camera:")
passw=input("Enter the password:")
s.connect((ip,6101))
if addorremove=="halt" or addorremove=="resume":
    s.send(bytes(addorremove,"utf-8"))
    s.recv(128)
    s.send(bytes(passw,"utf-8"))
else:
    
    address=input("Enter email address:")
   
    sensitivity=input("Enter your desired sensitiviy:")



    s.send(bytes(addorremove,"utf-8"))
    s.recv(128)
    s.send(bytes(passw,"utf-8"))
    ret=s.recv(128)
    if ret.decode()=="1":
        s.send(bytes(address,"utf-8"))
        s.recv(128)
        s.send(bytes(sensitivity,"utf-8"))
    else:
        print("wrong password")
s.close()
    
