# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:42:02 2020

@author: Abdullah
"""

from tkinter import *
from functools import partial


def signin():
    global username
    global password
    global useremail
    global password1
    global Squestion
    global Sanswer
    
    global Gui
    Gui = Tk()
    
    username = StringVar()
    password = StringVar()
    useremail = StringVar()
    password1 = StringVar()
    Squestion = StringVar()
    Sanswer = StringVar()
    
    
    Gui.geometry('500x400')  
    Gui.title('Messaging app')
    Gui.configure(background = "light green")

    Label(Gui, text="WELCOME TO MESSAGING APP",  bg = "light green", font= ("bold", 12)).grid(row=1, column= 3, columnspan = 3)
    Label(Gui, text="",  bg = "light green").grid(row=2, column= 3)
    Label(Gui, text="ENTER USERNAME AND PASSWORD TO CONTINUE",bg = "light green", font= ("bold", 8)).grid(row= 3, column = 0, columnspan = 4) 
    Label(Gui, text="",  bg = "light green").grid(row=4, column= 0)
    Label(Gui, text="",  bg = "light green").grid(row=4, column= 1)
    Label(Gui, text="User Name", width = 20, bg = "light green", font= ("bold", 10)).grid(row=4, column=2)
    Entry(Gui, textvariable=username).grid(row=4, column=3)
    Label(Gui,text="Password", width = 20, bg = "light green", font= ("bold", 10)).grid(row=5, column=2)  
    Entry(Gui, textvariable=password, show='*').grid(row=5, column=3)  

    loginButton = Button(Gui, text="Login", command=validateLogin,  bg = "light green", fg = "dark green").grid(row=6, column=2)
    Signup1 = Button(Gui, text="Signup", command=presignup, bg = "light green", fg = "dark green").grid(row=6, column=3)
    Gui.mainloop()

    
def signup():
   global root1
   root1 = Tk()
   root1.geometry('500x400')  
   root1.title('Messaging app')
   root1.configure(background = "light green")

   Label(root1, text="ENTER YOUR DATA, HERE", bg = "light green").grid(row= 2, column = 0, columnspan = 2)  

   Label(root1, text="User Name *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=4, column=0)
   Entry(root1, textvariable=username).grid(row=4, column=1) 
   Label(root1, text="Email *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=5, column=0)
   Entry(root1, textvariable=useremail).grid(row=5, column=1)
   Label(root1,text="Password *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=6, column=0)  
   Entry(root1, textvariable=password, show='*').grid(row=6, column=1)  
   Label(root1,text="Password *",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=7, column=0)  
   Entry(root1, textvariable=password1, show='*').grid(row=7, column=1) 
   Label(root1,text="Security Question",  width = 20, bg = "light green", font= ("bold", 10)).grid(row=8, column=0)  
   OptionMenu(root1, Squestion, "Which month you born? " ).grid(row=8, column=1) 
   Entry(root1, textvariable=Sanswer ).grid(row=9, column=1) 
   loginButton = Button(root1, text="Signup", command=savesignup, bg = "light green").grid(row=11, column=0)
   root1.mainloop()
   
def login():
   root2 = Tk()
   root2.geometry('500x400')  
   root2.title('Successfully login')
   
def savesignup():
    root1.destroy()
    signin()

def presignup():
    Gui.destroy()
    signup()

def validateLogin():
    Gui.destroy()
    login()

signin()

