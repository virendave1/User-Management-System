from tkinter import *
from tkinter import ttk
def print_data():
    print(entry_email.get())
    print(entry_uname.get())
    print(var.get())
root = Tk()
root.geometry('540x600')
root.configure(background="white")
labelframe = LabelFrame(root, text="Add User",bd=30,fg="black",font=("italic",35,"bold"),bg="white",highlightthickness=20)
labelframe.pack(fill="both",expand="yes")
root.title("Registration Form")
#label and entry for email
label_email = Label(root, text="Email-ID:",width=10,font=("courier", 14,"bold"),fg="black",bg="white")
label_email.place(x=120,y=170)
entry_email = Entry(root,width=25,bd=5,bg="lightblue2",fg="white")
entry_email.place(x=280,y=170)
#label and entry for username
label_uname = Label(root, text="UserName:",width=10,font=("courier", 14,"bold"),fg="black",bg="white")
label_uname.place(x=120,y=230)
entry_uname = Entry(root,width=25,bd=5,bg="lightblue2",fg="white")
entry_uname.place(x=280,y=230)
#label and radiobutton for selection through which we can directly differ user and admin 
label_role = Label(root, text="Role:",width=10,font=("courier", 14,"bold"),fg="black",bg="white")
label_role.place(x=120,y=290)
var = IntVar(root,1)
Radiobutton(root,text="Super Admin",variable=var, value=1,font=("courier", 12,"bold"),fg="black",bg="white",activeforeground="red").place(x=280,y=290)
Radiobutton(root, text="Admin", variable=var, value=2,font=("courier", 12,"bold"),fg="black",bg="white",activeforeground="red").place(x=280,y=340)
Button(root, text='Submit',width=20,font=("bold",12),bg='skyblue',fg='white',command=print_data).place(x=170,y=440)
root.mainloop()
#for that code working or not please remove it for further operation to attach

