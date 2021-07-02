# 

import socket 
import threading
import os
import re 
import pickle
from tkinter import *  
from tkinter import font
import shutil
HEADER = 64
PORT = 9999
host = socket.gethostname()
SERVER = socket.gethostbyname(host)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "e"
global temp
global c_name
c_name = ""
temp = ""

parent = os.getcwd()
clients=[] 
name=[]
client_id=-1
timer=-1
root = Tk()
signal=""
signal_disconnected=""

# m for displaying all operation on server on by one
global m
m = ""
# 1 thread for connection 
class handle_client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)

        server.listen(5)
        flag=0
        count=0
        while(True):  
            c, addr = server.accept()
            if(len(clients)==0):
                count=1
            else:   
                x=sorted(clients)
                count=int(x[len(clients)-1])+1
            t=myThread(c,count)
            t.start() 
# 2 Thread for handling connection 
class myThread(threading.Thread):
    def __init__(self,c,id):
        threading.Thread.__init__(self)
        self.c=c
        self.id=id
        self.n="" 
        self.msg=100
        self.flag = False
    def run(self): 
        err=0  
        clients.append(self.id) 
        global signal_disconnected
        if(len(clients)==4):
            clients.remove(self.id)
            self.msg = 404
            data = pickle.dumps(self.msg)
            self.c.send(data)   
        else:
            global client_id
            while (True):    
                try:
                    if(self.msg==100): 
                        signal_disconnected=""
                        print("asking name")
                        self.msg=201  
                    else:
                        self.msg=200
                    data = pickle.dumps(self.msg)
                    #print("data",data)
                    self.c.send(data)
                    rdata = pickle.loads(self.c.recv(1024))

                    #1 excetue for first time takes client name and create client's name directory
                    if(self.flag==False):
                        global c_name
                        c_name = rdata
                        print(c_name)
                        self.flag = True 
                        create_directory(rdata)
                    if(rdata == 200):
                        #print("got 200")
                        self.msg = 200
                    # 2 execute when directory operation called. 
                    if(re.search("#",str(rdata))!=None and self.flag==True):
                        sub_dir = rdata.split("#")
                        print("sub_dir array matters")
                        print(sub_dir)
                        if str(sub_dir[0]) == "1":
                            flag =  create_sub_directory(sub_dir[1],sub_dir[2])
                            if(flag==0):
                                #conn.send("Directory already exist".encode(FORMAT))
                                a = "Directory already exist"
                                data = pickle.dumps(a)
                                self.c.send(data)  

                            elif(flag==1):
                                #conn.send("Directory sucessfully created".encode(FORMAT))
                                #global temp
                                data = pickle.dumps(temp)
                                self.c.send(data)  
                        if str(sub_dir[0]) == "2":
                            flag = delete_sub_directory(sub_dir[1],sub_dir[2])
                            if(flag==0):
                                a = "source_path or destination_path is not exist"
                                #conn.send("source_path or destination_path is not exist".encode(FORMAT))
                                data = pickle.dumps(a)
                                self.c.send(data)  
                            elif(flag==1): 
                                #global temp
                                data = pickle.dumps(temp)
                                self.c.send(data)  

                                #conn.send("Directory sucessfully moved".encode(FORMAT))
                        if str(sub_dir[0]) == "3":
                            flag = moving_directory(sub_dir[1],sub_dir[2],sub_dir[3])
                            if(flag==0):
                                a = "source_path or destination_path is not exist"
                                data = pickle.dumps(a)
                                self.c.send(data)  
                                #conn.send("source_path or destination_path is not exist".encode(FORMAT))
                            elif(flag==1): 
                                #global temp
                                data = pickle.dumps(temp)
                                self.c.send(data)  
                                #conn.send("Directory sucessfully moved".encode(FORMAT))
                        if str(sub_dir[0]) == "4":
                            #print(sub_dir[1])
                            #print(sub_dir[2])
                            flag = rename_directory(sub_dir[1],sub_dir[2],sub_dir[3])
                            if(flag==0):
                                a = "source_path or destination_path is not exist"
                                data = pickle.dumps(a)
                                self.c.send(data)  
                                #conn.send("source_path or destination_path is not exist".encode(FORMAT))
                            elif(flag==1): 
                                #global temp
                                #global temp
                                data = pickle.dumps(temp)
                                self.c.send(data)  
                                #conn.send("Directory sucessfully moved".encode(FORMAT))



                    #3  check client name exist or not 
                    if(self.msg==201): 
                        #print("201 if part")
                        if(rdata in name):
                            self.msg=400
                            data = pickle.dumps(self.msg)
                            self.c.send(data)
                            raise("Name is already taken")
                        else: 
                            self.n=rdata 
                            name.append(self.n)
                            #print(name)
                            #print("got")
                            self.msg=200

                except Exception as e: 
                    print("entered in Exception")
                    err=1 
                    print(e)
                    if(self.n!=""): 
                        signal_disconnected=self.n+" disconnected"
                        print(self.n," disconnected")
                    clients.remove(self.id) 
                    if(self.n!=""):
                        name.remove(self.n)
                    break  


# 4 function for below operation 
# Rename Directory , Moving Directory , Delete Directory , Create Directory 

def rename_directory(client_name,a,b):
    print("entered in rename_directory")
    #current_directory = os.getcwd()
    current_directory = parent + "/" + client_name
    full_path = os.path.join(current_directory,a)
    #print(full_path)
    full_path1 = os.path.join(current_directory,b)
    #print(full_path1)
    if os.path.exists(full_path):
        try:
            os.rename(full_path,full_path1)
        except OSError:
            return 0
        #a = os.getcwd() 
        global temp
        temp = []
        for x in os.walk(current_directory):
            #global temp
            temp.append(x)  
        global m 
        m = "directory renamed in client name  :  "+str(client_name)  
        return 1
    else:
        return 0 


def moving_directory(client_name,source_dir,destination_dir):
    #current_directory = os.getcwd()
    current_directory = parent + "/" + client_name
    source_path = os.path.join(current_directory,source_dir)
    #print(source_path)
    destination_path = os.path.join(current_directory,destination_dir)
    #print(destination_path)
    final_destination = os.path.join(destination_path,source_dir)
    #print(final_destination)
    if os.path.exists(source_path) and os.path.exists(destination_path):
        try:
            os.rename(source_path,final_destination)
        except OSError:
            return 0


        #a = os.getcwd() 
        global temp
        temp = []
        for x in os.walk(current_directory):
            print(f"list {x}")
            temp.append(x)
        global m 
        m = "Directory deleted in client name :  "+str(client_name)  
        return 1
    else:
        return 0 


def delete_sub_directory(client_name,sub_dir):
    #current_directory = os.getcwd()
    current_directory = parent + "/" + client_name
    source_path = os.path.join(current_directory,sub_dir)
    print(source_path)
    if os.path.exists(source_path):
        #sub_dir = './'+str(sub_dir)
        try:
            shutil.rmtree(source_path) 
        except OSError:
            return 0
        global temp
        temp = []
        #a = os.getcwd()  
        for x in os.walk(current_directory):
            print(f"list {x}")
            temp.append(x)
        global m 
        m = "Directory deleted in client name  :  "+str(client_name)  
        return 1
    else:
        return 0

def create_sub_directory(client_name,sub_dir):  
    #current_directory = os.getcwd()
    current_directory = parent + "/" + client_name
    source_path = os.path.join(current_directory,sub_dir)
    print("create sub directory")
    print(source_path)
    #print(a)
    if os.path.exists(source_path):
        return 0 
    else:
        #sub_dir = './'+str(sub_dir)
        try:
            os.mkdir(source_path)
        except OSError:
            return 0
        # list of sub directory of client
        #a = os.getcwd()
        global temp
        temp = []
        for x in os.walk(current_directory):
            print(f"list {x}")
            temp.append(x)
        global m 
        m = "Directory created in client name  :  "+str(client_name)  
        return 1 

        
def create_directory(msg):
    print("entered in create_directory")
    msg1 = str(parent)+'/'+str(msg)
    print(msg1)
    if os.path.exists(msg1):
        os.chdir(msg1)
    else: 
        os.mkdir(msg1)
        #print(msg)
        #print(msg1)
        os.chdir(msg1)
    a = os.getcwd()
    global temp
    temp = []
    # list of sub directory of client
    for x in os.walk(a):
        #global temp
        temp.append(x)
        print(f"list {x}")
    print("temp directory")
    print(temp)

# For closing connection with button 
def close_window(): 
    root.destroy()
    os._exit(0)


# GUI for server
Font = font.Font(size=20)
Font1 = font.Font(size=40)
Label(root).pack()
Label(root).pack()

# CLOSE server button 
btn=Button(root,text="Disconnect  server",command=close_window)
btn['font']=Font
btn.pack()
root.geometry("600x600")  
Label(root).pack()
Label(root).pack()

head=Label(root,text="Currently connected client")
head['font']=Font
head.pack()
Label(root).pack()
Label(root).pack()
cstatus=Label(root)
cstatus['font']=Font
cstatus.pack()
Label(root).pack()
Label(root).pack()


status=Label(root)
status['font']=Font
status.pack()
Label(root).pack()
Label(root).pack()

# last operation performed 
p=Label(root)
p['font']=Font
p.pack()
Label(root).pack()
Label(root).pack()
# dstatus=Label(root)
# dstatus['font']=Font
# dstatus.pack()
# Label(root).pack()
# Label(root).pack() 

# This function update GUI  elements with updated value
def update(): 
    status.config(text=signal)
    global m
    p.config(text=m)
    c=""
    #print("name",name)
    if(len(name)==0):
        c="No one is connected"
    else:
        for i in name:
            c=c+i+"\n"
    cstatus.config(text=c)
    root.after(100, update)
update()  

main_t=handle_client()
main_t.start()

root.mainloop()
