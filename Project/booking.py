import sys
import cx_Oracle
import datetime
from array import array

#This class deals with the splash/login menu
class Booking:
	email = ""
	name = ""

	#This is the init file. A connection string is required to setup the class.
	def __init__(self, connectionString):
		self.connectionString = connectionString
	

	def cancelBooking(self):
		print("cancel Booking")
			
	
	def makeBooking(self):
		print("Making Booking")
		
	
	#String format for double from:
	#http://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
	def listExistingBookings(self,email):
			
		ticketNumber = self.listAllUserBookings(email)
		
		if (ticketNumber >0):
			self.viewBookingDetails(ticketNumber)
			
		
	
	
	def viewBookingDetails(self,ticketNumber):
	
		#	tno		int,
		#	flightno	char(6),
		#	fare		char(2),
		#	dep_date	date,
		#	seat		char(3),
		#query merges ticket and booking tables and retrives the tno, name, dep_date, paid_price
		query = "SELECT * FROM bookings WHERE tno=:ticketNum"
		
		
		#connect to SQL and execute query.
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(query, ticketNum=ticketNumber)
		rows = curs.fetchone()
		
		#if number of hits ==0: user has no bookings in the system
		if (curs.rowcount ==0):
			curs.close()
			connection.close()
			print("\nBooking no longer exists.")
			return 0
		
		else:
			#this prints a formated heading for the ticket info
			print("%s %s %s %s %s" % ("Ticket No".ljust(11), "Flight No".ljust(11), "Fare".ljust(6), "Depart Date".ljust(12), "Seat"))
			
			flightno = rows[1].ljust(11)
			fare = rows[2].ljust(6)
			departDate = rows[3]
			departDateStr = str(int(departDate.day)) + "-" + str(int(departDate.month)) + "-" + str(int(departDate.year))
			seat = rows[4]
			
			print("%s %s %s %s %s" %(str(ticketNumber).ljust(11), flightno.ljust(11), fare.ljust(6), departDateStr.ljust(12), seat))


		
	def listAllUserBookings(self,email):
		#query merges ticket and booking tables and retrives the tno, name, dep_date, paid_price
		query = "SELECT t.tno, t.name, b.dep_date, t.paid_price FROM tickets t, bookings b WHERE t.tno=b.tno AND TRIM(t.email)=:u_email"
		
				
		#an array of totalHits size to contain a list of all the ticket numbers
		ticketArray = array("i")
		#item number in booking list
		itemNum = 0
		
		#connect to SQL and execute query.
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(query, u_email=email)
		rows = curs.fetchone()
		
		#if number of hits ==0: user has no bookings in the system
		if (curs.rowcount ==0):
			curs.close()
			connection.close()
			print("\nUser has no previous bookings.")
			return 0
		
		else:
			#this prints a formated heading for the ticket info
			print("%s %s %s %s %s" % ("Item No".ljust(8),"Ticket No".ljust(11), "Name".ljust(22), "Depart Date".ljust(12), "Price"))
			
			while (rows):
				itemNum += 1
				ticketArray.append(self.extractPartialBookingDetails(itemNum,rows))
				rows = curs.fetchone()
				
			curs.close()
			connection.close()
			print("\nWould you like a booking?")
			userInput = self.verifyUInt("Please enter an item number or press 0 to return to the main menu.", len(ticketArray))
			if(userInput >0):
				return ticketArray[userInput-1]
			else:
				return 0
		
	
		
	def extractPartialBookingDetails(self, itemNum,item):	

		#Splits up
		ticketNum=int(item[0])
		name=item[1]
		departDate=item[2]
		price=item[3]
		
		#converts the depart date to a usable string
		departDateStr = str(int(departDate.day)) + "-" + str(int(departDate.month)) + "-" + str(int(departDate.year))
				
		#prints out the row
		print("%s %s %s %s %.2f" %(str(itemNum).ljust(8), str(ticketNum).ljust(11), name.ljust(22), departDateStr.ljust(12), price))
		
		return ticketNum
		
	
	def verifyUInt(self, message, maxSize):
		userInput= 0
		while (True):
			try:
				userInput = int(input(message));
				break
			except ValueError:
				print("\nInvalid option.")

		while((userInput < 0) or (userInput > maxSize)):
			print("\nInvalid option.")
			userInput = int(input(message));
			
		return userInput
			
