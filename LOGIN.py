import tkinter as tk
import mysql.connector


#database
"""mydb = mysql.connector.connect(host = "localhost", user="Aman", database = "mydb")
mycursor = mydb.cursor()"""


#functions
def signup():
    
    global S_no
    
    signup_win = tk.Toplevel()
    signup_win.geometry("400x400")
    
    signup_win.title("CRYPTOCURRENCY PORTFOLIO MANAGEMENT")
    tk.Label(signup_win,text="SIGN UP",justify='center',font=('Times 18')).place(x=150,y=100)
    
    name_var = tk.StringVar()
    passwd_var = tk.StringVar()
    passwd2_var = tk.StringVar()
    
    tk.Label(signup_win,text="USERNAME").place(x=100,y=150)
    tk.Label(signup_win,text="PASSWORD").place(x=100,y=180)
    tk.Label(signup_win,text="RE-ENTER PASSWORD").place(x=100,y=210)
    
    tk.Entry(signup_win,textvariable=name_var,width=20).place(x=230,y=150)
    tk.Entry(signup_win,textvariable=passwd_var,show="*",width=20).place(x=230,y=180)
    tk.Entry(signup_win,textvariable=passwd2_var,show="*",width=20).place(x=230,y=210)

    name = name_var.get()
    passwd = passwd_var.get()
    passwd2 = passwd2_var.get()

    #if passwd!=passwd2:
        #tk.Label(signup_win,text="Re-enter the password").place(x=150,y=230)
        
    tk.Button(signup_win,text="SIGN UP",height=2,width=8,command=signup_win.after(10000,signup_win.destroy)).place(x=150,y=300)

    name_var.set("")
    passwd_var.set("")
    passwd2_var.set("")
        
def signing(name,passwd):
    pass
def check_login(name,passwd):
    pass
def login():
    
    login_win = tk.Toplevel()
    login_win.geometry("400x400")
    
    login_win.title("CRYPTOCURRENCY PORTFOLIO MANAGEMENT")
    tk.Label(login_win,text="LOG IN",justify='center',font=('Times 18')).place(x=150,y=100)
    
    name_var = tk.StringVar()
    passwd_var = tk.StringVar()
    
    tk.Label(login_win,text="USERNAME").place(x=100,y=150)
    tk.Label(login_win,text="PASSWORD").place(x=100,y=180)
    
    tk.Entry(login_win,textvariable=name_var,width=20).place(x=230,y=150)
    tk.Entry(login_win,textvariable=passwd_var,show="*",width=20).place(x=230,y=180)
    
    name = name_var.get()
    passwd = passwd_var.get()
    
    tk.Button(login_win,text="LOG IN",height=2,width=8,command=check_login(name,passwd)).place(x=150,y=300)
    

    
#main window
win = tk.Tk()
win.geometry("900x600")

win.title("CRYPTOCURRENCY PORTFOLIO MANAGEMENT")
tk.Label(win,text="CRYPTOCURRENCY PORTFOLIO MANAGEMENT",justify='center',fg='#308849',font=('Times 20')).place(x=180,y=150)

login_button = tk.Button(win,text="LOG IN",height=2,width=10,command=login)
login_button.place(x=300,y=400)

signup_button = tk.Button(win,text="SIGN UP",height=2,width=10,command=signup)
signup_button.place(x=500,y=400)
win.mainloop()
