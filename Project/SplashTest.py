import sys;
import cx_Oracle;
import test;
import splashScreen;

##splash screen stuff

	#Home
connectionString = "eorodrig/Lionheart1@localhost:1521/XE"
	#Lab
	#connectionString = "eorodrig/pass@gwynne.cs.ualberta.ca:1521/CRS"
ss = splashScreen.SplashScreen(connectionString);
ss.start();


#while(authenticated == True):
email = ss.getEmail();
password = ss.getPassword();
isAgent = ss.isAgent();
	
if(isAgent):
	print("hello agent")
else:
	print("hello user")
