# NAME : Tejas Pravinbhai Patel 
# UTA ID : 1001729131


import socket
import sys
import os
from tkinter import *  
from tkinter import font
import pickle
import threading
import re
import time
import tkinter 
from tkinter import messagebox
import shutil
import  json
#from tkinter import simpledailougebox
root = Tk()
name1 = StringVar()
name2 = StringVar()
new_name = StringVar()
new_name1 = StringVar()
HEADER = 64
PORT = 9999
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
name=StringVar()
global operation
global directory
global L_dir
data=""
operation= 0
directory = ""
L_dir = ""
token = ['A','B','C']
global list_directory
list_directory = []
global services
services = []
global selected
selected = []
global oop
oop = ""
global dd
dd = {}



class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client = None
        self.PORT = 9999
        self.FORMAT = 'utf-8'
        self.conn = 0
        self.code=0
        self.name_client=""
        self.dir_name = ""
        self.track = []
        self.list_directory = []
        self.selected = []
        self.oop = ""

    def run(self):
        while(True):
            global operation
            global directory
            global L_dir
            #print("start while")
            if(self.conn==0):
                try:
                    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client.connect(ADDR) 
                    self.conn=1
                except:
                    self.status="Server is not available"
                    self.conn=0
                    self.code=403
            else:
                try:
                    # server_dict = pickle.loads(self.client.recv(1024))
                    # print("server_dict",server_dict)
                    # print("connected wating for msg")
                    # print("starting of client")
                    msg = pickle.loads(self.client.recv(1024))
                    # print(msg)
                    # print("msg is here", msg)
                    # if re.search("#",str(msg))!=None:
                    #     msg = msg.split("#")
                    if(msg==404): 
                        self.status="server is full please try after some time"
                        self.conn=0
                        self.code=404
                    elif(msg==201):
                        print("201")
                        self.code=201
                        self.status="Not Connected" 
                        while(self.name_client==""):
                            pass
                        temp = self.name_client+"#"

                        # if(len(token)!=0):
                            #global oop
                        hw = os.getcwd()
                        hw1  = hw.split("/client")
                        hw2  = str(hw1[0]) + "/server"+"/token.pickle"
                        hw3  = str(hw1[0]) + "/server"+"/track.pickle"
                        # with open("index.pickle","rb") as handle:
                        #     index_key = pickle.load(handle) 
                        temp_dict1 = {}
                        temp_d = False
                        with open(hw3,"rb") as handle:
                            temp_dict1=pickle.load(handle)
                            print("temp_dict1",temp_dict1)
                            if self.name_client in temp_dict1:
                                self.oop = temp_dict1[self.name_client]
                                temp_d = True
                                print("client is in memory")
                        if(temp_d==False):
                            with open(hw2,"rb") as handle:
                                ooop = pickle.load(handle) 
                                print("0000p",ooop[0])
                                self.oop = ooop[0]
                                ooop.pop(0)
                            with open(hw2,"wb") as handle:
                                pickle.dump(ooop,handle)
                        # temp_dict= {}
                        with open(hw3,"wb") as handle:
                            temp_dict1[self.name_client] = self.oop
                            pickle.dump(temp_dict1,handle)

                        h = os.getcwd()
                        h1  = h.split("/client")
                        # if(len(dd[self.oop]) > 0):    
                        #     for i in dd.get(self.oop):
                        #         temp = i.split("server/")
                        #         # print("key",key)
                        #         if os.path.exists(h+"/"+self.oop+"/"+"copy_"+temp[1]):
                        #             shutil.rmtree(h+"/"+key+"/"+"copy_"+temp[1])
                        #         shutil.copytree(h1[0]+"/"+i,h+"/"+key+"/"+"copy_"+temp[1])
                        # print('self.oop', self.oop)

                        temp = temp+str(os.getcwd())+"/"+self.oop
                        # token.pop(0)
                        self.client.send(pickle.dumps(temp))
                        k = pickle.loads(self.client.recv(1024))
                        # global list_directory
                        self.list_directory = k
                        g = ""
                        for i in k:
                            g = g + i + "\n"
                        self.status="Connected"
                        messagebox.showinfo("directory",g)
                        frame = tkinter.LabelFrame (root, text = "Synchronize", padx = 5, pady = 5)
                        frame.pack ()
                        for i in range(len(k)):
                            var = tkinter.IntVar()
                            var.set(0)
                            self.track.append(var)
                        for i in range(len(self.track)):
                            checkbox = tkinter.Checkbutton(frame, text = k[i], variable= self.track[i]).pack()
                        button1 = tkinter.Button(frame, text = "Synchronize", command = self.display).pack()
                        button89 = tkinter.Button(frame, text = "Desynchronize", command = self.Desynchronize).pack()
                        # print("control reaches to end")  
                        self.conn=1
                    elif(msg==400):  
                        self.status=""
                        self.name=""
                        self.conn=0 
                        self.code=400  
                    # global directory
                    elif(msg==200):
                        # print("inside 200")
                        self.conn=1
                        self.status="Connected" 
                        self.code=200
                        # print("operation",operation)
                        # print("directory",directory)
                        global directory
                        if(operation>0 and operation<5 and directory!=" "):
                            merge = str(operation) +"@"+str(self.name_client)+"@"+ str(directory)
                            # print("merge",merge)
                            self.client.send(pickle.dumps(merge)) 
                            L_dir = pickle.loads(self.client.recv(1024))
                            # print("got the directory",L_dir)
                            # global data
                            # data = str(L_dir)
                            operation = 0 
                            # self.client.send(pickle.dumps("hh"))
                            # print("before dummy")
                            # dummy_200 = pickle.loads(self.client.recv(1024))
                            # print(dummy_200)
                            # print("dummy_200",dummy_200)
                            # self.client.send(pickle.dumps("finddict"))
                            # server_data = pickle.loads(self.client.recv(1024))
                            # print("server dictionary",server_data)
                            # self.client.send(pickle.dumps("hh"))
                            self.synchronize()
                            # print(dd)
                            # print("after synchronize")
                            # with open("you.pickle","wb") as handle:
                            #     pickle.dump(dd,handle)
                            # with open("you.pickle","rb") as handle:
                            #     h = pickle.load(handle) 
                            # print("after pickle")
                            # print("hhhhhhhhhhhh",h)
                            # print("hhh dictionary",h)
                            # pickle.dump(dd,open("you.txt","wb"))
                            
                            # print("h",h)
                            # a  = open("you.txt","r")
                            # print("aa",a.read())

                            # dummy_200 = pickle.loads(self.client.recv(1024))
                            # global dd
                            # dict_string = "rdict"+str(dd)
                            # self.client.send(pickle.dumps(dict_string))
                            # acknowledgement = pickle.loads(self.client.recv(1024))
                            # print("acknowledgement",acknowledgement)                           
                            # server_data = pickle.loads(self.client.recv(1024))
                            
                            # global dd
                            # self.client.send(pickle.dumps(dd))  
                            # server_dict = pickle.loads(self.client.recv(1024))
                            # # server_dict = json.loads(self.client.recv(1024))
                            # print('sever_dict',server_dict)


                            # if (self.oop not in server_dict):
                            #     server_dict[self.oop] = list()
                            # t1 = dd[self.oop]
                            # print("temp",t1)
                            # for i in temp:
                            #     server_dict[self.oop].append(i)
                            # print("after insertion",server_dict)
                            # dd[self.oop] = list(set(dd[self.oop]))

                            # print("Server dictionary",server_dict)
                            
                        else:
                            self.client.send(pickle.dumps(self.code))  
            
                        self.status="Connected" 


                except Exception as e:  
                    print(e) 
                    self.name_client=""
                    self.status="Server is not available"
                    self.conn=0
                    self.code=403
    def Desynchronize(self):
        hw = os.getcwd()
        hw1  = hw.split("/client")
        hw4  = str(hw1[0]) + "/server"+"/distributed.pickle"
        if os.path.getsize(hw4) > 0:
            with open(hw4,"rb") as handle:
                temp_dsync=pickle.load(handle)

        if self.oop in temp_dsync.keys():
            for i in temp_dsync[self.oop]:
                print("path",hw+"/"+self.oop+"/"+"copy_"+i)
                if os.path.exists(hw+"/"+self.oop+"/"+"copy_"+i):
                    shutil.rmtree(hw+"/"+self.oop+"/"+"copy_"+i)
            for i in temp_dsync[self.oop]:
                temp_dsync.get(self.oop).remove(i)
                with open(hw4,"wb") as handle:
                    pickle.dump(temp_dsync,handle)

    def display(self):
        # print("list directory",self.list_directory)
        for i in range(len(self.list_directory)):
            # print(self.track[i].get())
            if self.track[i].get() >= 1:
                #global selected
                if(self.list_directory[i] not in self.selected):
                    self.selected.append(self.list_directory[i])
                else:
                    if(self.list_directory[i] in self.selected):
                        self.selected.remove(self.list_directory[i])
        # print("selected...........",self.selected)
                # print (self.list_directory[i])
        # global dd
        # # print("at time of dd",dd)
        # if(self.oop in dd):        
        #     e = dd[self.oop]
        #     h = os.getcwd()
        #     h1  = h.split("/client")
        #     for i in range(0,len(e)):
        #         j = self.e[i].split("server/")
        #         try:
        #             #if path already exists, remove it before copying with copytree()
        #             if os.path.exists(h+"/"+self.oop+"/"+"copy_"+j[1]):
        #                 shutil.rmtree(h+"/"+self.oop+"/"+"copy_"+j[1])
        #             shutil.copytree(h1[0]+"/"+self.e[i],h+"/"+self.oop+"/"+"copy_"+j[1])
        #             # print("copytree part")
        #         except OSError as e:
        #             # print("errrorrrrrrrrrrrr",e)
        #             # If the error was caused because the source wasn't a directory
        #             if e.errno == errno.ENOTDIR:
        #                 pass
        #                #shutil.copy(source_dir_prompt, destination_dir_prompt)
        #             else:
        #                 print('Directory not copied. Error: %s' % e)
        self.synchronize()

    #def client_memory(self):
    def synchronize(self):
        h = os.getcwd()
        h1  = h.split("/client")
        global dd
        # print("selectedddddd",self.selected)
        for i in range(0,len(self.selected)):
            j = self.selected[i].split("server/")
            global dd
            if(self.oop not in dd):
                dd[self.oop]=list()
            dd[self.oop].append(j[1])
            dd[self.oop] = list(set(dd[self.oop]))
            # with open("you.pickle","wb") as handle:
            #     pickle.dump(dd,handle)
            # with open("you.pickle","rb") as handle:
            #     h = pickle.load(handle) 
            try:
                #if path already exists, remove it before copying with copytree()
                if os.path.exists(h+"/"+self.oop+"/"+"copy_"+j[1]):
                    shutil.rmtree(h+"/"+self.oop+"/"+"copy_"+j[1])
                shutil.copytree(h1[0]+"/"+self.selected[i],h+"/"+self.oop+"/"+"copy_"+j[1])
                # server_data = pickle.loads(self.client.recv(1024))
                # global dd
                # self.client.send(pickle.dumps(dd))  
                #print("copytree part")
            except OSError as e:
                print("errrorrrrrrrrrrrr",e)
                # If the error was caused because the source wasn't a directory
                if e.errno == errno.ENOTDIR:
                    pass
                   #shutil.copy(source_dir_prompt, destination_dir_prompt)
                else:
                    print('Directory not copied. Error: %s' % e)
        print(dd)
        hw = os.getcwd()
        hw1  = hw.split("/client")
        hw4  = str(hw1[0]) + "/server"+"/distributed.pickle"
        print(hw4)
        print("dictionary",dd)
        # print(os.path.getsize(hw4))
        if os.path.getsize(hw4) > 0:
            with open(hw4,"rb") as handle:
                track_dict=pickle.load(handle)
                print("track_dict",track_dict)
            with open(hw4,"wb") as handle:
                if self.oop in track_dict.keys():
                    print("if part")
                    track_dict[self.oop] = track_dict[self.oop] + dd[self.oop]
                else:
                    print("else part")
                    print(dd[self.oop])
                    track_dict[self.oop] = dd[self.oop]
                pickle.dump(track_dict,handle)
        else:
            with open(hw4,"wb") as handle:
                pickle.dump(dd,handle)

        if os.path.getsize(hw4) > 0:
            with open(hw4,"rb") as handle:
                track_dict11=pickle.load(handle)
                print("track_dict",track_dict11)

        for i in range(0,len(self.selected)):
            # j = self.selected[i].split("server/")
            for key in track_dict11:
                print ("dictionary for distributed thing",key)
                # print(dd)
                print(track_dict11.get(key))
                for p in track_dict11.get(key):
                    if os.path.exists(h+"/"+key+"/"+"copy_"+p):
                        shutil.rmtree(h+"/"+key+"/"+"copy_"+p)
                    shutil.copytree(h1[0]+"/"+self.selected[i],h+"/"+key+"/"+"copy_"+p)
                    print("actual path",h1[0]+"/"+self.selected[i],h+"/"+key+"/"+"copy_"+p)



    # def synchronize(self):
    #     h = os.getcwd()
    #     h1  = h.split("/client")
    #     global dd
    #     # print("selectedddddd",self.selected)
    #     for i in range(0,len(self.selected)):
    #         j = self.selected[i].split("server/")
    #         global dd
    #         if(self.oop not in dd):
    #             dd[self.oop]=list()
    #         dd[self.oop].append(j[1])
    #         dd[self.oop] = list(set(dd[self.oop]))
    #         # with open("you.pickle","wb") as handle:
    #         #     pickle.dump(dd,handle)
    #         # with open("you.pickle","rb") as handle:
    #         #     h = pickle.load(handle) 
    #         try:
    #             #if path already exists, remove it before copying with copytree()
    #             if os.path.exists(h+"/"+self.oop+"/"+"copy_"+j[1]):
    #                 shutil.rmtree(h+"/"+self.oop+"/"+"copy_"+j[1])
    #             shutil.copytree(h1[0]+"/"+self.selected[i],h+"/"+self.oop+"/"+"copy_"+j[1])
    #             # server_data = pickle.loads(self.client.recv(1024))
    #             # global dd
    #             # self.client.send(pickle.dumps(dd))  
    #             #print("copytree part")
    #         except OSError as e:
    #             print("errrorrrrrrrrrrrr",e)
    #             # If the error was caused because the source wasn't a directory
    #             if e.errno == errno.ENOTDIR:
    #                 pass
    #                #shutil.copy(source_dir_prompt, destination_dir_prompt)
    #             else:
    #                 print('Directory not copied. Error: %s' % e)
        # print(dd)
        # hw = os.getcwd()
        # hw1  = hw.split("/client")
        # hw4  = str(hw1[0]) + "/server"+"/distributed.pickle"
        # print(hw4)
        # # if os.path.getsize(hw4) > 0:
        # with open(hw4,"rb") as handle:
        #     track_dict=pickle.load(handle)
        #     print("track_dict",track_dict)
        # print("dd",dd)
        # print("before starting of the dictionary")
        # with open(hw4,"wb") as handle:
        #     if self.oop in track_dict.keys():
        #         previous_dict = track_dict[self.oop]
        #         previous_dict.append(dd)
        #     else:
        #         track_dict[self.oop] = list()
        #         for i in dd[self.oop]:
        #             track_dict[self.oop].append(i)
        #         print("track_dict",track_dict)
                # print("previous_dict",previous_dict)



                # temp_dict1[self.name_client] = self.oop
                # pickle.dump(temp_dict1,handle)
                # if self.oop in track_dict:
                #     previous_dict = track_dict[self.oop]
                #     print("previous_dict",previous_dict)
                # else:
                #     print("dd[self.oop]",dd[self.oop])
                    # print("p")

                    # pickle.loads(dd,handle)
            # with open("distributed.pickle","rb") as handle:
            #     h = pickle.load(handle) 



            # for key in track_dict.keys():
            #     for q in track_dict[key]:
            #         print("j[1]",j[1])
            #         if os.path.exists(h+"/"+key+"/"+"copy_"+q):
            #           shutil.rmtree(h+"/"+key+"/"+"copy_"+q)
            #         shutil.copytree(h1[0]+"/"+self.selected[i],h+"/"+key+"/"+"copy_"+q)
            
            # for key in dd:
            #     print ("dictionary for distributed thing",dd)
            #     if(j[1] in dd.get(key)):
            #         if os.path.exists(h+"/"+key+"/"+"copy_"+j[1]):
            #             shutil.rmtree(h+"/"+key+"/"+"copy_"+j[1])
            #         shutil.copytree(h1[0]+"/"+self.selected[i],h+"/"+key+"/"+"copy_"+j[1])

        #return dd
    # def Desynchronize(self):
    #     global dd
    #     d
        
print(dd)


t=myThread()
t.start()
def close_window(): 
    root.destroy()
    os._exit(0)
def enter_data1(): 
    pass
    # nts1=new_name1.get()
    # if(nts1!=""):
    #     t.dir_name = nts1
    # else:
    #     t.dir_name = ""
    #t.name_client = "tejas"
def enter_data():
    nts=new_name.get()
    if(re.match("^[A-Za-z0-9_-]*$",nts)):
        # print(nts)
        if(nts!=""): 
          t.name_client=nts 
        else:
          t.name_client=""
    else:
        er_display()
    nts1=new_name1.get()
    if(nts1!=""):
        t.dir_name = nts1
    else:
        t.dir_name = ""
    en.destroy()
    submit.destroy()

# 4 function call for four directory operation create , rename , reomove and delete 

def directory_operation1(): 
    global operation
    operation=1 
    directory_name = name.get()
    # print(directory_name)
    if(directory_name!=""):
        global directory
        directory = directory_name
        # print("global directory",directory)

def directory_operation2():
    global operation
    operation =2
    directory_name = name.get()
    if(directory_name!=""):
        global directory
        directory = directory_name

def directory_operation3():
    global operation
    operation =3 
    directory_name = name.get()
    if(directory_name!=""):
        global directory
        directory = directory_name

def directory_operation4():
    global operation
    operation =4 
    directory_name = name.get()
    if(directory_name!=""):
        global directory
        directory = directory_name

# def Desynchronize():
#     global dd


# GUI Starts from here

Font = font.Font(size=20)
Font1 = font.Font(size=40)
Label(root).pack()
Label(root).pack()

# CLOSE client button 
btn=Button(root,text="Disconnect  client",command=close_window)
btn['font']=Font
btn.pack()
root.geometry("600x600")  
Label(root).pack()
Label(root).pack()

# connect with given client name  

en=Entry(root,textvariable=new_name)
en['font']=Font
en.pack()
root.geometry("600x800")  
submit=Button(root,text="Click to Connect client with name given in above textbox",command=enter_data)
submit['font']=Font
submit.pack()
Label(root).pack()
# Label(root).pack()


# Connect with copying this directory 

en1=Entry(root,textvariable=new_name1)
en1['font']=Font
# en1.pack()
root.geometry("600x800")  
submit1=Button(root,text="directories need to be copied",command=enter_data)
submit1['font']=Font
# submit1.pack()
# Label(root).pack()
# Label(root).pack()

# error display 

warning=Label(root)
warning['font']=Font
warning.pack()
# Label(root).pack()
# Label(root).pack()

# illegal charachter in client name display label 

# w1=Label(root)
# w1['font']=Font
# w1.pack()
# Label(root).pack()
# Label(root).pack()

# status label 

status=Label(root)
status['font']=Font
status.pack()
Label(root).pack()
# Label(root).pack()

# Display list of direcotry 

# directory12=Text(root,height=4,width=40)
# directory12['font']=Font
# directory12.pack()
# Label(root).pack()
# Label(root).pack()

# Enter directory name on which you want to perfrom operation 
d_name=Entry(root,textvariable=name)
d_name['font']=Font
d_name.pack()
#d_name.pack()
Label(root).pack
# Label(root).pack()




# vbar=Scrollbar(root,orient=VERTICAL)
# vbar.pack(side=RIGHT,fill=Y)


demo=Label(root, text="here goes the directory name")
demo['font']=Font
demo.pack()
# btn1=Button(root,text="test",command=test)
# btn1['font']=Font
# btn1.pack() 
# Label(root).pack()
# Label(root).pack()

# btn1=Button(root,text="Desynchronize",command=Desynchronize)
# btn1['font']=Font
# btn1.pack() 
# Label(root).pack()


btn1=Button(root,text="List directory",command=directory_operation1)
btn1['font']=Font
btn1.pack() 
Label(root).pack()


btn1=Button(root,text="Create directory",command=directory_operation1)
btn1['font']=Font
btn1.pack() 
Label(root).pack()
#Label(root).pack()



btn2=Button(root,text="Delete directory",command=directory_operation2)
btn2['font']=Font
btn2.pack() 
Label(root).pack()
#Label(root).pack()

btn3=Button(root,text="Move directory",command=directory_operation3)
btn3['font']=Font
btn3.pack() 
Label(root).pack()
#Label(root).pack()

btn4=Button(root,text="Rename directory",command=directory_operation4)
btn4['font']=Font
btn4.pack() 
Label(root).pack()
#Label(root).pack()

def er_display():
    #w1.config(text="please enter valid username")
    #time.sleep(10)
    close_window()

# Update GUI elements with updated values 
def update():
    #print(t.status)  
    global data
    demo.config(text = data)
    if(t.code==400):
        warning.config(text="Name is already taken")
    elif(t.code==404):
        print("server full code") 
        warning.config(text="")
        status.config(text=t.status)
        # d_name.pack_forget()
        # en.pack_forget()
        # submit.pack_forget() 
    elif(t.code==201):
        warning.config(text="")
        status.config(text=t.status)
        
        # en.pack()
        #submit.pack()  
    elif(t.code==200):
        warning.config(text="") 
        status.config(text=t.status) 
        # d_name.pack_forget()
        # en.pack_forget()
        # submit.pack_forget()
    elif(t.code==403):
        warning.config(text="")
        status.config(text=t.status) 
        # d_name.pack_forget()
        # en.pack_forget()
        # submit.pack_forget()
    root.after(100, update) 
update()
root.mainloop()

