from tkinter.ttk import Label,Style,Frame
import tkinter
from tkinter import *
from PIL import Image,ImageTk
root=tkinter.Tk()
root.geometry('1800x2000')
root.configure(background="gainsboro")
root.title("User Management System")
Style().configure(root, background="white")
frame=Frame(root,bg="navy",height=200,width=40)
frame.pack(fill="both")
ima="AHMNV_free-file.png"
PIL_image= Image.open(ima)
width = 200
height = 200
PIL_image_small = PIL_image.resize((height,width), Image.ANTIALIAS)      
PIL_image_small = PIL_image
PIL_image_small.thumbnail((width,height), Image.ANTIALIAS)
img= ImageTk.PhotoImage(PIL_image_small)
label1= Label(frame, image=img)
label1.image = img
label1.place(x=0, y=0)
label_user = Label(frame, text="Current User:",font=("courier", 25,"bold"),fg="navy",bg="white")
label_user.place(x=165,y=10)
label_uname = Label(frame, text="Name:AHMNV",font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname.place(x=170,y=60)
label_uname1 = Label(frame, text="Email:AHMNV99@gmail.com",font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname1.place(x=170,y=95)
label_uname1 = Label(frame, text="Username:AHMNV_TEAM",font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname1.place(x=170,y=125)
label_uname1 = Label(frame, text="Role:Developer",font=("courier", 20,"bold"),fg="white",bg="navy")
label_uname1.place(x=170,y=155)
Button(frame, text='Edit Detail',width=20,bd=4,font=("courier", 20,"bold"),bg='white',fg='navy',relief=RAISED).place(x=1150,y=30)
Button(frame, text='Logout',width=20,bd=4,font=("courier", 20,"bold"),bg='white',fg='navy',relief=RAISED).place(x=1150,y=120)
frame.pack()
labelframe = LabelFrame(root, text="Add User",bd=2,fg="navy",font=("italic",45,"bold"),bg="gainsboro",highlightthickness=15)
labelframe.pack(fill="both",expand="yes")
label_user = Label(labelframe,text="Name:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
label_user.place(x=50,y=50)
entry_user = Entry(labelframe,width=25,bd=5,bg="white",fg="navy")
entry_user.place(x=230,y=50)
label_uname = Label(labelframe, text="Username:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
label_uname.place(x=45,y=120)
entry_uname = Entry(labelframe,width=25,bd=5,bg="white",fg="navy")
entry_uname.place(x=230,y=123)
label_email = Label(labelframe, text="Email:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
label_email.place(x=45,y=190)
entry_email = Entry(labelframe,width=25,bd=5,bg="white",fg="navy")
entry_email.place(x=230,y=198)
label_role = Label(labelframe, text="Role:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
label_role.place(x=45,y=250)
var = IntVar(root,1)
Radiobutton(labelframe,text="Admin",variable=var, value=1,font=("courier", 15,"bold"),fg="black",bg="grey",activeforeground="red").place(x=230,y=260)
Button(labelframe, text='Add',width=20,font=("bold",12),bg='navy',fg='white',bd=5).place(x=90,y=350)
Button(labelframe, text='⬅   Back',width=13,font=("bold",12),bg='white',fg='navy',bd=5).place(x=1340,y=450)
root.mainloop()

