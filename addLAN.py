import socket

addorremove=input("add or remove address?: ")
ip=input("Enter ip of the camera:")
address=input("Enter email address:")
passw=input("Enter the password:")
sensitivity=input("Enter your desired sensitiviy:")

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ip,6101))
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
