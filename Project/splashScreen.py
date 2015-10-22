import sys
import cx_Oracle

#This class deals with the splash/login menu
class SplashScreen:
	userVerified = False
	isAirlineAgent = False

	#This is the init file. A connection string is required to setup the class.
	def __init__(self, connectionString):
		self.connectionString = connectionString
	
	#This starts up the login/splash menu.
	#This finds out what the user wants to do and directs the flow of the program based on that option.
	#	The user has the option of typing in the activity(login,register,exit) or the corresponding number)
	#Return: TRUE if user is authenticated, FALSe if user is unauthenticated
	def start(self):
		#Repeat the process while user is unverified or input is invalid
		while(self.userVerified == False):
			#Introductory message
			print("Welcome to group 40's airline ticket system")
			userInput = input("Please select an option: \nLogin(1) \nRegister(2) \nExit(3) \nPlease Enter your selection:")
			
			#check if user wants to exit
			if((userInput.lower()=="3") or (userInput.lower()=="exit")):
				self.userVerified = True
				print("Thank you for using group 40's airline ticket system.")
				exit()
			
			#check if user wants to register
			elif((userInput.lower()=="2") or (userInput.lower()=="register")):
				self.userVerified = self.registerUser()
				
			#check if user wants to login	
			elif((userInput.lower()=="1") or (userInput.lower()=="login")):
				self.userVerified = self.userSignin()
			
			#if input is invalid, inform the user
			else:
				self.userVerified = False
				print("\ninvalid User Input. Please select a valid input.")
		
		#returns true if the user is authenticated
		return self.userVerified

	
	#This attempts to sign in the user.
	#Returns true if the user is signed in, false if the user signin failed
	#variables used in sql example from:
	#http://stackoverflow.com/questions/13650632/user-input-variables-in-cx-oracle
	def userSignin(self):
		#variables needed from user. Note, email is made into lowercase as all emails should be lowercase
		#password is CASE SENSITIVE
		self.email = input("Please enter your email address: ").lower()
		self.password = input("Please enter your password: ")
		
		#query retrives the user's password if email is vaild
		query = "SELECT pass FROM users WHERE TRIM(email)=:u_email"
		
		#connect to SQL and execute query.
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(query, u_email=self.email)
		rows = curs.fetchone()

		#if rowcount=0, no email was found and user does not exist in system.
		#in this case, close connections, alert the user and return false
		if (curs.rowcount ==0):
			curs.close()
			connection.close()
			print("Login failed. Invalid email or password.")
			return False
			
		#if rowcount =! 0, an email was found. 
		else:
			dbPassword = rows[0]
			curs.close()
			connection.close()				
		
			#if the database password and the user password match, notify user and return true.
			#also checks to see if the user is an Agent or not.
			if (dbPassword==self.password):
				print("Login Successful, Type logout at anytime to logout of your account.")
				self.checkIfAgent()
				return True
				
			#if the passwords do not match, notify user and return false	
			else:
				print("Login failed. Invalid email or password!.")
				return False
	
	
	
	#This checks to see if the user is an agent or not. It saves the result to a local variable (isAirlineAgent)
	def checkIfAgent(self):
	
		#query to see if the user email is in the airline_Agents database
		query = "SELECT email from airline_agents WHERE TRIM(email)=:userEmail"
		
		#SQL connection and query call
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(query, userEmail=self.email)
		rows = curs.fetchone()
		
		#If rowcount=0, the user is not an agent.
		if (curs.rowcount ==0):
			self.isAirlineAgent = False;
			
		#if rowcount != 0, the user is an agent.
		else:
			self.isAirlineAgent = True;
		curs.close()
		connection.close()			
	
	#this registers a user. 
	def registerUser(self):
		#required variables from user.
		#email is not case Senstive, Password is.
		self.email = input("Please enter an email address: ").lower()
		self.password = input("Please enter a 4 character password: ")
		
		#this flag checks to see if the entered value is invalid (db restrictions)
		invalidPass = True
		invalidEmail = True
		
		#checks to see if email is a valid lenght
		while(1):
			if (len(self.email)<=20):
				break
			else:
				self.email = input("Invalid email. Please enter an email address with a maximum lenght of 20 characters:").lower()
		
		#checks to see if password is a valid lenght.
		while(1):
			if (len(self.password)<=4):
				break
			else:
				self.password = input("Invalid Password. Please enter a password with a maximum lenght of 4 characters:")
				
		
		#2 queries
		#query: checks to see if email exists in system
		#insertquery: insert query for new user
		query = "SELECT email from users where TRIM(email)=:userEmail"
		insertquery = "INSERT into users(email, pass) values(:userEmail, :userPass)"
		
		#connection and initial query call
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(query, userEmail=self.email)
		rows = curs.fetchone()
		
		#if rowcount =0, email does not exist so add user
		if (curs.rowcount ==0):
			curs.execute(insertquery, userEmail=self.email, userPass=self.password)
			connection.commit()
			curs.close()
			connection.close()	
			print("Account created. Type logout at anytime to logout of your account.")
			return True
		
		#if rowcount != 0, email exists, process failed, return false.
		else:
			curs.close()
			connection.close()				
			print("Account could not be created. Email already exists in the system.")
			return False
			
	
	#this logs out the user and resets the variables
	def logOut(self):
		self.email = ""
		self.password = ""
		self.isAirlineAgent = False
		self.userVerified = False

	
	def getEmail(self):
		return self.email
		
	def getPassword(self):
		return self.password
		
	def isAgent(self):
		return self.isAirlineAgent
		
		
		
		
		
		
		
	
	
	
	
	
	
