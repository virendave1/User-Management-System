from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
def data():
    m=entry_uname.get()
    n=entry_pass.get()
    if(m==""):
        messagebox.showinfo("login","Please fill proper credentials")
root = Tk()    
root.title("User Management System")
ima="AHMNV_free-file.png"
PIL_image = Image.open(ima)
root.geometry('500x500') 
root.geometry('540x600')
root.configure(background="gainsboro")
labelframe = LabelFrame(root, text="Login",bd=2,fg="navy",font=("italic",45,"bold"),bg="gainsboro",highlightthickness=20)
labelframe.pack(fill="both",expand="yes")
width = 200
height = 150
PIL_image_small = PIL_image.resize((width,height), Image.ANTIALIAS)      
PIL_image_small = PIL_image
PIL_image_small.thumbnail((width,height), Image.ANTIALIAS)
img = ImageTk.PhotoImage(PIL_image_small)
in_frame = Label(labelframe, image = img)
in_frame.pack()
label_uname = Label(root, text="UserName :",width=10,font=("courier", 14,"bold"),fg="navy",bg="gainsboro")
label_uname.place(x=600,y=300)
entry_uname = Entry(root,width=25,bd=5,bg="white",fg="navy")
entry_uname.place(x=750,y=300)
label_pass = Label(root, text="Password :",width=10,font=("courier", 14,"bold"),fg="navy",bg="gainsboro")
label_pass.place(x=600,y=360)
entry_pass = Entry(root,width=25,bd=5,bg="white",fg="navy")
entry_pass.place(x=750,y=360)
Button(root, text='Submit',width=13,font=("bold",12),bg='navy',fg='white',command=data).place(x=550,y=480)
Button(root, text='Forget Password',width=20,font=("bold",12),bg='navy',fg='white',command=data).place(x=800,y=480)
root.mainloop()
