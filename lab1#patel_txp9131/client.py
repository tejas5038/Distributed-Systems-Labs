import socket
import sys
import os
from tkinter import *  
from tkinter import font
import pickle
import threading
import re
import time

root = Tk()
name1 = StringVar()
new_name = StringVar()
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



class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client = None
        self.PORT = 9999
        self.FORMAT = 'utf-8'
        self.conn = 0
        self.code=0
        self.name_client=""
    def run(self):
        while(True):
            global operation
            global directory
            global L_dir
            if(self.conn==0):
                try:
                    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client.connect(ADDR) 
                    self.conn=1
                except:
                    # print("can not reach server")
                    self.status="Server is not available"
                    self.conn=0
                    self.code=403
            else:
                try:  
                    #msg=pickle.loads(self.s.recv(1024))  
                    msg = pickle.loads(self.client.recv(1024))  
                    #print("message",msg)
                    if(msg==404): 
                        self.status="server is full please try after some time"
                        self.conn=0
                        self.code=404
                    elif(msg==201):
                        self.code=201
                        self.status="Connected" 
                        while(self.name_client==""):
                            pass
                        self.client.send(pickle.dumps(self.name_client))
                        self.conn=1
                    elif(msg==400):  
                        self.status=""
                        self.name=""
                        self.conn=0 
                        self.code=400  
                    elif(msg==200):
                        # print("inside 200")
                        self.conn=1
                        self.status="Connected" 
                        self.code=200
                        if(operation>0 and operation<5 and directory!=" "):
                            print("client name")
                            print(self.name_client)
                            merge = str(operation) +"#"+str(self.name_client)+"#"+ str(directory)
                            print(merge)
                            # print("merge",merge)
                            self.client.send(pickle.dumps(merge)) 
                            L_dir = pickle.loads(self.client.recv(1024))
                            print("got the directory",L_dir)
                            global data
                            data = str(L_dir)
                            operation = 0 
                            #directory.config(text=L_dir)  
                        else:
                            # print(operation)
                            # print("sending again 200")
                            self.client.send(pickle.dumps(self.code))  
                        # print("skipping something")
                        #global operation 
                        #operation = 0 
                        #global directory
                        #directory = " "                     
                        self.status="Connected" 
                        #self.code=200
                        #self.conn = 1


                except Exception as e:  
                    print(e) 
                    self.name_client=""
                    self.status="Server is not available"
                    self.conn=0
                    self.code=403


t=myThread()
t.start()
def close_window(): 
    root.destroy()
    os._exit(0)
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

# 4 function call for four directory operation create , rename , reomove and delete 

def directory_operation1(): 
    global operation
    operation=1 
    directory_name = name.get()
    print(directory_name)
    if(directory_name!=""):
        global directory
        directory = directory_name


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
Label(root).pack()

# error display 

warning=Label(root)
warning['font']=Font
warning.pack()
Label(root).pack()
Label(root).pack()

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
Label(root).pack()

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
Label(root).pack()

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

btn1=Button(root,text="Create directory",command=directory_operation1)
btn1['font']=Font
btn1.pack() 
Label(root).pack()
Label(root).pack()



btn2=Button(root,text="Delete directory",command=directory_operation2)
btn2['font']=Font
btn2.pack() 
Label(root).pack()
Label(root).pack()

btn3=Button(root,text="Move directory",command=directory_operation3)
btn3['font']=Font
btn3.pack() 
Label(root).pack()
Label(root).pack()

btn4=Button(root,text="Rename directory",command=directory_operation4)
btn4['font']=Font
btn4.pack() 
Label(root).pack()
Label(root).pack()

def er_display():
    #w1.config(text="please enter valid username")
    #time.sleep(10)
    close_window()

# Update GUI elements with updated values 
def update():
    #print(t.status)  
    global data
    #print("update:",data
    #w = str(data.replace(" ","\n"))
    #vbar.config(text=data)
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
        submit.pack()  
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

