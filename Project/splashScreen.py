import sys;
import cx_Oracle;

class SplashScreen:
	email = "";
	password = "";
	logoutTime = "";
	userVerified = False;
	isAgent = False;

	def start(self):
		while(self.userVerified == False):
			print("Welcome to group 40's airline ticket system");
			userInput = input("Please select an option: Login, Register, Exit:");
			if(userInput.lower()=="exit"):
				self.userVerified = True;
				exit();
			elif(userInput.lower()=="register"):
				self.userVerified = self.registerUser();
				
			elif(userInput.lower()=="login"):
				self.userVerified = self.userSignin();
				
			else:
				self.userVerified = False;
				print("\ninvalid User Input. Please select a valid input.");
		return self.userVerified;

	

	def userSignin(self):
		self.email = input("Please enter your email address: ");
		self.password = input("Please enter your password: ");
		
		print("Login Successful, Type logout at anytime to logout of your account.");
		return True;
	
	
	

	def registerUser(self):
		self.email = input("Please enter an email address: ");
		self.password = input("Please enter a password: ");
		
		print("Account created. Type logout at anytime to logout of your account.");
		return True;

	def getEmail(self):
		return self.email;
		
	def getPassword(self):
		return self.password;
	
	def logOut(self):
		self.userVerified = False;
		
	def isAgent(self):
		return self.isAgent;
