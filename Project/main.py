import sys;
#import cx_Oracle;


class SplashScreen:
	email = "";
	password = "";
	loginTime = "";
	userVerified = False;

	def start(self):
		while(self.userVerified == False):
			print("Welcome to group 40's airline ticket system");
			userInput = raw_input("Please select an option: Login, Register, Exit:");
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
	

	def userSignin(self):
		self.email = raw_input("Please enter your email address: ");
		self.password = raw_input("Please enter your password: ");
		return True;
	
	
	

	def registerUser(self):
		self.email = raw_input("Please enter an email address: ");
		self.password = raw_input("Please enter a password: ");
		return True;

	def getEmail(self):
		return self.email;
		
	def getPassword(self):
		return self.password;
	
#class SearchForFlight:


#class Bookings:
	


##splash screen stuff
ss = SplashScreen();
ss.start();
email = ss.getEmail();
password = ss.getPassword();


print("email: " + email + " \npassword: " + password);
