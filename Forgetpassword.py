from tkinter import *
from tkinter import ttk
from tkinter import messagebox
def send():
    labelframe = LabelFrame(root, text="Mail has been sent succeccfully!!!",bd=2,fg="navy",font=("italic",45,"bold"),bg="gainsboro",highlightthickness=20)
def back():
    labelframe = LabelFrame(root, text="welcome back to login",bd=2,fg="navy",font=("italic",45,"bold"),bg="gainsboro",highlightthickness=20)
root = Tk()    
root.title("User Management System")
root.geometry('540x600')
root.configure(background="gainsboro")
labelframe = LabelFrame(root, text="Forget Password",bd=2,fg="navy",font=("italic",45,"bold"),bg="gainsboro",highlightthickness=20)
labelframe.pack(fill="both",expand="yes")
label_uname = Label(root, text="Enter Your Email:",width=20,font=("courier", 14,"bold"),fg="navy",bg="gainsboro")
label_uname.place(x=620,y=200)
entry_uname = Entry(root,width=25,bd=5,bg="white",fg="navy")
entry_uname.place(x=650,y=260)
var = IntVar(root,1)
Button(root, text='Send  Mail',width=13,font=("bold",12),bg='navy',fg='white',command=send).place(x=665,y=350)
Button(root, text='⬅   Back',width=13,font=("bold",12),bg='navy',fg='white',command=back).place(x=667,y=710)
root.mainloop()
