import sys;
import cx_Oracle;
import test;
import splashScreen;
import booking;
import datetime
import time

class main:
	#Home
	#connectionString = "eorodrig/Lionheart1@localhost:1521/XE"
	#Lab
	#connectionString = "eorodrig/pass@gwynne.cs.ualberta.ca:1521/CRS"
	#this determines if the user is authenticated	
	email = ""
	password =""
	
	#This gets the main User Information.
	def getUserInfo(self,splashScreen):
		self.email = splashScreen.getEmail()
		self.password = splashScreen.getPassword()
		self.isAgent = splashScreen.isAgent()
		
	
    #this verifies that the menu input is an int, if it isn't it will prompt the user to retry
	def verifyMenuIsInt(self):
		if (self.isAgent):
			while (True):
				try:
					userInput = int(input("\nPlease Select one of the following options: \nSearch for Flights(1) \nMake a booking(2) \nList existing bookings(3) \nCancel a booking(4) \nRecord flight departure(5) \nRecord flight arrival(6) \nLogout(9) \nPlease Enter an option:"));
					break
				except ValueError:
					print("\nInvalid option, Please enter a valid number")
														
		else:
			while(True):
				try:
					userInput = int(input("\nPlease Select one of the following options: \nSearch for Flights(1) \nMake a booking(2) \nList existing bookings(3) \nCancel a booking(4) \nLogout(9) \nPlease Enter an option:"));
					break
				except ValueError:
					print("\nInvalid option, Please enter a valid number")
						
		return userInput				
	
	
	#this gets the menuInput from the user
	def getMenuInput(self):
		
		isUserMenuValid = False
		
		while(isUserMenuValid==False):

			userInput = self.verifyMenuIsInt()
			
			if ((userInput==1) or (userInput==2) or (userInput==3) or (userInput==4) or (userInput==9)):
				isUserMenuValid=True
			elif ((self.isAgent == True) and ((userInput==5) or (userInput==6) )):
				isUserMenuValid=True
			else:
				print("\nInvalid input, Please select a valid option.")
		
		return userInput
	
	#this processes the menu selection from the user
	def processMenuSelection(self, menuItem, splashScreen):
		if(menuItem ==1):
			print("\n1: Searching for flights")
			return True
		elif(menuItem ==2):
			book = booking.Booking(self.connectionString)
			book.makeBooking(self.email)
			return True
		elif(menuItem ==3):
			book = booking.Booking(self.connectionString)
			book.listExistingBookings(self.email)
			return True
		elif(menuItem ==4):
			book = booking.Booking(self.connectionString)
			book.cancelBooking(self.email)
			return True
		elif(menuItem ==5):
			print("5")
			return True
		elif(menuItem ==6):
			print("6")
			return True
		#LOUTOUT
		elif(menuItem ==9):
			print("\nThank you for using our airline ticket program "+self.email+".")
			self.logout(splashScreen)
			return False
	
	def logout(self,splashScreen):
		self.email=""
		self.password=""
		self.isAgent=False
		splashScreen.logout()
			
	#this starts the program
	def start(self):
		#this is the splashScreen object
		ss = splashScreen.SplashScreen(self.connectionString)
		
		#user is not authenticated by default
		isUserAuthenticated = False
		
		#while not authenticated, run the program.
		while (isUserAuthenticated == False):

			#gets the authentication from the splash screen
			isUserAuthenticated = ss.start()
			
			#if authenticated, show the menu and do some work
			while(isUserAuthenticated == True):
				
				#get the user information (email,pass,isAgent)
				self.getUserInfo(ss);
				
				#show the menu to the user and get their selection
				menuSelection = self.getMenuInput()
				
				#processes the item. 
				isUserAuthenticated = self.processMenuSelection(menuSelection, ss)
							
					

		
				

program = main()
dbUserName = sys.argv[1]
dbPassword = sys.argv[2]

program.connectionString = dbUserName + "/" +dbPassword + "@localhost:1521/XE"
program.start()				

			
	