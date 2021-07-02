# NAME : Tejas Pravinbhai Patel 
# UTA ID : 1001729131
import json
import socket
import threading
import os
import re 
import pickle
from tkinter import *  
from tkinter import font
import shutil
import tkinter
from collections import defaultdict

log_dict = defaultdict(dict)
HEADER = 64
PORT = 9999
host = socket.gethostname()
SERVER = socket.gethostbyname(host)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "e"
global temp12
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
global dict_server
dict_server = {}
empty = {}
token = ['A','B','C']
index = [0,1,2]
name1 = StringVar()
w = list()
with open("token.pickle","wb") as handle:
    pickle.dump(token,handle)
with open("track.pickle","wb") as handle:
    pickle.dump(empty,handle)
with open("log.pickle","wb") as handle:
    pickle.dump(w,handle)
with open("distributed.pickle","wb") as handle:
    pickle.dump(empty,handle)  
# m for displaying all operation on server on by one
global m
m = ""
# global log_dict
# log_dict = {}
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
        self.dic = {}
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
            global dd
            global client_id
            while (True):    
                try:
                    # self.c.send(pickle.dumps(dict_server))
                    # print("server start while")
                    if(self.msg==100): 
                        signal_disconnected=""
                        self.msg=201
                    else:
                        # print("200 is here")
                        self.msg=200
                    
                    o= pickle.dumps(self.msg)
                    self.c.send(o)
                    print("msg sent")
                    rdata = pickle.loads(self.c.recv(2048))
                    # if(re.search("finddict",str(rdata))!=None):
                    #     global dict_server
                    #     print("insied find dict",dict_server)
                    #     self.c.send(pickle.dumps(dict_server))
                    # if(re.search("rdict",str(rdata))!=None):
                    #     # global dict_server
                    #     # print("insied find dict",dict_server)
                    #     rdata = rdata[5:]
                    #     global dd
                    #     dd = eval(rdata)
                    #     print("dictionary from client",dd)
                    #     self.c.send(pickle.dumps("done"))

                    # print("waiting for msg")


                    #1 excetue for first time takes client name and create client's name directory
                    if(self.flag==False and re.search("#",str(rdata))!=None):
                        # print("entered in first time creation folder")
                        rdata = rdata.split("#")
                        msg1 = str(parent)+'/'+str(rdata[0])
                        create_directory(msg1)
                        create_directory(rdata[1])
                        list_directory = []
                        list_directories = []
                        # print (parent)
                        for root, directories, files in os.walk(parent, topdown = False):
                            for j in directories:
                                list_directory.append(os.path.join(root, j))
                        for i in list_directory:
                            temp = []
                            temp = i.split("/server/")
                            temp = temp[1].split("/")
                            temp[0] = "server/" + temp[0]
                            if (temp[0] not in list_directories):
                                list_directories.append(temp[0])

                        self.c.send(pickle.dumps(list_directories))
                        global c_name
                        c_name = rdata
                        self.flag = True 


                    if(rdata == 200):
                        self.msg = 200





                    # 2 execute when directory operation called. 
                    if(re.search("@",str(rdata))!=None and self.flag==True):
                        print("entered directory crud operation") 
                        sub_dir = rdata.split("@")
                        # print("sub directory",sub_dir) d
                        # with open("log.pickle","wb") as handle:
                        #     pickle.dump(empty,handle)
                        q = parent+"/log.pickle"
                        # print(q) d
                        # log_array = list()

                        if os.path.getsize(q) > 0:
                            with open(q,"rb") as handle:
                                dict_log=pickle.load(handle)
                        # else:
                        #     with open(q,"rb") as handle:
                        #         dict_log=pickle.load(handle)
                                # print("track_dict",track_dict)  
                        # print("dict_log",dict_log) d
                        if os.path.getsize(q) >= 0:
                            with open(q,"wb") as handle:
                                dict_log.append(sub_dir)
                                pickle.dump(dict_log,handle)

                        # with open("log.pickle","rb") as handle:
                        #     temp_list1=pickle.load(handle)
                        #     print("temp_list1",temp_dict1)
                        #     if self.name_client in temp_list1:
                        #             self.oop = temp_list1[self.name_client]
                        #             list_flag = True
                        #             print("client is in memory")
                        # if(temp_d==False):
                        #     with open(hw2,"rb") as handle:
                        #         ooop = pickle.load(handle) 
                        #         print("0000p",ooop[0])
                        #         self.oop = ooop[0]
                        #         ooop.pop(0)
                        #     with open(hw2,"wb") as handle:
                        #         pickle.dump(ooop,handle)
                        # with open("you.pickle","rb") as handle:
                        #     h = pickle.load(handle) 
                        if str(sub_dir[0]) == "1":
                            # print("enterd in one")
                            # print("sub dir [1]",sub_dir[1])
                            # print("log dict access",log_dict[sub_dir[1]])
                            # if sub_dir[1] in log_dict.keys():
                            #     log_dict[sub_dir[1]].append("create "+sub_dir[2])
                            # else:
                            #     log_dict[sub_dir[1]]=list()
                            #     log_dict[sub_dir[1]].append("create "+sub_dir[2])
                            

                            flag =  create_sub_directory(sub_dir[1],sub_dir[2])
                            # print("control in creation of sub directory") d
                            if(flag==0):
                                a = "Directory already exist"
                                data = pickle.dumps(a)
                                self.c.send(data)  

                            else:
                                # print("entered in flag 1") d
                                global temp12
                                # print("sending...", temp12) d
                                data = pickle.dumps(temp12)
                                self.c.send(data) 
                        if str(sub_dir[0]) == "2":
                            flag = delete_sub_directory(sub_dir[1],sub_dir[2])
                            # print("inside deletion part") d
                            if(flag==0):
                                a = "source_path or destination_path is not exist"
                                data = pickle.dumps(a)
                                self.c.send(data)  
                            else:
                                data = pickle.dumps(temp12)
                                self.c.send(data)  

                        if str(sub_dir[0]) == "3":
                            flag = moving_directory(sub_dir[1],sub_dir[2],sub_dir[3])
                            # print("inside moving part")   d                          
                            if(flag==0):
                                a = "source_path or destination_path is not exist"
                                data = pickle.dumps(a)
                                self.c.send(data)
                            elif(flag==1): 
                                #global temp12
                                data = pickle.dumps(temp12)
                                self.c.send(data)
                        if str(sub_dir[0]) == "4":
                            # print("inside rename part")  d
                            flag = rename_directory(sub_dir[1],sub_dir[2],sub_dir[3])
                            if(flag==0):
                                a = "source_path or destination_path is not exist"
                                data = pickle.dumps(a)
                                self.c.send(data)
                            elif(flag==1):
                                self.c.send(pickle.dumps(temp12))
                        print("end o")
                        # global dict_server
                        # self.c.send(pickle.dumps(dict_server))
                    # frame = tkinter.LabelFrame (root, text = "Undo", padx = 5, pady = 5)
                    # frame.pack ()
                    # for i in range(len(k)):
                    #     var = tkinter.IntVar()
                    #     var.set(0)
                    #     log_track.append(var)
                    # with open("log.pickle","rb") as handle:
                    #     log_list=pickle.load(handle)
                    # for i in range(len(log_list)):
                    #         checkbox = tkinter.Checkbutton(frame, text = log_list[i], variable=log_track[i]).pack()

                    
                    #3  check client name exist or not 
                    if(self.msg==201):
                        # print("201 if part")
                        if(rdata[0] in name):
                            #print("rdataaa",)
                            self.msg=400
                            data = pickle.dumps(self.msg)
                            self.c.send(data)
                            raise("Name is already taken")
                        else: 
                            self.n=rdata[0] 
                            name.append(self.n)
                            #print(name)
                            self.msg=200


                except Exception as e: 
                    # print("entered in Exception") d
                    err=1 
                    print(e) 
                    if(self.n!=""): 
                        signal_disconnected=self.n+" disconnected"
                        # print(self.n," disconnected") d
                    clients.remove(self.id) 
                    if(self.n!=""):
                        name.remove(self.n)
                    break


# 4 function for below operation 
# Rename Directory , Moving Directory , Delete Directory , Create Directory 

def rename_directory(client_name,a,b):
    # print("entered in rename_directory") d
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
        global temp12
        temp12 = []
        for x in os.walk(current_directory):
            #global temp
            temp12.append(x)  
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
        global temp12
        temp12 = []
        for x in os.walk(current_directory):
            print(f"list {x}")
            temp12.append(x)
        global m 
        m = "Directory deleted in client name :  "+str(client_name)  
        return 1
    else:
        return 0 


def delete_sub_directory(client_name,sub_dir):
    #current_directory = os.getcwd()
    current_directory = parent + "/" + client_name
    source_path = os.path.join(current_directory,sub_dir)
    # print(source_path)
    if os.path.exists(source_path):
        #sub_dir = './'+str(sub_dir)
        try:
            shutil.rmtree(source_path) 
        except OSError:
            return 0
        global temp12
        temp12 = []
        #a = os.getcwd()  
        for x in os.walk(current_directory):
            # print(f"list {x}") d
            temp12.append(x)
        global m 
        m = "Directory deleted in client name  :  "+str(client_name)  
        return 1
    else:
        return 0

def create_sub_directory(client_name,sub_dir):  
    #current_directory = os.getcwd()
    current_directory = parent + "/" + client_name
    source_path = os.path.join(current_directory,sub_dir)
    #print("create sub directory")
    #print(source_path)
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
        global temp12
        temp12 = []
        for x in os.walk(current_directory):
            # print(f"list {x}") d
            temp12.append(x)
        global m 
        m = "Directory created in client name  :  "+str(client_name)  
        return 1 

        
def create_directory(msg1):
    #print("entered in create_directory")
    #msg1 = str(parent)+'/'+str(msg)
    #print(msg1)
    if os.path.exists(msg1):
        os.chdir(msg1)
    else: 
        os.mkdir(msg1)
        #print(msg)
        #print(msg1)
        os.chdir(msg1)
    a = os.getcwd()
    global temp12
    temp12 = []
    # list of sub directory of client
    for x in os.walk(a):
        #global temp
        temp12.append(x)
    #    print(f"list {x}")
   # print("temp directory")
   # print(temp)

# For closing connection with button 
def close_window(): 
    root.destroy()
    os._exit(0)

def log():
    n=int(name1.get())
    q = parent+"/log.pickle"
    if os.path.getsize(q) > 0:
        with open(q,"rb") as handle:
            dict_log=pickle.load(handle)
    list_directory1 = []
    print("parent path")
    print(parent+"/"+dict_log[n][1])
    for root1, directories, files in os.walk(parent+"/"+dict_log[n][1]+"/"+dict_log[n][2], topdown = False):
        for j in directories:
            list_directory1.append(j)
    print(list_directory1)
    if str(dict_log[n][0]) == "1":
        # print("enterd in undo created")
        delete_sub_directory(dict_log[n][1],dict_log[n][2])
        # print(dict_log[n][1],dict_log[n][2])
        with open(q,"wb") as handle:
            dict_log.pop(n)
            for i in  range(0,len(list_directory1)):
                for j in range(0,len(dict_log)):
                    o1 = dict_log[j][2].split("/")

                    if dict_log[j][2]==list_directory1[i]:
                        dict_log.pop(j)
                    elif o1[-1]==list_directory1[i]:
                        dict_log.pop(j)

            # print("dict_log",dict_log)
            pickle.dump(dict_log,handle)
        # for root1, directories, files in os.walk(parent+dict_log[n][2], topdown = False):
        #     for j in directories:
        #         list_directory1.append(os.path.join(root1, j))
        # print(list_directory1)

    elif str(dict_log[n][0]) == "2":
        # print("enterd in undo deleted")
        create_sub_directory(dict_log[n][1],dict_log[n][2])
        for j in range(0,len(dict_log)):
            o1 = dict_log[j][2].split("/")
            if o1[0]==dict_log[n][2]:
                create_sub_directory(dict_log[n][1],dict_log[j][2])
        with open(q,"wb") as handle:
            dict_log.pop(n)
            for i in  range(0,len(list_directory1)):
                for j in range(0,len(dict_log)):
                    o1 = dict_log[j][2].split("/")

                    if dict_log[j][2]==list_directory1[i]:
                        dict_log.pop(j)
                    elif o1[-1]==list_directory1[i]:
                        dict_log.pop(j)

            print("dict_log",dict_log)
            pickle.dump(dict_log,handle)

    elif str(dict_log[n][0]) == "3":
        print("path")
        print(dict_log[n][2],dict_log[n][1])
        moving_directory(dict_log[n][1],dict_log[n][3],dict_log[n][2])
        with open(q,"wb") as handle:
            dict_log.pop(n)
            # for i in  range(0,len(list_directory1)):
            #     for j in range(0,len(dict_log)):
            #         o1 = dict_log[j][2].split("/")

            #         if dict_log[j][2]==list_directory1[i]:
            #             dict_log.pop(j)
            #         elif o1[-1]==list_directory1[i]:
            #             dict_log.pop(j)
            # print("dict_log",dict_log)
            pickle.dump(dict_log,handle) 

    elif str(dict_log[n][0]) == "4":
        # print("path")
        # print(dict_log[n][2],dict_log[n][1])
        rename_directory(dict_log[n][1],dict_log[n][3],dict_log[n][2])
        with open(q,"wb") as handle:
            dict_log.pop(n)
            # for i in  range(0,len(list_directory1)):
            #     for j in range(0,len(dict_log)):
            #         o1 = dict_log[j][2].split("/")

            #         if dict_log[j][2]==list_directory1[i]:
            #             dict_log.pop(j)
            #         elif o1[-1]==list_directory1[i]:
            #             dict_log.pop(j)
            # print("dict_log",dict_log)
            pickle.dump(dict_log,handle)        

    print("exited log")

    # if str(dict_log[n][0]) == "3":

    # if str(dict_log[n][0]) == "4":




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


d_name=Entry(root,textvariable=name1)
d_name['font']=Font
d_name.pack()


btn=Button(root,text="UNDO",command=log)
btn['font']=Font
btn.pack()

v=Label(root)
v['font']=Font
v.pack()
Label(root).pack()
Label(root).pack()
# root.geometr
# dstatus=Label(root)
# dstatus['font']=Font
# dstatus.pack()
# Label(root).pack()
# Label(root).pack() 

# This function update GUI  elements with updated value
def update(): 
    status.config(text=signal)
    global m,p,lo
    # print("upodate")
    
    c=""
    q = parent+"/log.pickle"
    if os.path.getsize(q) > 0:
        with open(q,"rb") as handle:
            dict_log=pickle.load(handle)
            # print("update",dict_log) 
            x = ""
            for i in dict_log:
                x = x + "\n" + str(i)
            p.config(text=x)
    global m 
    v.config(text=m)

    # print("update part")
    # print("updated name ba",name)
    #print("name",name)
    if(len(name)==0):
        c="No one is connected"
    else:
        #print(name)
        for i in name:
            c=c+i+"\n"
    cstatus.config(text=c)
    root.after(100, update)
update()  

main_t=handle_client()
main_t.start()

root.mainloop()
