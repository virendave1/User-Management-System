########################################################Import Statements########################################################### 


import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Style
from PIL import Image, ImageTk
import pymysql
import hashlib
import smtplib
import random
import re


########################################################Global Variables############################################################


#for tracking which user has logged in...
current_name = ""
current_email = ""
current_username = ""
current_role = ""
otp_display = 0
req_otp = ""
req_email = ""


########################################################All Pages And Functions#####################################################


class umsApp(tk.Tk) :
    '''This class is Base Class of our App.This class inherits tk.Tk class
        and all other class are going to use it for accessing functions...
        This Class can be thought of as a controller...'''

    def __init__(self, *args, **kwargs) :
        '''For creating controller...'''
        
        tk.Tk.__init__(self, *args, **kwargs)
        photo = PhotoImage(file = "icon_ahmnv.png")      #for corner icon
        self.iconphoto(False, photo)
        tk.Tk.wm_title(self, "User Management System")          #for title heading i.e. "User Management System"     
        self.container = tk.Frame(self)                         #container for all frames
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0 , weight=1)
        self.container.grid_columnconfigure(0 , weight=1)
        self.state('zoomed')                                    #for full screen while opening startpage...
        self.load_function()                                    #for loading all the page frames at the atart of the application...
        self.show_frame(LoginPage)                              #This code shows first frame i.e. "LoginPage"

    def load_function(self) :
        '''This function loads all pages or frames of the GUI application...'''
    
        self.frames = {}                                        #This dictionary contains all frames i.e. all different pages
        T = (LoginPage, ForgotPasswordPage, HomePage, AddUserPage, \
             DeleteUserPage, ChangeRolePage, SearchByUsernamePage, \
             ListOfUsersPage, EditDetailsPage, EditNamePage, EditUsernamePage, \
             EditEmailPage, EditPasswordPage)
        #Tuple to store all different pages classes
        for F in T :                                            #loop to assign all frames with its associated page to dictionary
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, current_page) :                        #Function to show different frames by .tkraise() built-in function
        '''For raising the frame up to the top...'''

        if(current_page == SearchByUsernamePage or current_page == ListOfUsersPage) :
            self.load_function()
        frame = self.frames[current_page]
        frame.tkraise()

    def header(self, current_page, heading) :
        '''For creating header in every logged in section...'''

        global current_name
        global current_email
        global current_username
        global current_role
        current_page.configure(background="gainsboro")
        Style().configure(current_page, background="white")
        frame=Frame(current_page,bg="navy",height=200,width=40)
        frame.pack(fill="both")
        image_path = "icon_ahmnv.png"
        PIL_image= Image.open(image_path)
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
        label_uname0 = Label(frame, text="Name:"+current_name,font=("courier", 20,"bold"),fg="white",bg="navy")
        label_uname0.place(x=170,y=60)
        label_uname1 = Label(frame, text="Email:"+current_email,font=("courier", 20,"bold"),fg="white",bg="navy")
        label_uname1.place(x=170,y=95)
        label_uname2 = Label(frame, text="Username:"+current_username,font=("courier", 20,"bold"),fg="white",bg="navy")
        label_uname2.place(x=170,y=125)
        label_uname3 = Label(frame, text="Role:"+current_role,font=("courier", 20,"bold"),fg="white",bg="navy")
        label_uname3.place(x=170,y=155)
        Button(frame, text='Edit Detail',width=20,bd=4,font=("bold",20),bg='white',fg='navy',relief=RAISED,
               command=lambda: self.show_frame(EditDetailsPage)).place(x=1150,y=30)
        Button(frame, text='Logout',width=20,bd=4,font=("bold",20),bg='white',fg='navy',relief=RAISED,
               command=lambda: self.logoutFunction()).place(x=1150,y=120)
        frame.pack()
        labelframe = LabelFrame(current_page, text=heading,bd=2,fg="navy",font=("italic",45,"bold"),bg="gainsboro",
                                highlightthickness=15)
        labelframe.pack(fill="both",expand="yes")
        return labelframe

    def footer(self,labelframe) :
        '''For creating footer of go back home button...'''

        Button(labelframe, text='⬅  Back To Home',width=20,font=("bold",15),bg='white',fg='navy',bd=5,
               command=lambda : self.show_frame(HomePage)).place(x=1230,y=430)

    def logoutFunction(self) :
        '''for setting current session data as empty string literal for tracking of logged in user....'''
        
        global current_name
        global current_email
        global current_username
        global current_role
        current_name = ""
        current_email = ""
        current_username = ""
        current_role = ""
        self.load_function()
        self.show_frame(LoginPage)

    def passwordGenerationFunction(self,email) :
        '''This function generates 10 characters systen generated random password...'''
        
        charset = [chr(x) for x in range(65,91)] + [chr(x) for x in range(97,123)] + [str(x) for x in range(10)] + \
        ['@','#','$','@','#','$','@','#','$']
        password = ''.join(random.choice(charset) for i in range(10))
        self.sendEmailFunction(email,password,"password")
        return password

    def otpGenerationFunction(self,email) :
        '''This function generates 6 digit otp used for changing registered email address...'''

        charset = [str(x) for x in range(10)]
        otp = ''.join(random.choice(charset) for i in range(6))
        self.sendEmailFunction(email,otp,"otp")
        return otp

    def sendEmailFunction(self,email_id,content,flag):
        '''This function sends mails to user(only regustered email address)
            with a auto generated password or otp according to flag...'''
        
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        sender = 'ahmnv.ums.pu@gmail.com'
        sender_password = 'ahmnv.ums.pu@gmail.com'
        receiver = email_id
        s.login(sender, sender_password)
        if(flag == "password") :
            s.sendmail(sender,receiver,'Subject : Password for logging in... \n\n Your requested Password is : ' + content + \
                       '\n\n\n If it was not you please ignore. \n\n\n This is a system generated email.Please do not reply back!')
        if(flag == "otp") :
            s.sendmail(sender,receiver,'Subject : Password for logging in... \n\n Your requested One Time Password is : ' + content + \
                       '\n\n\n If it was not you please ignore. \n\n\n This is a system generated email.Please do not reply back!')
        s.quit()

    def validationName(self,name,current_page) :
        '''This function validates name of user'''

        error = ""
        if(len(name) > 40) :
            current_page.name.set("")
            error += "name should be less than 40 characters..."
        charset = [chr(x) for x in range(65,91)] + [chr(x) for x in range(97,123)] + [' ']
        for i in name :
            if i not in charset :
                current_page.name.set("")
                error += "\n\nname is invalid!It consists of only alphabets and space..."
                break
        return error

    def validationUsername(self,username,current_page) :
        '''This function validates username of user'''

        error = ""
        if(len(username) > 25) :
            current_page.username.set("")
            error += "\n\nusername should be less than 25 characters..."
        charset = [chr(x) for x in range(65,91)] + [chr(x) for x in range(97,123)] + [str(x) for x in range(0,10)]
        for i in username :
            if i not in charset :
                current_page.username.set("")
                error += "\n\nusername is invalid!!!It consists of only alphabets and numbers..."
                break
        connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
        cursor = connection.cursor()
        connection.autocommit(True)
        query = f"SELECT * FROM `user_table` WHERE `username` = '{username}';"
        cursor.execute(query)
        username_query = cursor.fetchone()
        if(username_query != None):
            current_page.username.set("")
            error = "\n\nOops...Sorry, this username is alreday taken!!!"    
        connection.close()
        return error

    def validationEmail(self,email,current_page) :
        '''This Function validates email of the user'''

        error = ""
        if(len(email) > 40) :
            current_page.email.set("")
            error += "\n\nemail should be less than 40 characters..."
        if((re.match(r'\b[A-Z0-9._]+@[A-Z.]+\.[A-Z]{2,}\b', email, re.I) == None) or \
           (email != re.match(r'\b[A-Z0-9._]+@[A-Z.]+\.[A-Z]{2,}\b', email, re.I).group())) :
            current_page.email.set("")
            error += "\n\nemail address is invalid!!!Enter a valid email id like something@example.com..."
        connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
        cursor = connection.cursor()
        connection.autocommit(True)
        query = f"SELECT * FROM `user_table` WHERE `email` = '{email}';"
        cursor.execute(query)
        email_query = cursor.fetchone()
        if(email_query != None):
            current_page.email.set("")
            error = "\n\nThis Email Address is already Registered!!!"
        connection.close()
        return error


'''All the classes which are for different pages are going to inherit tk.Frame class...'''


class LoginPage(tk.Frame) :
    '''This is a Login Page where user can login with unique username and password...'''

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        self.configure(background="gainsboro")                  #BACKGROUND-COLOR
        labelframe = LabelFrame(self, text="Login",bd=2,fg="navy",font=("italic",45,"bold"),bg="gainsboro",highlightthickness=20)
        labelframe.pack(fill="both",expand="yes")               #for rectangle border
        image_path = "icon_ahmnv.png"
        self.PIL_image = Image.open(image_path)
        width = 200
        height = 150
        self.PIL_image_small = self.PIL_image.resize((width,height), Image.ANTIALIAS)      
        self.PIL_image_small = self.PIL_image
        self.PIL_image_small.thumbnail((width,height), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.PIL_image_small)
        self.in_frame = Label(labelframe, image = self.img)     #for image on top of labels and entry boxes
        self.in_frame.pack()
        label_uname = Label(self, text="Username :", width=10, font=("courier", 14, "bold"), fg="navy", bg="gainsboro")
        label_uname.place(x=600,y=300)
        self.username = StringVar(self , value="")
        entry_uname = Entry(self, textvariable=self.username, width=25, bd=5, bg="white", fg="navy")     #labels and entry boxes
        entry_uname.place(x=750,y=300)
        label_pass = Label(self, text="Password :", width=10, font=("courier", 14, "bold"), fg="navy", bg="gainsboro")
        label_pass.place(x=600,y=360)
        self.password = StringVar(self , value="")
        entry_pass = Entry(self, textvariable=self.password, width=25, bd=5, bg="white", fg="navy", show='*')
        entry_pass.place(x=750,y=360)
        submitButton = tk.Button(self, text='Submit', width=13, font=("bold", 12), bg='navy', fg='white',
                                 command=lambda: self.loginFunction(self.username.get(),self.password.get(),controller))
        submitButton.place(x=580,y=440)                         #both the buttons
        forgotPasswordButton = tk.Button(self, text='Forgot Password?', width=15, font=("bold",12), bg='white', fg='navy',
                                         command=lambda : self.forgotPasswordFunction(controller))
        forgotPasswordButton.place(x=800,y=440)

    def loginFunction(self,username,password,controller):
        '''for authorising user who is trying to log in and creating a session of user
        by setting a global variables...'''

        if(username=="" or password==""):
            messagebox.showwarning("Warning","Please fill the proper credentials!!!")
        else :
            try :
                connection = ""
                connection = pymysql.connect(host="localhost", user="root", passwd="", database="ums_database")
                cursor = connection.cursor()
                connection.autocommit(True)
                query=f"SELECT * FROM `user_table` where `user_table`.`username` = '{username}';"
                cursor.execute(query)
                current_data=cursor.fetchone()
                if(current_data == None) :
                    self.username.set("")
                    self.password.set("")
                    messagebox.showwarning("Warning","Invalid Username!!!")
                else :
                    hashed_password = hashlib.md5(password.encode()).hexdigest()
                    if(hashed_password == current_data[3]) :
                        self.username.set("")
                        self.password.set("")
                        #for setting current logged in user
                        global current_name
                        global current_email
                        global current_username
                        global current_role
                        current_name = current_data[0]
                        current_email = current_data[1]
                        current_username = current_data[2]
                        current_role = current_data[4]
                        controller.load_function()
                        controller.show_frame(HomePage)
                        messagebox.showinfo("Success",f" welcome {current_data[0]}... \n You are logged in as {current_data[4]}!")
                    else :
                        self.password.set("")
                        messagebox.showwarning("Warning","Wrong Password!!!")
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()

    def forgotPasswordFunction(self , controller) :
        '''for going to forgot password page...'''

        self.username.set("")
        self.password.set("")
        controller.show_frame(ForgotPasswordPage)


class ForgotPasswordPage(tk.Frame) :
    '''This is Forgot Password Page where by entering a registered email address
        new system generated password is sent to user via mail...'''

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        self.configure(background="gainsboro")
        labelframe = LabelFrame(self, text="Forgot Password?", bd=2, fg="navy", font=("italic",45,"bold"), bg="gainsboro",
                                highlightthickness=20)
        labelframe.pack(fill="both", expand="yes")              #for a rectangle border
        label_email = Label(self, text="Enter Your Regsitered Email id", width=30, font=("courier", 14,"bold"), fg="navy",
                            bg="gainsboro")
        label_email.place(x=585,y=200)                          #email, entry and send button boxes
        self.email = StringVar(self , value="")
        entry_email = Entry(self, textvariable=self.email, width=60, bd=5, bg="white", fg="navy")
        entry_email.place(x=570,y=260)
        sendButton = Button(self, text='Send Password Verification Mail', width=30, font=("bold",12), bg='navy', fg='white',
                            command = lambda : self.forgotPasswordVerificationMail(self.email.get(),controller))
        sendButton.place(x=620,y=350)
        backButton = Button(self, text='⬅   Back To Login Page', width=25, font=("bold",12), bg='white', fg='navy',
                            command = lambda : controller.show_frame(LoginPage))
        backButton.place(x=640,y=710)                           #back button

    def forgotPasswordVerificationMail(self,email,controller) :
        '''For sending a password to user with verifying user through email id when he forgots password'''

        if(email=="") :
            messagebox.showwarning("Warning","Please fill the Email id!!!")
        else :
            connection = ""
            try :
                connection = pymysql.connect(host="localhost", user="root", passwd="", database="ums_database")
                cursor = connection.cursor()
                connection.autocommit(True)
                self.email.set("")
                query=f"SELECT * FROM `user_table` WHERE email = '{email}';"
                cursor.execute(query)
                current_data=cursor.fetchone()
                if(current_data == None):
                    messagebox.showwarning("Warning","This Email is not Registered!!!")
                else:
                    try :
                        password = controller.passwordGenerationFunction(email)
                    except :
                        messagebox.showerror("Error","Password Cannot be sent right now!!!\nTry again later...")
                        return 0                                #for terminating function after exception...
                    hashed_password = hashlib.md5(password.encode()).hexdigest()
                    query = f"UPDATE `user_table` SET `password`='{hashed_password}' WHERE email = '{email}';"
                    cursor.execute(query)
                    messagebox.showinfo("Success","Password has been sent to entered email address")
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()
            

class HomePage(tk.Frame) :
    '''This is logged in super admin menu page...
        where users are shown with different functionality
        sccording to their role...'''

    global current_role

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        controller.header(self,"Home")
        self.homeFunction(controller)

    def homeFunction(self,controller) :
        '''For checking current role to display the way of logged in page...'''

        #home page for super admin user
        if(current_role == "SuperAdmin") :
            Button(self, text='Add User',width=10,height=1,font=("bold",50),bd=10,bg='navy',fg='white',relief=RAISED,
                   command=lambda : controller.show_frame(AddUserPage)).place(x=50,y=315)
            Button(self, text='Delete User',width=10,height=1,font=("bold",50),bd=10,bg='navy',fg='white',relief=RAISED,
                   command=lambda : controller.show_frame(DeleteUserPage)).place(x=560,y=315)
            Button(self, text='Change Role',width=10,height=1,bd=10,font=("bold",50),bg='navy',fg='white',relief=RAISED,
                   command=lambda : controller.show_frame(ChangeRolePage)).place(x=1070,y=315)
            Button(self, text='Search by Username',width=17,height=1,bd=10,font=("bold",50),bg='navy',fg='white',
                   relief=RAISED, command=lambda : controller.show_frame(SearchByUsernamePage)).place(x=50,y=550)
            Button(self, text='List of Users',width=17,height=1,bd=10,font=("bold",50),bg='navy',fg='white',relief=RAISED,
                   command=lambda : controller.show_frame(ListOfUsersPage)).place(x=800,y=550)
        #home page for admin user
        if(current_role == "Admin") :
            Button(self, text='Add User',width=36,height=1,font=("bold",50),bd=10,bg='navy',fg='white',relief=RAISED,
                   command=lambda : controller.show_frame(AddUserPage)).place(x=50,y=315)
            Button(self, text='Search by Username',width=17,height=1,bd=10,font=("bold",50),bg='navy',fg='white',
                   relief=RAISED, command=lambda : controller.show_frame(SearchByUsernamePage)).place(x=50,y=550)
            Button(self, text='List of Users',width=17,height=1,bd=10,font=("bold",50),bg='navy',fg='white',relief=RAISED,
                   command=lambda : controller.show_frame(ListOfUsersPage)).place(x=800,y=550)


class AddUserPage(tk.Frame) :
    '''This is a add user page where admin can add only another admin whereas
        super admin can add both admin and another super admin...'''

    global current_role

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Add User")
        self.addUserFunction(controller,labelframe)
        controller.footer(labelframe)

    def addUserFunction(self,controller,labelframe) :
        '''For checking current role to display the way of add user page...'''

        #add user page for super admin user
        if(current_role == "SuperAdmin") :
            label_user = Label(labelframe,text="Name:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_user.place(x=50,y=50)
            #work here#
            self.name = StringVar(self , value="")
            entry_user = Entry(labelframe,textvariable=self.name,width=25,bd=5,bg="white",fg="navy")
            entry_user.place(x=230,y=50)
            label_uname = Label(labelframe, text="Username:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_uname.place(x=45,y=120)
            self.username = StringVar(self , value="")
            entry_uname = Entry(labelframe,textvariable=self.username,width=25,bd=5,bg="white",fg="navy")
            entry_uname.place(x=230,y=123)
            label_email = Label(labelframe, text="Email:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_email.place(x=45,y=190)
            self.email = StringVar(self , value="")
            entry_email = Entry(labelframe,textvariable=self.email,width=25,bd=5,bg="white",fg="navy")
            entry_email.place(x=230,y=198)
            label_role = Label(labelframe, text="Role:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_role.place(x=45,y=260)
            self.role = IntVar(self,1)
            Radiobutton(labelframe,text="Admin",variable=self.role, value=1,font=("courier", 15,"bold"),
                        fg="black",bg="gainsboro",activeforeground="navy").place(x=230,y=260)
            Radiobutton(labelframe, text="SuperAdmin", variable=self.role, value=2,font=("courier", 15,"bold"),
                        fg="black",bg="gainsboro",activeforeground="navy").place(x=230,y=300)
            Button(labelframe, text='Add',width=20,font=("bold",12),bg='navy',fg='white',bd=5,
                   command = lambda : self.addUser(self.name.get(),self.email.get(),self.username.get(),
                                              self.role.get(),controller)).place(x=90,y=390)
        #add user page for admin user
        if(current_role == "Admin") :
            label_user = Label(labelframe,text="Name:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_user.place(x=50,y=50)
            self.name = StringVar(self , value="")
            entry_user = Entry(labelframe,textvariable=self.name,width=25,bd=5,bg="white",fg="navy")
            entry_user.place(x=230,y=50)
            label_uname = Label(labelframe, text="Username:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_uname.place(x=45,y=120)
            self.username = StringVar(self , value="")
            entry_uname = Entry(labelframe,textvariable=self.username,width=25,bd=5,bg="white",fg="navy")
            entry_uname.place(x=230,y=123)
            label_email = Label(labelframe, text="Email:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_email.place(x=45,y=190)
            self.email = StringVar(self , value="")
            entry_email = Entry(labelframe,textvariable=self.email,width=25,bd=5,bg="white",fg="navy")
            entry_email.place(x=230,y=198)
            label_role = Label(labelframe, text="Role:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_role.place(x=45,y=260)
            self.role = IntVar(self,1)
            Radiobutton(labelframe,text="Admin",variable=self.role, value=1,font=("courier", 15,"bold"),fg="black",
                        bg="gainsboro",activeforeground="navy").place(x=230,y=260)
            Button(labelframe, text='Add',width=20,font=("bold",12),bg='navy',fg='white',bd=5,
                   command = lambda : self.addUser(self.name.get(),self.email.get(),self.username.get(),
                                              self.role.get(),controller)).place(x=90,y=350)

    def addUser(self,name,email,username,role,controller) :
        '''This function adds or registers a user to the database which can be done by only existing user...'''

        if(name == "" or email == "" or username == "") :
            messagebox.showwarning("Warning","Please fill all the details!!!")
        else:
            try :
                connection = ""
                name_error = controller.validationName(name,self)
                username_error = controller.validationUsername(username,self)
                email_error = controller.validationEmail(email,self)
                error = name_error + username_error + email_error
                if(error != "") :
                    messagebox.showwarning("Warning",error)    
                else :
                    self.name.set("")
                    self.email.set("")
                    self.username.set("")
                    self.role.set(1)
                    try :
                        password = controller.passwordGenerationFunction(email)
                    except :
                        messagebox.showeerror("Error","Password Cannot be sent right now!!!\nTry again later...")
                        return 0                                #for terminating function after exception...
                    hashed_password = hashlib.md5(password.encode()).hexdigest()
                    connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
                    cursor = connection.cursor()
                    connection.autocommit(True)
                    if(role == 1) :
                        query = f"INSERT INTO `user_table`(`name`,`email`,`username`,`password`,`role`) VALUES ('{name}','{email}','{username}','{hashed_password}','Admin');"
                    if(role == 2) :
                        query = f"INSERT INTO `user_table`(`name`,`email`,`username`,`password`,`role`) VALUES ('{name}','{email}','{username}','{hashed_password}','SuperAdmin');"
                    cursor.execute(query)
                    controller.load_function()
                    controller.show_frame(AddUserPage)
                    messagebox.showinfo("Success","User Added successfully...\n\nPassword has been sent to added user's mail id..")
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()
                    

class DeleteUserPage(tk.Frame) :
    '''This is a Delete user page for super admin only
        where he can delete only another admin not super admin...'''

    global current_role
    
    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Delete User")
        self.deleteUserFunction(controller,labelframe)
        controller.footer(labelframe)

    def deleteUserFunction(self,controller,labelframe) :
        '''For deleting user functonality for super admin only...'''

        if(current_role == "SuperAdmin") :        
            label_user = Label(labelframe,text="Please enter the username for deleting the user.",font=("courier", 20,"bold"),
                               fg="navy",bg="gainsboro")
            label_user.place(x=45,y=50)
            label_uname = Label(labelframe, text="Username:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_uname.place(x=45,y=140)
            self.username = StringVar(self , "")
            entry_uname = Entry(labelframe,textvariable=self.username,width=25,bd=5,bg="white",fg="navy")
            entry_uname.place(x=200,y=145)
            Button(labelframe, text='Delete',width=10,font=("bold",12),bg='navy',fg='white',bd=5,
                   command=lambda : self.deleteUser(self.username.get(),controller)).place(x=130,y=230)

    def deleteUser(self,username,controller) :
        '''This Function deletes the user from database...only Super Admin
            can delete a user that too only a admin user not another super admin...'''

        global current_username
        if(username == "") :
            messagebox.showwarning("Warning","please fill the username!!!")
        elif (username == current_username):
            messagebox.showwarning("Warning","You cannot delete Yourself from databse!!!")
            self.username.set("")
        else :
            connection = ""
            try:
                self.username.set("")
                connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
                cursor = connection.cursor()
                connection.autocommit(True)
                query = f"SELECT `username`,`role` FROM `user_table` WHERE `username` = '{username}';"
                cursor.execute(query)
                current_data = cursor.fetchone() == None
                if(current_data == None) :
                    messagebox.showwarning("Warning","This User does not Exists...!!!")
                else :
                    if(current_data[1] == "SuperAdmin") :
                        messagebox.showwarning("Warning","You Don't have Permission to Delete Super Admin...!!!")
                    else :
                        query = f"DELETE FROM `user_table` WHERE `user_table`.`username` = '{username}';"
                        if(messagebox.askokcancel('Confirm', 'Are You sure want to delete User?')):
                            cursor.execute(query)
                            controller.load_function()
                            controller.show_frame(DeleteUserPage)
                            messagebox.showinfo("Success","User has been deleted...")
                        else :
                            messagebox.showinfo("Info","User has not been deleted...!!!")
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()
                

class ChangeRolePage(tk.Frame) :
    '''This is a Change role of the user page for super admin only where
        he can change role for another admin not super admin...'''

    global current_role

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Change Role")
        self.changeRoleFunction(controller,labelframe)
        controller.footer(labelframe)

    def changeRoleFunction(self,controller,labelframe) :
        '''For changing role of user functionality for super admin only...'''

        if(current_role == "SuperAdmin") :
            label_user = Label(labelframe,text="Please enter the username for changing role of the user.",
                               font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_user.place(x=45,y=50)
            label_uname = Label(labelframe, text="Username:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_uname.place(x=45,y=140)
            self.username = StringVar(self , "")
            entry_uname = Entry(labelframe,textvariable=self.username,width=25,bd=5,bg="white",fg="navy")
            entry_uname.place(x=200,y=145)
            label_uname = Label(labelframe, text="Role:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_uname.place(x=45,y=230)
            self.role = IntVar(self,1)
            Radiobutton(labelframe,text="SuperAdmin",variable=self.role, value=1,font=("courier", 20,"bold"),
                        fg="navy",bg="gainsboro",activeforeground="navy").place(x=200,y=230)
            Button(labelframe, text='Change',width=10,font=("bold",12),bg='navy',fg='white',bd=5,
                   command=lambda:self.changeRole(self.username.get(),self.role.get(),controller)).place(x=100,y=320)

    def changeRole(self,username,role,controller) :
        '''This function changes the role of the user :- only superadmin can change role of admin to superadmin...'''

        global current_username
        if(username == "") :
            messagebox.showwarning("Warning","please fill the username!!!")
        elif (username == current_username):
            messagebox.showwarning("Warning","You cannot change your own role!!!")
            self.username.set("")
            self.role.set(1)
        else :
            connection = ""
            try:
                self.username.set("")
                self.role.set(1)
                connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
                cursor = connection.cursor()
                connection.autocommit(True)
                query = f"SELECT `username`,`role` FROM `user_table` WHERE `username` = '{username}';"
                cursor.execute(query)
                current_data = cursor.fetchone()
                if(current_data == None) :
                    messagebox.showwarning("Warning","This User does not Exists...!!!")
                else :
                    if(current_data[1] == "SuperAdmin") :
                        messagebox.showwarning("Warning","This User is already a Super Admin User!!!")
                    else :
                        if(role == 1) :
                            actual_role = "SuperAdmin"
                        query = f"UPDATE `user_table` SET `role`='{actual_role}' WHERE `username` = '{username}';"
                        if(messagebox.askokcancel('Confirm', 'Are You sure want to Change Role of the User?')):
                            cursor.execute(query)
                            controller.load_function()
                            controller.show_frame(ChangeRolePage)
                            messagebox.showinfo("Success","User's Role has been changed...")
                        else :
                            messagebox.showinfo("Info","User's role has not been changed...!!!")
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()


class SearchByUsernamePage(tk.Frame) :
    '''This is a search by username where user can search anyone by username...'''

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Search By Username")
        self.searchByUsernameFunction(controller,labelframe)
        controller.footer(labelframe)

    def searchByUsernameFunction(self,controller,labelframe) :
        '''This is functionality for displaying search by username page...'''

        label_uname1 = Label(labelframe, text="S.N0.",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=5,relief=RAISED)
        label_uname1.place(x=49,y=10)
        label_uname1 = Label(labelframe, text="Name",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=25,relief=RAISED)
        label_uname1.place(x=154,y=10)
        label_uname1 = Label(labelframe, text="Email",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=25,relief=RAISED)
        label_uname1.place(x=579,y=10)
        label_uname1 = Label(labelframe, text="Username",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=16,relief=RAISED)
        label_uname1.place(x=1004,y=10)
        label_uname1 = Label(labelframe, text="Role",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=10,relief=RAISED)
        label_uname1.place(x=1285,y=10)
        frame1=Frame(labelframe,bg="grey",height=480,width=480,bd=3)
        frame1.place(x=50,y=60)
        self.lis=Listbox(frame1, width=138, height=1, font=("courier", 12,"bold"),bg="white",bd=6,relief=RAISED)
        self.lis.pack(side="left", fill=BOTH)
        scrollbar = Scrollbar(frame1, orient="vertical")
        scrollbar.config(command=self.lis.yview)
        scrollbar.pack(side="left", fill="y")
        self.lis.config(yscrollcommand=scrollbar.set) 
        label_uname = Label(labelframe, text="Enter  Username of user to search.",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
        label_uname.place(x=45,y=150)
        label_uname = Label(labelframe, text="Username:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
        label_uname.place(x=45,y=220)
        self.username = StringVar(self , "")
        entry_uname = Entry(labelframe,textvariable=self.username,width=37,bd=5,bg="white",fg="navy")
        entry_uname.place(x=220,y=220)
        Button(labelframe, text='Search',width=13,font=("courier",12,"bold"),bg='navy',fg='white',bd=5,
               command=lambda:self.searchByUsername(self.username.get())).place(x=200,y=290)
        self.lis.delete(0, END)
        
    def searchByUsername(self,username) :
        '''This function search a user by its username and display particular user's information...'''

        self.lis.delete(0, END)
        if(username == "") :
            messagebox.showwarning("Warning","please fill the username!!!")
        else :
            connection = ""
            try:
                self.username.set("")
                connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
                cursor = connection.cursor()
                connection.autocommit(True)
                query = f"SELECT `name`,`email`,`username`,`role` FROM `user_table` WHERE `username` = '{username}';"
                cursor.execute(query)
                current_data = cursor.fetchone()
                if(current_data == None) :
                    messagebox.showwarning("Warning","This User does not Exists...!!!")
                else :
                    srno = 1
                    fsrno =  str(srno) + "." + "".join([" " for _ in range(9-len(str(srno)))])
                    fname =  current_data[0] + "".join([" " for _ in range(43-len(current_data[0]))])
                    femail = current_data[1] + "".join([" " for _ in range(43-len(current_data[1]))])
                    fusername = current_data[2] + "".join([" " for _ in range(28-len(current_data[2]))])
                    frole = current_data[3] + "".join([" " for _ in range(15-len(current_data[3]))])
                    fstring = fsrno + fname + femail + fusername + frole
                    self.lis.insert(END , fstring)
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()
                

class ListOfUsersPage(tk.Frame) :
    '''This is a see all users list where like all users or admins users or super admins users...'''

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"List of Users")
        self.listOfUsersFunction(controller,labelframe)
        controller.footer(labelframe)

    def listOfUsersFunction(self,controller,labelframe) :
        '''This is functionality for displaying list of users page...'''
        
        label_uname1 = Label(labelframe, text="S.N0.",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=5,relief=RAISED)
        label_uname1.place(x=49,y=10)
        label_uname1 = Label(labelframe, text="Name",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=25,relief=RAISED)
        label_uname1.place(x=154,y=10)
        label_uname1 = Label(labelframe, text="Email",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=25,relief=RAISED)
        label_uname1.place(x=579,y=10)
        label_uname1 = Label(labelframe, text="Username",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=16,relief=RAISED)
        label_uname1.place(x=1004,y=10)
        label_uname1 = Label(labelframe, text="Role",font=("courier", 20,"bold"),fg="white",bg="navy",bd=10,width=10,relief=RAISED)
        label_uname1.place(x=1285,y=10)
        frame1=Frame(labelframe,bg="grey",height=480,width=480,bd=3)
        frame1.place(x=50,y=60)
        self.lis=Listbox(frame1, width=138, height=17, font=("courier", 12,"bold"),bg="white",bd=6,relief=RAISED)
        self.lis.pack(side="left", fill=BOTH)
        scrollbar = Scrollbar(frame1, orient="vertical")
        scrollbar.config(command=self.lis.yview)
        scrollbar.pack(side="left", fill="y")
        self.lis.config(yscrollcommand=scrollbar.set)
        Button(labelframe, text='All Users',width=20,font=("courier", 15,"bold"),bg='navy',fg='white',bd=5,
               command=lambda:self.listOfUsers("ALL")).place(x=50,y=430)
        Button(labelframe, text='All SuperAdmins',width=20,font=("courier", 15,"bold"),bg='navy',fg='white',bd=5,
               command=lambda:self.listOfUsers("SUPERADMINS")).place(x=350,y=430)
        Button(labelframe, text='All Admins',width=20,font=("courier", 15,"bold"),bg='navy',fg='white',bd=5,
               command=lambda:self.listOfUsers("ADMINS")).place(x=650,y=430)
            
    def listOfUsers(self,flag) :
        '''This Function shows list of users according to users preferences
            i.e. only admins or superadmins or all users...'''

        self.lis.delete(0,END)
        connection = ""
        connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
        cursor = connection.cursor()
        connection.autocommit(True)
        if(flag == "ALL") :
            query = f"SELECT `name`,`email`,`username`,`role` FROM `user_table`;"
            cursor.execute(query)
        elif(flag == "SUPERADMINS") :
            query = f"SELECT `name`,`email`,`username`,`role` FROM `user_table` WHERE `role` = 'SuperAdmin';"
            cursor.execute(query)
        elif(flag == "ADMINS") :
            query = f"SELECT `name`,`email`,`username`,`role` FROM `user_table` WHERE `role` = 'Admin';"
            cursor.execute(query)
        current_data = cursor.fetchone()
        srno = 1
        while(current_data != None) :
            fsrno =  str(srno) + "." + "".join([" " for _ in range(9-len(str(srno)))])
            fname =  current_data[0] + "".join([" " for _ in range(43-len(current_data[0]))])
            femail = current_data[1] + "".join([" " for _ in range(43-len(current_data[1]))])
            fusername = current_data[2] + "".join([" " for _ in range(28-len(current_data[2]))])
            frole = current_data[3] + "".join([" " for _ in range(15-len(current_data[3]))])
            fstring = fsrno + fname + femail + fusername + frole
            self.lis.insert(END , fstring)
            current_data = cursor.fetchone()
            srno += 1


class EditDetailsPage(tk.Frame) :
    '''This is a Edit details page where any logged in user can change their details
        like name,email,username,password but not role :) ...'''

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Edit Details")
        self.editDetailsFunction(controller,labelframe)
        controller.footer(labelframe)

    def editDetailsFunction(self,controller,labelframe) :
        '''This is functionality for editing details page...'''

        Button(labelframe, text='Edit Name',width=20,bd=7,font=("courier",20,"bold"),bg='navy',fg='white',relief=RAISED,
               command = lambda : controller.show_frame(EditNamePage)).place(x=90,y=50)
        Button(labelframe, text='Edit Username',width=20,bd=7,font=("courier",20,"bold"),bg='navy',fg='white',relief=RAISED,
               command = lambda : controller.show_frame(EditUsernamePage)).place(x=90,y=150)
        Button(labelframe, text='Edit Email',width=20,bd=7,font=("courier",20,"bold"),bg='navy',fg='white',relief=RAISED,
               command = lambda : controller.show_frame(EditEmailPage)).place(x=90,y=250)
        Button(labelframe, text='Edit Password',width=20,bd=7,font=("courier",20,"bold"),bg='navy',fg='white',relief=RAISED,
               command = lambda : controller.show_frame(EditPasswordPage)).place(x=90,y=350)


class EditNamePage(tk.Frame) :
    '''This is a Edit name page...'''

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Edit Name")
        self.editNameFunction(controller,labelframe)
        controller.footer(labelframe)

    def editNameFunction(self,controller,labelframe) :
        '''This is for displaying editing name page'''

        label_uname = Label(labelframe, text="Enter New Name:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
        label_uname.place(x=45,y=120)
        self.name = StringVar(self , "")
        entry_name = Entry(labelframe,textvariable=self.name,width=35,bd=5,bg="white",fg="navy")
        entry_name.place(x=50,y=200)
        Button(labelframe, text='Change',width=13,font=("courier",12,"bold"),bg='navy',fg='white',bd=5,
               command=lambda:self.editName(self.name.get(),controller)).place(x=85,y=280)

    def editName(self,name,controller) :
        '''This function edits name of a current user...'''

        global current_name
        if(name == "") :
            messagebox.showwarning("Warning","please enter the Name...!!!")
        elif(name == current_name) :
            self.name.set("")
            messagebox.showwarning("Warning","Your New Name cannot be same as Old Name!!!")
        else :        
            try :
                connection = ""
                error = controller.validationName(name,self)
                if(error != "") :
                    messagebox.showwarning("Warning",error)
                else :
                    self.name.set("")
                    global current_username
                    connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
                    cursor = connection.cursor()
                    connection.autocommit(True)
                    query = f"UPDATE `user_table` SET `name`= '{name}' WHERE username = '{current_username}';"
                    cursor.execute(query)
                    current_name = name
                    controller.load_function()
                    controller.show_frame(EditNamePage)
                    messagebox.showinfo("Success","Your Name has been updated...")
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()


class EditUsernamePage(tk.Frame) :
    '''This is a edit email id page...'''

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Edit Username")
        self.editUsernameFunction(controller,labelframe)
        controller.footer(labelframe)

    def editUsernameFunction(self,controller,labelframe) :
        '''This is for displaying editing username page'''

        label_uname = Label(labelframe, text="Enter New Username:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
        label_uname.place(x=45,y=120)
        self.username = StringVar(self , "")
        entry_uname = Entry(labelframe,textvariable=self.username,width=45,bd=5,bg="white",fg="navy")
        entry_uname.place(x=50,y=200)
        Button(labelframe, text='Change',width=13,font=("courier",12,"bold"),bg='navy',fg='white',bd=5,
               command=lambda:self.editUsername(self.username.get(),controller)).place(x=105,y=280)

    def editUsername(self,username,controller) :
        '''This function edits username of a current user...'''

        global current_username
        if(username == "") :
            messagebox.showwarning("Warning","please enter the Username...!!!")
        elif(username == current_username) :
            self.username.set("")
            messagebox.showwarning("Warning","Your New Usernname cannot be same as Old Username")
        else :        
            try :
                connection = ""
                error = controller.validationUsername(username,self)
                if(error != "") :
                    messagebox.showwarning("Warning",error)
                else :
                    self.username.set("")
                    connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
                    cursor = connection.cursor()
                    connection.autocommit(True)    
                    query = f"UPDATE `user_table` SET `username`= '{username}' WHERE username = '{current_username}';"
                    cursor.execute(query)
                    current_username = username
                    controller.load_function()
                    controller.show_frame(EditUsernamePage)
                    messagebox.showinfo("Success","Your Username has been updated...")
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()


class EditEmailPage(tk.Frame) :
    '''This is a edit email id page...'''
    
    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Edit Email")
        self.editEmailFunction(controller,labelframe)
        controller.footer(labelframe)

    def editEmailFunction(self,controller,labelframe) :
        '''This is for displaying editing email address page'''

        global otp_display
        
        if(otp_display not in [1,2,3]) :            
            label_uname = Label(labelframe, text="Enter New Email-ID:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_uname.place(x=45,y=100)
            self.email = StringVar(self , "")
            entry_uname = Entry(labelframe,textvariable=self.email,width=45,bd=5,bg="white",fg="navy")
            entry_uname.place(x=50,y=180)
            Button(labelframe, text='Send OTP',width=13,font=("courier",12,"bold"),bg='navy',fg='white',bd=5,
                   command=lambda : self.showOtpEntryFunction(self.email.get(),controller)).place(x=120,y=260)
        if(otp_display in [1,2,3]) :    
            label_uname = Label(labelframe, text="Enter OTP:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_uname.place(x=45,y=100)
            self.otp = StringVar(self , "")
            entry_uname = Entry(labelframe,textvariable=self.otp,width=45,bd=5,bg="white",fg="navy")
            entry_uname.place(x=50,y=180)
            Button(labelframe, text='Change',width=13,font=("courier",12,"bold"),bg='navy',fg='white',bd=5,
                   command=lambda : self.editEmail(self.otp.get(),controller)).place(x=120,y=260)
            label_uname = Label(labelframe, text="Enter correct OTP in 3 attempts!!!\n\nYou have  " \
                                + str(otp_display) + " attempts left...",
                                font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
            label_uname.place(x=45,y=340)

    def showOtpEntryFunction(self,email,controller) :
        '''This function will send otp if email is valid and direct app to enter otp frame...'''

        global current_email
        if(email == "") :
            messagebox.showwarning("Warning","please enter the Email...!!!")
        elif(email == current_email) :
            self.email.set("")
            messagebox.showwarning("Warning","Your New Email cannot be same as Old Email!!!")
        else :        
            try :
                connection = ""
                error = controller.validationEmail(email,self)
                if(error != "") :
                    messagebox.showwarning("Warning",error)
                else :
                    self.email.set("")
                    try :
                        global req_otp
                        otp = controller.otpGenerationFunction(email)
                        req_otp = otp
                    except :
                        messagebox.showerror("Error","OTP Cannot be sent right now!!!\nTry again later...")
                        return 0                                #for terminating function after exception...
                    global req_email
                    req_email = email
                    global otp_display
                    otp_display = 3
                    messagebox.showinfo("Success","OTP has been sent to your mail ID...")
                    controller.load_function()
                    controller.show_frame(EditEmailPage)    
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()

    def editEmail(self,otp,controller) :
        '''This function edits email of a current user if enterd otp is correct...'''
        
        if(otp == "") :
            messagebox.showwarning("Warning","please enter the OTP sent to your mail Id!!!")
        else :        
            global otp_display
            global req_otp
            global req_email
            self.otp.set("")
            if(otp != req_otp) :
                messagebox.showwarning("Warning","OTP You entered is incorrect!!!")
                otp_display -= 1
                if(otp_display == 0) :
                    messagebox.showwarning("Warning","You are not left with any attempt!!!")
                controller.load_function()
                controller.show_frame(EditEmailPage)
            else :
                try :
                    global current_username
                    global current_email
                    connection = ""
                    connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
                    cursor = connection.cursor()
                    connection.autocommit(True)
                    query = f"UPDATE `user_table` SET `email`= '{req_email}' WHERE `username` = '{current_username}';"
                    cursor.execute(query)
                    current_email = req_email
                    req_otp = ""
                    req_email = ""
                    otp_display = 0
                    messagebox.showinfo("Success","Your Email has been updated...")
                    controller.load_function()
                    controller.show_frame(EditEmailPage)
                except :
                    messagebox.showerror("Error","Connection to database cannot be established!!!")
                finally :
                    if(connection != "") :
                        connection.close()


class EditPasswordPage(tk.Frame) :
    '''This is a edit password page...'''

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        labelframe = controller.header(self,"Edit Password")
        self.editPasswordFunction(controller,labelframe)
        controller.footer(labelframe)

    def editPasswordFunction(self,controller,labelframe) :
        '''This is for displaying editing name page'''

        label_uname = Label(labelframe, text="Enter Old Password:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
        label_uname.place(x=40,y=35)
        self.old_password = StringVar(self , "")
        entry_uname = Entry(labelframe,textvariable=self.old_password,width=45,bd=5,bg="white",fg="navy")
        entry_uname.place(x=45,y=100)
        label_uname = Label(labelframe, text="Enter New Password:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
        label_uname.place(x=40,y=150)
        self.new_password = StringVar(self , "")
        entry_uname = Entry(labelframe,textvariable=self.new_password,width=45,bd=5,bg="white",fg="navy")
        entry_uname.place(x=45,y=210)
        label_uname = Label(labelframe, text="Confirm New Password:",font=("courier", 20,"bold"),fg="navy",bg="gainsboro")
        label_uname.place(x=45,y=270)
        self.confirm_password = StringVar(self , "")
        entry_uname = Entry(labelframe,textvariable=self.confirm_password,width=45,bd=5,bg="white",fg="navy")
        entry_uname.place(x=45,y=335)
        Button(labelframe, text='Change',width=13,font=("courier",12,"bold"),bg='navy',fg='white',bd=5,
               command=lambda : self.editPassword(self.old_password.get(),self.new_password.get(),
                                             self.confirm_password.get(),controller)).place(x=105,y=420)
    
    def editPassword(self,old_password,new_password,confirm_password,controller) :
        '''This function will edit the password of the current user...'''

        if(old_password == "" or new_password == "" or confirm_password == "") :
            messagebox.showwarning("Warning","please fill the credentials...!!!")
        else :
            connection = ""
            try :
                if(self.validatePassword(old_password,new_password,confirm_password)) :
                    global current_username    
                    connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
                    cursor = connection.cursor()
                    connection.autocommit(True)
                    hashed_password = hashlib.md5(new_password.encode()).hexdigest()
                    query = f"UPDATE `user_table` SET `password`= '{hashed_password}' WHERE username = '{current_username}';"
                    cursor.execute(query)
                    messagebox.showinfo("Success","Your Password has been updated...")        
            except :
                messagebox.showerror("Error","Connection to database cannot be established!!!")
            finally :
                if(connection != "") :
                    connection.close()

    def validatePassword(self,old_password,new_password,confirm_password) :
        '''This checks validaty of passwords enterd..'''

        error = ""
        hashed_old_pass = hashlib.md5(old_password.encode()).hexdigest()
        hashed_new_pass = hashlib.md5(new_password.encode()).hexdigest()
        hashed_con_pass = hashlib.md5(confirm_password.encode()).hexdigest()            
        connection = ""
        connection = pymysql.connect(host="localhost",user="root",passwd="", database="ums_database")
        cursor = connection.cursor()
        connection.autocommit(True)
        global current_username
        query = f"SELECT `password` FROM `user_table` WHERE `username` = '{current_username}';"
        cursor.execute(query)
        hashed_actual_pass = cursor.fetchone()[0]
        self.old_password.set("")
        self.new_password.set("")
        self.confirm_password.set("")
        if(hashed_old_pass != hashed_actual_pass) :
            messagebox.showwarning("Warning","Your Old Password is incorrect...")
            return False
        elif(hashed_new_pass == hashed_old_pass) :
            messagebox.showwarning("Warning","Your New Password cannot be same as Old Password...")
            return False
        else :   
            if(hashed_new_pass != hashed_con_pass) :
                messagebox.showwarning("Warning","Your New Password and Confirmed Password does not match...")
                return False
            else :
                return True


############################################################Execution Starts Here###################################################


app = umsApp()                                          #instance of base class
app.mainloop()                                          #mainloop is like a indefinite loop which will run the program continuosly

