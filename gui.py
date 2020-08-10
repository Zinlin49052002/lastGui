from tkinter import *

import client


fg = "#ffffff"
bg = "#333333"
placeholderFg = "gray"
font=('aril',14,'bold')



def changeFrame(old,new):
    old.destroy()
    new


def loginFrame():
    # Login frame create
    lf = Frame(client.root,bg=bg,bd=0,width=800,height=800,relief="solid")
    lf.config(highlightcolor="#FFA500",highlightbackground="#FFA500",highlightthickness=3)
    # Title
    title=Label(lf,text='Whisper',font=font,padx=150,pady=20,bg=bg,fg="#FFA500")
    # Entry field
    username = Entry(lf,width=26,textvariable=client.loginuserTV,fg=placeholderFg)
    username.delete(0,END)
    username.insert(0,"Username  ")
    placeHolder(username,"Username  ")
    
    password = Entry(lf,width=26,textvariable=client.loginpassTV,fg=placeholderFg)
    password.delete(0,END)
    password.insert(0,"Password  ")
    placeHolder(password,"Password  ","*")
    # Button
    loginButton = Button(lf,text="Login",relief="flat",padx=22,bg=bg,fg="#FFA500",command=lambda:changeFrame(lf,homeScreen()))
    signupButton = Button(lf,text="Signup",relief="flat",padx=18,bg=bg,fg="#FFA500",command=lambda : changeFrame(lf,signupFrame()))
    # Padding Bottom
    # Lpadlabel=Label(lf,bg=bg)
    # Adding into current frame
    title.grid(row=0,column=1)
    username.grid(row=1,column=0,columnspan=4,pady=20,ipady=7,ipadx=30)
    password.grid(row=2,column=0,columnspan=4,pady=20,ipady=7,ipadx=30)
    loginButton.grid(row=3,column=1,columnspan=2)
    signupButton.grid(row=4,column=1,columnspan=2,pady=30)
    # Lpadlabel.grid(row=5,column=1,pady=10)
    # Adding current frame to root
    lf.pack(anchor="center",pady=100)

def signupFrame():
    # Signup frame create
    sf = Frame(client.root,bg=bg,bd=0,width=800,height=800,relief="solid")
    sf.config(highlightcolor="#FFA500",highlightbackground="#FFA500",highlightthickness=3)
    # title
    title=Label(sf,text='Signup ',font=font,padx=150,pady=20,bg=bg,fg="#FFA500")
    # Entry field
    
    global siusername
    siusername = Entry(sf,width=26,textvariable=client.signupuserTV,fg=placeholderFg)
    siusername.delete(0,END)
    siusername.insert(0,"Username  ")
    placeHolder(siusername,"Username  ")
    
   
    password = Entry(sf,width=26,textvariable=client.signuppassTV,fg=placeholderFg)
    password.delete(0,END)
    password.insert(0,"Password  ")
    placeHolder(password,"Password  ","*")
    
    rePassword = Entry(sf,width=26,fg=placeholderFg)
    rePassword.delete(0,END)
    rePassword.insert(0,"Repassword  ")
    placeHolder(rePassword,"Repassword  ","*")
    
    email = Entry(sf,width=26,textvariable=client.signupemailTV,fg=placeholderFg)
    email.delete(0,END)
    email.insert(0,"Email  ")
    placeHolder(email,"Email  ")
    
    # Button
    signupButton = Button(sf,text="Signup",relief="flat",padx=18,bg=bg,fg="#FFA500",command=lambda username=siusername,ps=password,reps=rePassword,email=email: client.signupAccount(username.get(),ps.get(),reps.get(),email.get()))
    backButton = Button(sf,text="Back",relief="flat",padx=24,bg=bg,fg="#FFA500",command=lambda : changeFrame(sf,loginFrame()))
    # Padding
    # Spadlabel=Label(sf,bg=bg)
    # Adding into current frame
    title.grid(row=0,column=1)
    siusername.grid(row=1,column=0,columnspan=4,ipady=7,ipadx=30)
    password.grid(row=2,column=0,columnspan=4,pady=30,ipady=7,ipadx=30)
    rePassword.grid(row=3,column=0,columnspan=4,ipady=7,ipadx=30)
    email.grid(row=4,column=0,columnspan=4,pady=30,ipady=7,ipadx=30)
    signupButton.grid(row=5,column=1,columnspan=2)
    backButton.grid(row=6,column=1,columnspan=2,pady=30)
    # Spadlabel.grid(row=7,column=1,pady=20)
    # Adding current frame to root
    sf.pack(anchor="center",pady=100)

def homeScreen():
	nevFrame= Frame(client.root,bg=bg,bd=0,width=400,height=800,relief="solid")
	nevFrame.config(highlightcolor="#FFA500",highlightbackground="#FFA500",highlightthickness=3)

	chatFrame=Frame(client.root,bg=bg,bd=0,width=1000,height=800,relief="solid")
	chatFrame.config(highlightcolor="#FFA500",highlightbackground="#FFA500",highlightthickness=3)


	scrollbar = Scrollbar(nevFrame,bg='red',troughcolor="red")
	user_list = Listbox(nevFrame, height=60, width=30, yscrollcommand=scrollbar.set,bg='#333333')

	for line in range(1000):
		user_list.insert(END,"Number"+str(line))

	scrollbar.pack(side=RIGHT, fill=Y)
	scrollbar.config(command=user_list.yview)
	user_list.pack(side=LEFT, fill=BOTH)




	nevFrame.pack(side=LEFT)
	chatFrame.pack(side=LEFT,padx=30)



#for Place holder
def placeHolder(ent,plce="",s=''):
    #for placehokder text
    def putPlaceholder(ent):
    	if ent.get()==plce:
    		ent.delete(0,END)
    	else:
        	ent.config(show="")
        	ent.config(fg="gray")
        	ent.insert(0,plce)

    #if click the entry
    def focIn(*args):
        if ent.get()==plce:
            ent.delete(0,END)
            ent.config(fg="black")
            ent.config(show=s)
        

    #not click the entry
    def focOut(*args):
        if not ent.get():
            putPlaceholder(ent)
        
        

    ent.bind("<FocusIn>",focIn)
    ent.bind("<FocusOut>",focOut)
    



