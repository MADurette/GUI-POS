#Point Of Sale Project

#Marcus A Durette
#Skyler J Sheler
#Morgan A Hill
import datetime
import mysql.connector
import tkinter as tk
import os
import sys
import time
#To Do:
#Products list update for actual products
#error label dynamic changing
#balance dynamic changing 
#fix grid_size for return 
#move db for balance update to checkout button in checkout screen

class LoginWindow:
		def __init__(self, window):
				#So user knows can press ESC to exit... Can put into exit button as well for ease
				#esclab = tk.Label(text="Press <ESC> to exit").grid(row=4,column = 1)
				#Sets up login label
				errorans=""
				#print(root.grid_size())
				#print(root.grid_slaves())
				emaillabel = tk.Label(root, text = "Username")
				emaillabel.config(font=("New Times Roman", 20))
				emaillabel.grid(row = 1, column = 1)

				#Sets up Email Entry
				emailentry = tk.Entry(root)
				emailentry.config(width=50)
				emailentry.grid(row = 2, column = 1)

				#Sets up Password Label
				passwordlabel = tk.Label(root, text = "Password")
				passwordlabel.config(font=("New Times Roman",20))
				passwordlabel.grid(row = 3, column = 1)
                
				#Sets up Password Entry
				passwordentry = tk.Entry(root,show="*")
				passwordentry.config(width=50)
				passwordentry.grid(row = 4, column = 1)

				space = tk.Label(root, text = "")
				space.config(font=("New Times Roman",20))
				space.grid(row = 5, column = 1)

				#Submit Button
				submitbtn = tk.Button(root, text="Submit")
				submitbtn.grid(row=6,column = 1)

				errormessage = tk.Label(root,text="{}".format(errorans))
				errormessage.config(font=("New Times Roman",12),fg='#ff0000')
				errormessage.grid(row=8,column=1)
				Exit = tk.Button(root, text="Exit", command=root.destroy)
				Exit.grid(column = 1,row =10)
				
				#Configures row and column weight to fit it into fullscreen better instead of top left of window
				root.rowconfigure(0, weight=1)
				root.columnconfigure(0, weight=2)
				root.rowconfigure(8, weight=1)
				root.columnconfigure(8, weight=2)

				def submitpressed(event):#When submit is hit checks then move to next screen
					usernameentered = emailentry.get()
					passwordentered = passwordentry.get()
					mydb = mysql.connector.connect(host="localhost",user="root",passwd="Ecodeath2",database="users")
					mycursor = mydb.cursor()
					mycursor.execute("SELECT * FROM users where User = '%s'" % usernameentered)
					myresult = mycursor.fetchall()
					#checks the database for a user. this will check if the name and the password matches the database
					#if they dont and error message occurs.
					for x in myresult:
						if(usernameentered in x and passwordentered in x):
							emailentry.destroy()
							emaillabel.destroy()
							passwordentry.destroy()
							passwordlabel.destroy()
							submitbtn.destroy()
							errormessage.destroy()
							Exit.destroy()
							mydb.close()
							CreatePOS(root, sqlresult,usernameentered,x[0],x[3])
						else:
							errorans="Invalid Credentials"
							errormessage.config(text="{}".format(errorans))
				Exit.bind('<Button>',exit)
				submitbtn.bind('<Button>',submitpressed)     
class CreatePOS:
	total_balance_due =0.0
	temp = 0.0
	sessionIDGlobal =0
	def __init__ (self, screen, sqlresult,username,sessionID,balance):
		global total_balance_due
		global temp
		global sessionIDGlobal
		sessionIDGlobal  = sessionID
		self.frame = tk.Frame(screen)
		self.frame.grid()
		self.buttons = {}
		self.sessionID = sessionID
		total_balance_due =0
		balanceamt = balance #to change with added amounts for buttons
		for i,row in enumerate(sqlresult):
			buttonImage = row[2]
			buttonId = row[1]
			price = row[0]
			button = tk.Button(#Issue fix from here
			self.frame,
			text = str(buttonImage)+"\n$"+str(price),
			#image = buttonImage
			height = 10,
			width = 20
			)
			button['command'] = self.createButtonCommand(buttonId, row[0],row[2])
			self.buttons[buttonId] = button
			#counting up to grid)
			button.grid(row = i//5, column = i%5)
		accntlabel = tk.Label(root,text="Welcome, {} UserID = {}".format(username,sessionID))
		balance = tk.Label(root, text="Ad\nSpace",relief="groove")
		checkout = tk.Button(root, text="Checkout", command=root.destroy)
		accntlabel.config(font=("New Times Roman",12))
		balance.config(font=("New Times Roman",34))
		checkout.config(width=20,height=3)
		
		
		accntlabel.grid(column=12,row=0,sticky="NE")
		balance.grid(column=12,row = 1,columnspan=6,rowspan=6)
		checkout.grid(column = 12,row = 9)
		root.columnconfigure(12, weight=1)
		root.rowconfigure(9, weight=1)
		
		
		def checkoutpressed(event):
			#updates the users balance with the total that was collected from each item and adds it to the balance
			#Commits the changes to the database
			global total_balance_due
			global sessionIDGlobal
			for all,row in enumerate(sqlresult):
				buttonId = row[1]
				self.buttons[buttonId].destroy()
			accntlabel.destroy()
			balance.destroy()
			checkout.destroy()
			self.frame.destroy()
			print("Total Owed is: {}".format(total_balance_due))
			Checkoutscreen(root,total_balance_due)
		checkout.bind('<Button>',checkoutpressed)
	def createButtonCommand(self, buttonId, buttonArg, buttondisc):
		def command():
			self.buttonActivate(buttonId, buttonArg, buttondisc)
		return command
	#Keeps track of the item price sends it to a global total that keepds track of all pressed buttons 
	def buttonActivate(self, buttonId, buttonArg, buttondisc):
		global sessionIDGlobal
		global total_balance_due
		total_balance_due+= buttonArg
		button = self.buttons.get(buttonId)
		if not button: return
		button.configure(state = tk.DISABLED)
		print("{}".format(str(buttondisc)))
	
                
class Checkoutscreen:
	def __init__ (self, screen, balance):
		#random widget open so to fix this used below code
		issuefix = root.grid_slaves()
		issuefix[0].destroy()
		#print(root.grid_slaves()) #to find the widgets connected
		self.frame = tk.Frame(screen)
		self.frame.grid()
		
		fnamelabel=tk.Label(root, text = "First Name:")
		fnameentry=tk.Entry(root)
		fnameentry.config(width=50)

		lnamelabel=tk.Label(root, text = "Last Name:")
		lnameentry=tk.Entry(root)
		lnameentry.config(width=50)
		
		addressonelabel=tk.Label(root, text = "Address:")
		addressoneentry=tk.Entry(root)
		addressoneentry.config(width=50)

		addresstwolabel=tk.Label(root, text = "Address(cont):")
		addresstwoentry=tk.Entry(root)
		addresstwoentry.config(width=50)

		cardnumlabel=tk.Label(root, text = "Card Number:")
		cardnumentry=tk.Entry(root)
		cardnumentry.config(width=50)

		expdatelabel=tk.Label(root, text = "Expiration Date:")
		expdateentry=tk.Entry(root)
		expdateentry.config(width=50)

		cardseclabel=tk.Label(root, text = "Security Code:")
		cardsecentry=tk.Entry(root)
		cardsecentry.config(width=50)
		
		ziplabel=tk.Label(root, text = "Zip:")
		zipentry=tk.Entry(root)
		zipentry.config(width=50)

		phonelabel=tk.Label(root, text = "Phone Number:")
		phoneentry=tk.Entry(root)
		phoneentry.config(width=50)

		emaillabel=tk.Label(root, text = "Email:")
		emailentry=tk.Entry(root)
		emailentry.config(width=50)

		fnamelabel.grid(row = 1, column = 2)
		fnameentry.grid(row = 2, column = 2)
		lnamelabel.grid(row = 3, column = 2)
		lnameentry.grid(row = 4, column = 2)
		addressonelabel.grid(row = 5, column = 2)
		addressoneentry.grid(row = 6, column = 2)
		addresstwolabel.grid(row = 7, column = 2)
		addresstwoentry.grid(row = 8, column = 2)
		ziplabel.grid(row = 9, column = 1)
		phonelabel.grid(row = 9, column = 3)
		zipentry.grid(row = 10, column = 1)
		phoneentry.grid(row = 10, column = 3)
		cardnumlabel.grid(row = 11, column = 2)
		cardnumentry.grid(row = 12, column = 2)
		expdatelabel.grid(row = 13, column = 1)
		expdateentry.grid(row = 14, column = 1)
		cardseclabel.grid(row = 13, column = 3)
		cardsecentry.grid(row = 14, column = 3)
		emaillabel.grid(row = 15, column = 2)
		emailentry.grid(row = 16, column = 2)

		submitbtn = tk.Button(root, text="Submit")
		submitbtn.grid(row=21,column = 2)
		
		root.rowconfigure(0, weight=1)
		root.columnconfigure(0, weight=3)
		root.rowconfigure(7,weight=0)
		root.rowconfigure(8,weight=0)
		root.rowconfigure(9,weight=0)
		root.rowconfigure(20, weight=3)
		root.rowconfigure(22, weight=2)
		root.columnconfigure(4, weight=1)
		def submitpressed(event):
			entfname = fnameentry.get()
			entlname = lnameentry.get()
			entaddone = addressoneentry.get()
			entaddtwo = addresstwoentry.get()
			entcardnum = cardnumentry.get()
			entexpdate = expdateentry.get()
			entcardsec = cardsecentry.get()
			entzip = zipentry.get()
			entphone = phoneentry.get()
			entemail = emailentry.get()
			
			good = 0
			while(good==0):
				try:
					#All answers correct
					if(len(entphone)!=10):
						good = 0
						break
					if(len(entcardnum)!=16):
						good = 0
						break
					if(len(entcardsec)!=3):
						good = 0
						break
					if(len(entzip)<5 or len(entzip)>5):
						good = 0
						break
					if(len(entaddone)==0):
						good = 0
						break
					dateob = datetime.datetime.strptime(entexpdate, "%m/%d/%Y")
					good = 1
				except:
					#not valid answers
					good = 0
			if(good == 0):
				print("\n---Error with Card information---\n")
			else:
				print("\n\n---Card Approved---\n\n")
				print("Card Number(no space):", entcardnum)
				print("Expiration Date (MM/DD/YYYY):", entexpdate)
				print("Security Number:", entcardsec)
				print("First Name:", entfname)
				print("Last Name:", entlname)
				print("Address (Line 1):", entaddone)
				print("Address (Line 2):", entaddtwo)
				print("Zip Code:", entzip)
				print("Phone Number (xxxxxxxxxx):", entphone)
				print("Email:", entemail)
				
				mydb = mysql.connector.connect(host="localhost",user="root",passwd="Ecodeath2",database="users")
				mycursor = mydb.cursor()
				mycursor.execute("Update users set balance =balance+ %d where idusers  =%d" % (total_balance_due,sessionIDGlobal))
				mydb.commit()
				mydb.close()
				
				fnameentry.destroy()
				fnamelabel.destroy()
				lnameentry.destroy()
				lnamelabel.destroy()
				addressoneentry.destroy()
				addressonelabel.destroy()
				addresstwoentry.destroy()
				addresstwolabel.destroy()
				cardnumentry.destroy()
				cardnumlabel.destroy()
				cardsecentry.destroy()
				cardseclabel.destroy()
				emailentry.destroy()
				emaillabel.destroy()
				phoneentry.destroy()
				phonelabel.destroy()
				zipentry.destroy()
				ziplabel.destroy()
				expdateentry.destroy()
				expdatelabel.destroy()
				submitbtn.destroy()
				self.frame.destroy()
				restart_program()
				

		submitbtn.bind('<Button>',submitpressed)
		
#To Exit Program
def exit(event):
	print("\nProgram Exited")
	time.sleep(.001)
	root.quit()
def restart_program():
	"""Restarts the current program.
	Note: this function does not return. Any cleanup action (like
	saving data) must be done before calling this function."""
	python = sys.executable
	os.execl(python, python, * sys.argv)
	root = tk.Tk()
#def enter(event):
	#root.quit()

# for sql results for buttons
sqlresult = [(1.25,1,'Candy Bar',1),(0.80,6,'Generic Fruit',0),(1.00,11,'Water',1),(1.25,16,'Soda Pop',0),(1.25,21,'Generic Candy',1),(1,26,'Chips',0),(1.25,31,'Salami Sticks',1),(1,36,'Dog Treat',0),(1.50,41,'Hotdog',1),(250,46,'A Cheap Date',0),(1.50,51,'Hamburger',1),(2.5,56,'Nachos',0),(0,61,'Horrid Customer Service',1),(1.00,66,'Okay Customer Service',0),(3.00,71,'Great Customer Service',1)]
root = tk.Tk()
root.overrideredirect(False)

#Set to fullscreen
root.attributes('-fullscreen',True)

#Binding key to the exit event
root.bind("<Escape>", exit)
#root.bind("<Return>", enter)
                
login = LoginWindow(root)

#runs window until exit is performed
root.mainloop()
