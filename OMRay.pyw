# =======================================================
# Author : Rizki Nur Rachmadi Yudadiningrat
# SID    : 1900018014
# Subject: Teknik Informatika - Skripsi
# Project: OMRay - scanner for non-LJK exam paper
# Created: 10/11/2022
# Contact: +62 895 0811 7055 (Telegram)
# =======================================================

from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import ast

mainMenu = Tk()
mainMenu.title('OMRay')
mainMenu.geometry('500x925+100+20')
mainMenu.configure(bg="#fff")
mainMenu.resizable(False, False)
mainMenu.iconbitmap('img/OMRay.ico')

# header ===============================================

img = PhotoImage(file='img/wp1.png')
Label(mainMenu, image=img, bg='white').place(x=30, y=30)

frameSignIn = Frame(mainMenu, width=280, height=200, bg="white")
frameSignIn.place(x=200, y=30)

heading = Label(frameSignIn, text='OMRay', fg='#3B92EA', bg='white',
                font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=10, y=10)

Frame(frameSignIn, width=200, height=2, bg='#3B92EA').place(x=10, y=75)

subheading = Label(frameSignIn, text='Teacher tool for Exam', fg='#3B92EA', bg='white',
                   font=('Microsoft YaHei UI Light', 14, 'bold'))
subheading.place(x=10, y=90)
subheading2 = Label(frameSignIn, text='Made by Rizki Nur Rachmadi Y', fg='#3B92EA', bg='white',
                    font=('Microsoft YaHei UI Light', 9, 'bold'))
subheading2.place(x=10, y=120)

# function ===============================================


def autoRun():
    # hide dashboard ---------
    mainMenu.withdraw()
    # checking if account exist
    try:
        file = open('datasheet.dat', 'r+')
        d = file.read()
        r = ast.literal_eval(d)
        file.close()
    except:
        file = open('datasheet.dat', 'w')
        pp = str({'Username': 'password'})
        file.write(pp)
        file.close()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mainMenu.destroy()


def showSignUp():
    signUpWd = Toplevel(mainMenu)
    signUpWd.title("OMRay - Sign Up")

    signUpWd.geometry('925x500+300+200')
    signUpWd.configure(bg="#fff")
    signUpWd.resizable(False, False)

    # function ====================================================

    def signup():
        username = user.get()
        password = code.get()
        confirm_password = confirm_code.get()

        if password == confirm_password:
            try:
                file = open('datasheet.dat', 'r+')
                d = file.read()
                r = ast.literal_eval(d)

                dict2 = {username: password}
                r.update(dict2)
                file.truncate(0)
                file.close()

                file = open('datasheet.dat', 'w')
                w = file.write(str(r))

                messagebox.showinfo('Sign Up', 'Account created successfully')
                signUpWd.destroy()
            except:
                file = open('datasheet.dat', 'w')
                pp = str({'Username': 'password'})
                file.write(pp)
                file.close()

        else:
            messagebox.showerror('Invalid', "Password doesn't match")

    def signIn_cmd():
        signUpWd.destroy()

    # set tampilan ================================================

    img = PhotoImage(file='img/wp2.png')
    Label(signUpWd, image=img, bg='white').place(x=50, y=100)

    frame = Frame(signUpWd, width=350, height=390, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text='SIGN UP', fg='#3B92EA', bg='white',
                    font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=105, y=5)

    # entry ========================================================

    # username --------------------------------------

    def on_enter(e):
        name = user.get()
        if name == 'Username':
            user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')

    user = Entry(frame, width=25, fg='black', border=0,
                 bg='white', font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    # password --------------------------------------

    def on_enter(e):
        name = code.get()
        if name == 'Password':
            code.delete(0, 'end')

    def on_leave(e):
        name = code.get()
        if name == '':
            code.insert(0, 'Password')

    code = Entry(frame, width=25, fg='black', border=0,
                 bg='white', font=('Microsoft YaHei UI Light', 11))
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    # confirm password -------------------------------

    def on_enter(e):
        name = confirm_code.get()
        if name == 'Confirm password':
            confirm_code.delete(0, 'end')

    def on_leave(e):
        name = confirm_code.get()
        if name == '':
            confirm_code.insert(0, 'Confirm password')

    confirm_code = Entry(frame, width=25, fg='black', border=0,
                         bg='white', font=('Microsoft YaHei UI Light', 11))
    confirm_code.place(x=30, y=220)
    confirm_code.insert(0, 'Confirm password')
    confirm_code.bind('<FocusIn>', on_enter)
    confirm_code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

    # button ------------------------------------------

    sign_up = Button(frame, width=30, pady=7, text='Sign Up',
                     bg='#3B92EA', fg='white', border=0, cursor='hand2',
                     font=('Calibri(Body)', 9, 'bold'), command=signup)
    sign_up.pack()
    sign_up.place(x=35, y=280)

    label = Label(frame, text="Already have account?", fg='black',
                  bg='white', font=('Microsoft YaHei UI Light', 9))
    label.place(x=73, y=340)

    sign_in = Button(frame, width=6, text='Sign In', border=0,
                     bg='white', cursor='hand2', fg='#3B92EA',
                     font=('Calibri(Body)', 9, 'bold'), command=signIn_cmd)
    sign_in.place(x=223, y=340)

    # Main app---------------------

    signUpWd.mainloop()


def showSignIn():
    signInWd = Toplevel(mainMenu)
    signInWd.title('OMRay - Sign In')
    signInWd.geometry('925x500+300+200')
    signInWd.configure(bg="#fff")
    signInWd.resizable(False, False)

    # set tampilan ================================================

    imgSi = PhotoImage(file='img/wp.png')
    Label(signInWd, image=imgSi, bg='white').place(x=50, y=50)

    frameSignIn = Frame(signInWd, width=350, height=350, bg="white")
    frameSignIn.place(x=480, y=70)

    heading = Label(frameSignIn, text='SIGN IN', fg='#3B92EA', bg='white',
                    font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=105, y=5)

    # function ====================================================

    def signInCmd():
        username = user.get()
        password = code.get()

        file = open('datasheet.dat', 'r')
        d = file.read()
        r = ast.literal_eval(d)
        file.close()

        if username in r.keys() and password == r[username]:
            mainMenu.deiconify()
            signInWd.destroy()
        else:
            messagebox.showerror("Invalid", "invalid username or password")

    def signUp_cmd():
        showSignUp()

    # entry ========================================================

    # username --------------------------------------

    def on_enter(e):
        name = user.get()
        if name == 'Username':
            user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')

    user = Entry(frameSignIn, width=25, fg='black', border=0,
                 bg='white', font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frameSignIn, width=295, height=2, bg='black').place(x=25, y=107)

    # password --------------------------------------

    def on_enter(e):
        name = code.get()
        if name == 'Password':
            code.delete(0, 'end')

    def on_leave(e):
        name = code.get()
        if name == '':
            code.insert(0, 'Password')

    code = Entry(frameSignIn, width=25, fg='black', border=0,
                 bg='white', font=('Microsoft YaHei UI Light', 11))
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frameSignIn, width=295, height=2, bg='black').place(x=25, y=177)

    # button ------------------------------------------

    sign_in = Button(frameSignIn, width=30, pady=7, text='Sign In',
                     bg='#3B92EA', fg='white', border=0, cursor='hand2',
                     font=('Calibri(Body)', 9, 'bold'), command=signInCmd)
    sign_in.pack()
    sign_in.place(x=35, y=204)

    label = Label(frameSignIn, text="Don't have an account?", fg='black',
                  bg='white', font=('Microsoft YaHei UI Light', 9))
    label.place(x=70, y=270)

    sign_up = Button(frameSignIn, width=6, text='Sign Up', border=0,
                     bg='white', cursor='hand2', fg='#3B92EA',
                     font=('Calibri(Body)', 9, 'bold'), command=signUp_cmd)
    sign_up.place(x=223, y=270)

    signInWd.protocol("WM_DELETE_WINDOW", on_closing)
    signInWd.mainloop()


# button =================================================

frame_btn = Frame(mainMenu, width=440, height=650, bg="white")
frame_btn.place(x=30, y=230)

# @@@ bagian tambah format kertas ujian ==================================
papIco = PhotoImage(file='img/paper.png')
n_paper = Button(frame_btn, width=395, pady=15, text='Add New Paper',
                 bg='#3B92EA', fg='white', border=0, cursor='hand2',
                 font=('Calibri(Body)', 11, 'bold'), image=papIco,
                 compound=LEFT)
n_paper.place(x=20, y=20)

# @@@ bagian tambah mata pelajaran =======================================
subIco = PhotoImage(file='img/subject.png')
n_subject = Button(frame_btn, width=395, pady=15, text='Add New Subject',
                   bg='#3B92EA', fg='white', border=0, cursor='hand2',
                   font=('Calibri(Body)', 11, 'bold'), image=subIco,
                   compound=RIGHT)
n_subject.place(x=20, y=150)

# @@@ bagian edit format kertas ujian ====================================
perIco = PhotoImage(file='img/paperedit.png')
u_paper = Button(frame_btn, width=395, pady=15, text='Customize Existing Paper',
                 bg='#3B92EA', fg='white', border=0, cursor='hand2',
                 font=('Calibri(Body)', 11, 'bold'), image=perIco,
                 compound=LEFT)
u_paper.place(x=20, y=280)

# @@@ bagian edit mata pelajaran =========================================
jectIco = PhotoImage(file='img/subjectedit.png')
u_subject = Button(frame_btn, width=395, pady=15, text='Customize Existing Subject',
                   bg='#3B92EA', fg='white', border=0, cursor='hand2',
                   font=('Calibri(Body)', 11, 'bold'), image=jectIco,
                   compound=RIGHT)
u_subject.place(x=20, y=410)

# @@@ bagian mulai scanning ==============================================
scanIco = PhotoImage(file='img/scan.png')
scanbtn = Button(frame_btn, width=436, pady=30, text='Scan Exam Paper',
                 bg='#3B92EA', fg='white', border=0, cursor='hand2',
                 font=('Calibri(Body)', 15, 'bold'), image=scanIco,
                 compound=LEFT)
scanbtn.place(x=0, y=540)

# main app ===============================================

mainMenu.wait_visibility()
autoRun()
showSignIn()
mainMenu.mainloop()
