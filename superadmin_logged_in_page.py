from tkinter.ttk import Label,Style,Frame
import tkinter
from tkinter import *
from PIL import Image,ImageTk
root=tkinter.Tk()
root.geometry('600x600')
root.configure(background="gainsboro")
root.title("User Management System")
Style().configure(root, background="white")
PIL_image= Image.open(r"C:\Users\viren\Desktop\ums\AHMNV_free-file.png")
width = 250
height = 200
PIL_image_small = PIL_image.resize((height,width), Image.ANTIALIAS)      
PIL_image_small = PIL_image
PIL_image_small.thumbnail((width,height), Image.ANTIALIAS)
img= ImageTk.PhotoImage(PIL_image_small)
label1= Label(root, image=img)
label1.image = img
label1.place(x=0, y=0)
frame=Frame(root)
label_uname = Label(root, text="Name :",width=13,font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname.place(x=170,y=15)
label_uname = Label(root, text="AHMNV",width=50,font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname.place(x=400,y=15)
label_uname1 = Label(root, text="Email :",width=13,font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname1.place(x=170,y=65)
label_uname = Label(root, text="AHMNV99@gmail.com",width=50,font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname.place(x=400,y=65)
label_uname1 = Label(root, text="Username :",width=13,font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname1.place(x=170,y=115)
label_uname = Label(root, text="AHMNV_TEAM",width=50,font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname.place(x=400,y=115)
label_uname1 = Label(root, text="Role :",width=13,font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname1.place(x=170,y=165)
label_uname =Label(root,text="Developer",width=50,font=("courier",20,"bold"),fg="white",bg="navy")
label_uname.place(x=400,y=165)
Button(root, text='Edit Detail',width=13,bd=4,font=("bold",20),bg='white',fg='navy').place(x=1260,y=30)
Button(root, text='Logout',width=13,bd=4,font=("bold",20),bg='white',fg='navy').place(x=1260,y=120)
frame.pack()
Button(root, text='Add User',width=10,height=2,font=("bold",50),bd=10,bg='navy',fg='white').place(x=50,y=260)
Button(root, text='Delete User',width=10,height=2,font=("bold",50),bd=10,bg='navy',fg='white').place(x=560,y=260)
Button(root, text='Change Role',width=10,height=2,bd=10,font=("bold",50),bg='navy',fg='white').place(x=1070,y=260)
Button(root, text='Search by username',width=17,height=2,bd=10,font=("bold",50),bg='navy',fg='white').place(x=50,y=550)
Button(root, text='List of Users',width=17,height=2,bd=10,font=("bold",50),bg='navy',fg='white').place(x=800,y=550)
root.mainloop()


