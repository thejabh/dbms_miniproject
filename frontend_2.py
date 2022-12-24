import tkinter as tk
import backend_2 as bef
import mysql.connector
import customtkinter as CTk

mydb = mysql.connector.connect(host = "localhost", user="root", database = "mydb",password='mysql')
mycursor = mydb.cursor()

general_font=('Times 18')
small_font=('Times 13')
large_font = ('Times 30')
current_theme='dark'
class MainWin:
    def __init__(self):
        self.win = CTk.CTk()
        self.win.state("zoomed")
        self.win.title("CRYPTOCURRENCY PORTFOLIO MANAGEMENT")
        self.frame1= CTk.CTkFrame()
        self.frame = CTk.CTkFrame(self.win,
                                  width=1100,height=850)
        self.frame.place(x=370,y=0)
        self.user_ = CTk.CTkLabel(self.frame,
                                  text="CRYPTOCURRENCY PORTFOLIO MANAGEMENT",
                                  justify='center',
                                  text_color='#308849',
                                  text_font=large_font)
        self.user_.place(x=120,y=150)
        
    def login(self):
        self.login_frame = CTk.CTkFrame(self.win,
                                        width=340,height=350)
        self.login_frame.place(x=20,y=70)
        self.title = CTk.CTkLabel(self.login_frame,
                                  text="LOGIN",
                                  text_font=general_font)
        self.title.place(x=100,y=20)
        self.name_var = tk.StringVar()
        self.passwd_var = tk.StringVar()
    
        self.login_label1 = CTk.CTkLabel(self.login_frame,
                                        text="USERNAME",
                                        text_font=small_font).place(x=0,y=100)
        self.login_entry1 = CTk.CTkEntry(self.login_frame,
                                        textvariable=self.name_var,
                                        width=200,
                                        height=30).place(x=130,y=100)
        
        self.login_label2 = CTk.CTkLabel(self.login_frame,  
                                        text="PASSWORD",
                                        text_font=small_font).place(x=0,y=150)
        self.login_entry2 = CTk.CTkEntry(self.login_frame,
                                        textvariable=self.passwd_var,
                                        show="*",
                                        width=200,
                                        height=30).place(x=130,y=150)

        self.login_but = CTk.CTkButton(self.login_frame,
                                       text="LOG IN",
                                       command=self.check_login,
                                       height=40,
                                       width=150).place(x=100,y=250)
                                       
        self.signup_but = CTk.CTkButton(self.login_frame,
                                       text="SIGN UP",
                                       command=self.signup,
                                       height=40,
                                       width=150).place(x=100,y=300)
    def signup(self):
        
        self.signup_win = CTk.CTkToplevel()
        self.signup_win.geometry("600x500")
        
        self.fullname_var =tk.StringVar()
        self.name_var =tk.StringVar()
        self.phno_var =tk.StringVar()
        self.passwd_var =tk.StringVar()
        self.passwd2_var =tk.StringVar()
    
        self.signup_win.title("CRYPTOCURRENCY PORTFOLIO MANAGEMENT")
        self.signup_win_label1 = CTk.CTkLabel(self.signup_win,
                                              text="SIGN UP",
                                              justify='center',
                                              text_font=general_font).place(x=200,y=70)
    
        self.signup_win_label2 = CTk.CTkLabel(self.signup_win,
                                              text="FULLNAME",
                                              text_font=small_font).place(x=10,y=130)
        self.signup_win_entry2 = CTk.CTkEntry(self.signup_win,
                                              textvariable=self.fullname_var,
                                              width=200).place(x=150,y=130)
        
        self.signup_win_label3 = CTk.CTkLabel(self.signup_win,
                                              text="USERNAME",
                                              text_font=small_font).place(x=10,y=160)
        self.signup_win_entry3 = CTk.CTkEntry(self.signup_win,
                                              textvariable=self.name_var,
                                              width=200).place(x=150,y=160)
        
        self.signup_win_label4 = CTk.CTkLabel(self.signup_win,
                                              text="PHONE NO.",
                                              text_font=small_font).place(x=10,y=190)
        self.signup_win_entry4 = CTk.CTkEntry(self.signup_win,
                                              textvariable=self.phno_var,
                                              width=200).place(x=150,y=190)
        
        self.signup_win_label5 = CTk.CTkLabel(self.signup_win,
                                              text="PASSWORD",
                                              text_font=small_font).place(x=10,y=220)
        self.signup_win_entry5 = CTk.CTkEntry(self.signup_win, 
                                              textvariable=self.passwd_var,
                                              show="*",
                                              width=200).place(x=150,y=220)
        
        self.signup_win_label6 = CTk.CTkLabel(self.signup_win,
                                              text="RE-ENTER\nPASSWORD",
                                              text_font=small_font).place(x=10,y=250)
        self.signup_win_entry6 = CTk.CTkEntry(self.signup_win,  
                                              textvariable=self.passwd2_var,
                                              show="*",
                                              width=200).place(x=150,y=250)

    
        self.signup_win_button1 = CTk.CTkButton(self.signup_win,text="SIGN UP",
                                                height=50,width=150,
                                                text_font=small_font,
                                                command=self.signing).place(x=200,y=350)
                            
    def signing(self):
        self.fullname = self.fullname_var.get()
        print(type(self.fullname))
        self.username = self.name_var.get()
        self.phno = self.phno_var.get()
        self.passwd = self.passwd_var.get()
        self.passwd2 = self.passwd2_var.get()
        
        if self.fullname=='' or self.username=='' or self.phno=='' or self.passwd=='':
            self.non = CTk.CTkLabel(self.signup_win,
                                    text="*FIELD IS EMPTY*",
                                    text_color='#f00',
                                    text_font=('Times 10')).place(x=150,y=300)
        else:
            if bef.selectfromusers(self.username) != '':
                self.ue = CTk.CTkLabel(self.signup_win,
                                    text="*USERNAME ALREADY EXIST*",
                                    text_color='#f00',
                                    text_font=('Times 10')).place(x=360,y=160)
        
            if len(self.phno)!=10:
                self.wpn = CTk.CTkLabel(self.signup_win,
                                        text="*INVALID PHONE NUMBER*",
                                        text_color='#f00',
                                        text_font=('Times 10')).place(x=360,y=190)
                
            if (self.passwd != self.passwd2) and self.passwd!='':
                self.wp = CTk.CTkLabel(self.signup_win,
                                    text="*PASSWORD DOESN'T MATCH*",
                                    text_color='#f00',
                                    text_font=('Times 10')).place(x=360,y=250)
            
            else:
                bef.insertintousers(self.fullname,self.username,self.phno,self.passwd)
            
        self.fullname_var.set("")
        self.name_var.set("")
        self.phno_var.set("")
        self.passwd_var.set("")
        self.passwd2_var.set("")
        
    def check_login(self):
        self.name = self.name_var.get()
        self.passwd = self.passwd_var.get()
        
        if bef.logindatabase(self.name,self.passwd) == True:
            print("successfully logged in")
            # self.login_frame.destroy()
            # self.win.destroy()
            #MainFrame(self.name)
        else:
            self.ue2 = CTk.CTkLabel(self.login_frame,text="USERNAME AND PASSWORD DOESN'T MATCH",text_color='#f00',text_font=('Times 10'))
            self.ue2.place(x=360,y=150)
        
        # if bef.logindatabase(self.name,self.passwd) != True:
        #     self.ue2 = CTk.CTkLabel(self.login_frame,
        #                             text="USERNAME AND PASSWORD DOESN'T MATCH",
        #                             text_color=('red','red'),
        #                             font=('Times 10'))
        #     self.ue2.place(x=30,y=60)
        #     # self.login_win.destroy()
        #     # self.win.destroy()
        #     #MainFrame(self.name)
        # else:
        #     self.ue2 = CTk.CTkLabel(self.login_frame,
        #                             text="USERNAME AND PASSWORD DOESN'T MATCH",
        #                             fg='#f00',font=('Times 10'))
        #     self.ue2.place(x=30,y=50)
        
        # self.passwd_var.set("")

if __name__=='__main__':
    app=MainWin()
    app.login()
    app.win.mainloop()
    
