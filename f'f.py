import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter import Label,Frame
mydb=mysql.connector.connect(host='localhost',user='root',password='',database='login')
mycur=mydb.cursor()
def dd():
    m=e1.get()
    n=e2.get()
    if(m!="" and n!=""):
        la=tk.Label(fff,font=("bold",),bd=2,fg="navy",text="User data stored successfully!!!",bg="white")
        la.place(x=730,y=500)
        k=[m,n]
        query=("insert into login(username,password) values(%s,%s)")
        mycur.execute(query,k)
        mydb.commit()
        lb.insert(END,k)
        

fff=tk.Tk()
fff.geometry("600x600")
fff.configure(bg="grey")
i="ff.png"
f=Frame(fff,bg="navy",bd=2,height=159,width=129)
ig=Image.open(i)
picture = ImageTk.PhotoImage(ig)
l1=Label(f,image=picture)
l1.place(x=0,y=0)
lab=tk.Label(fff,font=("bold",55),bd=2,fg="white",text="VCOMPANY",bg="navy")
lab.place(x=450,y=20)
f.pack(fill="both")
lf =tk.LabelFrame(fff, text="Login",bd=2,fg="navy",font=("italic",45,"bold"),bg="gainsboro",highlightthickness=20)
l2=tk.Label(fff,font=("bold",16),bd=2,fg="navy",text="Name",bg="grey")
l2.place(x=650,y=270)
lb=Listbox(lf,height=27,font=("bold",12),bd=4,width=50)
lb.pack(side="left",padx=10,fill="y")
scrollbar=Scrollbar(lf,orient="vertical")
scrollbar.config(command=lb.yview)
scrollbar.pack(side="left", fill="y")
lb.config(yscrollcommand=scrollbar.set)
e1=tk.Entry(fff,font=("bold",16),bd=2,fg="navy",bg="light blue2")
e1.place(x=770,y=270)
l3=tk.Label(fff,font=("bold",16),bd=2,fg="navy",text="password",bg="grey")
l3.place(x=650,y=330)
e2=tk.Entry(fff,font=("bold",16),bd=2,fg="navy",bg="light blue2")
e2.place(x=770,y=330)
b=tk.Button(fff,font=("bold",16),bd=12,fg="navy",text="Submit",bg="white",width=10,command=dd)
b.place(x=760,y=400)
lf.pack(expand="yes",fill="both")
fff.mainloop()
