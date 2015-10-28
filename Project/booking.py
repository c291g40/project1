import sys
import cx_Oracle
import datetime
from array import array
import random

#This class deals with the splash/login menu
class Booking:
	email = ""
	name = ""

	#This is the init file. A connection string is required to setup the class.
	def __init__(self, connectionString):
		self.connectionString = connectionString
	

	def cancelBooking(self,email):
		#query merges ticket and booking tables and retrives the tno, name, dep_date, paid_price WHERE t.tno=b.tno
		query = "SELECT t.tno, t.name, b.dep_date, t.paid_price FROM tickets t, bookings b WHERE t.tno=b.tno and TRIM(t.email)=:u_email"
		
				
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
			print("\n%s %s %s %s %s" % ("Item No".ljust(8),"Ticket No".ljust(11), "Name".ljust(22), "Depart Date".ljust(12), "Price"))
			
			while (rows):
				itemNum += 1
				ticketArray.append(self.extractPartialBookingDetails(itemNum,rows))
				rows = curs.fetchone()
				
			curs.close()
			connection.close()

			userInput = self.verifyUInt("\nPlease enter an item number or press 0 to return to the main menu:", len(ticketArray))
			if(userInput >0):
				self.cancelTicketBooking(ticketArray[userInput-1])

		
	def cancelTicketBooking(self,ticketNo):
		#this is the query to see if a user exists in the passenger's table
		bookingQuery = "DELETE FROM bookings WHERE TRIM(tno)=:u_ticketNo"
		ticketQuery = "DELETE FROM tickets WHERE TRIM(tno)=:u_ticketNo"
		
		
		#connect to SQL and execute query.
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(bookingQuery, u_ticketNo=ticketNo)
		curs.execute(ticketQuery, u_ticketNo=ticketNo)
		connection.commit()
		curs.close()
		connection.close()
		
		print("Successfully Deleted booking:%s" % ticketNo)
			

	def makeBooking(self,email):
		if(self.is2WayFlight()):
			self.book2Way(email)
		else:
			self.book1Way(email)
		
		

		
	
		
	#checks to see if the flight is a two way flight (TRUE) or 1 way (FALSE)
	def is2WayFlight(self): 
		isTwoWay=False
		flightType = ""
		while(1):
			flightType = input("\nWould you like to Book a return trip?").lower()
			
			if ((flightType=="yes") or (flightType=="y")):
				isTwoWay=True
				break
				
			elif((flightType=="no") or (flightType=="n")):
				isTwoWay=False
				break
			else:
				print ("Invalid Input. Please enter Yes(y) or No (n)")
		return isTwoWay
		
	#books a 1 way ticket with pre-defined items selected
	def book1WayFromSelection(self, email, flightNo, depDate, fareType):
		#departure = input("Please input the depature date (DD-MM-YYYY):")
		#depDate = datetime.datetime(int(departure[6:10]), int(departure[3:5]), int(departure[0:2]))
		userName = input("Please input the name of the passenger:")
		country = ""
		
		#checks to see if a user is in the passenger list
		if(self.isUserAPassenger(userName,email)==False):
			country = input("\nPassenger is not found. Please input the passenger's country of residence:")
		
		self.bookFlight(userName,email, flightNo, fareType, depDate,country)
		
		
		
	def book2WayFromSelection(self, email, FlightNo1, depDate1, fare1,FlightNo2, depDate2, fare2):
		userName = input("Please input the name of the passenger:")
		country = ""
		
		#checks to see if a user is in the passenger list
		if(self.isUserAPassenger(userName,email)==False):
			country = input("\nPassenger is not found. Please input the passenger's country of residence:")
		
		self.book2WayFlight(userName,email,country, flightNo1, fare1, depDate1,flightNo2, fare2, depDate2)
	



	
	#insert into sch_flights values ('AC029',to_date('23-Oct-2015','DD-Mon-YYYY'),to_date('22:45', 'hh24:mi'),to_date('02:05','hh24:mi'));
	def book1Way(self, email):
		flightNo = input("\nPlease input the flight number:")
		fareType = input("Please input the fare type:")
		departure = input("Please input the depature date (DD-MM-YYYY):")
		depDate = datetime.datetime(int(departure[6:10]), int(departure[3:5]), int(departure[0:2]))
		userName = input("\nPlease input the name of the passenger:")
		country=""
		
		#checks to see if a user is in the passenger list
		if(self.isUserAPassenger(userName,email)==False):
			country = input("\nPassenger is not found. Please input the passenger's country of residence:")
		
		self.bookFlight(userName,email, flightNo, fareType, depDate,country)
		
	def book2Way(self, email):
		flightNo = input("\nPlease input the flight number for your destination flight:")
		fareType = input("Please input the fare type for your destination flight:")
		departure = input("Please input the depature date for your destination flight(DD-MM-YYYY):")
		depDate = datetime.datetime(int(departure[6:10]), int(departure[3:5]), int(departure[0:2]))
		flightNo2 = input("\nPlease input the flight number for your return flight:")
		fareType2 = input("Please input the fare type for your return flight:")
		departure2 = input("Please input the depature date for your return flight(DD-MM-YYYY):")
		depDate2 = datetime.datetime(int(departure2[6:10]), int(departure2[3:5]), int(departure2[0:2]))
		userName = input("\nPlease input the name of the passenger:")
		country="" ""
		
		#checks to see if a user is in the passenger list
		if(self.isUserAPassenger(userName,email)==False):
			country = input("\nPassenger is not found. Please input the passenger's country of residence:")
		
		self.book2WayFlight(userName,email,country, flightNo, fareType, depDate,flightNo2, fareType2, depDate2)
	
	def book2WayFlight(self, userName,email,country, flightNo1, fareType1, depDate1,flightNo2, fareType2, depDate2):
		isDestinationFlightAvailable = False
		isReturnFlightAvailable = False
		price1 =0
		price2 =0
		#this searches for the price of a ticket. if the booking is still available in that fare it will return a price, else nothing.
		searchQuery = "SELECT price FROM flight_fares WHERE Trim(flightno)=:u_flightno and Trim(fare)=:u_fare and limit > ALL (SELECT count(*) from bookings where TRIM(flightno)=:u_flightno and TRIM(fare)=:u_fare and dep_Date=:u_date)"

		#update table queries
		UpdateTicketsQuery = "INSERT INTO tickets VALUES(:u_ticketNum, :u_name, :u_email, :u_price)"
		UpdateBookingsQuery = "INSERT INTO bookings VALUES (:u_ticketNum, :u_flightno, :u_fare, :u_depDate, null)"
		
		#connection and launch of search
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		
		#search for destination flight:
		curs.execute(searchQuery,u_fare=fareType1, u_date=depDate1, u_flightno=flightNo1)
		rows = curs.fetchone()
		if(curs.rowcount >0):
			isDestinationFlightAvailable=True
			price1 =rows[0]

		#search for return flight:
		curs.execute(searchQuery,u_fare=fareType2, u_date=depDate2, u_flightno=flightNo2)
		rows = curs.fetchone()
		if(curs.rowcount >0):
			isReturnFlightAvailable=True
			price2 =rows[0]
		
		#If seat is available at selected fare, update tables and commits
		if ((isDestinationFlightAvailable) and (isReturnFlightAvailable)):
			price = price1 + price2
			ticketNum = self.getTicketNum(curs)
			if(self.isUserAPassenger(userName,email)==False):
				self.addUserToPassengerList(userName,email,country)
			curs.execute(UpdateTicketsQuery,u_ticketNum = ticketNum, u_name=userName, u_email=email, u_price = price)
			curs.execute(UpdateBookingsQuery,u_ticketNum = ticketNum, u_flightno=flightNo1, u_fare=fareType1, u_depDate=depDate1)
			curs.execute(UpdateBookingsQuery,u_ticketNum = ticketNum, u_flightno=flightNo2, u_fare=fareType2, u_depDate=depDate2)
			connection.commit()
			print("\nThank for booking your flight with us %s. Your Ticket Number is %s" %(userName, ticketNum))
		#if one of the tickets are sold out
		elif((isDestinationFlightAvailable) and (isReturnFlightAvailable==False)):
			print("We were unable to book your flight. The seats in the requested fare are sold out for your return flight.")
		elif((isDestinationFlightAvailable==False) and (isReturnFlightAvailable)):
			print("We were unable to book your flight. The seats in the requested fare are sold out for your destination flight.")
		#if tickets sold out.
		else:
			print("We were unable to book your flight. The seats in the requested fare are sold out.")
		curs.close()
		connection.close()
	
	#This books a flight
	def bookFlight(self, userName,email, flightNo, fareType, depDate,country):
		#this searches for the price of a ticket. if the booking is still available in that fare it will return a price, else nothing.
		searchQuery = "SELECT price FROM flight_fares WHERE Trim(flightno)=:u_flightno and Trim(fare)=:u_fare and limit > ALL (SELECT count(*) from bookings where TRIM(flightno)=:u_flightno and TRIM(fare)=:u_fare and dep_Date=:u_date)"

		#update table queries
		UpdateTicketsQuery = "INSERT INTO tickets VALUES(:u_ticketNum, :u_name, :u_email, :u_price)"
		UpdateBookingsQuery = "INSERT INTO bookings VALUES (:u_ticketNum, :u_flightno, :u_fare, :u_depDate, null)"
		
		#connection and launch of search
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(searchQuery, u_fare=fareType, u_date=depDate, u_flightno=flightNo)

		rows = curs.fetchone()
		print(rows)
		
		#If seat is available at selected fare, update tables and commits
		if (curs.rowcount>0):
			price = rows[0]
			ticketNum = self.getTicketNum(curs)
			if(self.isUserAPassenger(userName,email)==False):
				self.addUserToPassengerList(userName,email,country)
			curs.execute(UpdateTicketsQuery,u_ticketNum = ticketNum, u_name=userName, u_email=email, u_price = price)
			curs.execute(UpdateBookingsQuery,u_ticketNum = ticketNum, u_flightno=flightNo, u_fare=fareType, u_depDate=depDate)
			connection.commit()
			print("\nThank for booking your flight with us %s. Your Ticket Number is %s" %(userName, ticketNum))
		#if tickets sold out.
		else:
			print("\nWe were unable to book your flight. The seats in the requested fare are sold out.")
		curs.close()
		connection.close()
	
	#this gets a unique ticket number
	def getTicketNum(self,curs):
		ticketNum=random.randint(0, 1000000)
		while(1):
			curs.execute("Select count(*) FROM tickets where tno=:u_ticketNo",u_ticketNo=ticketNum )
			if(curs.rowcount==0):
				break
			ticketNum=random.randint(0, 1000000)
		return ticketNum
	
	
	
	
	#checks to see if a user has been a passenger. 
	def isUserAPassenger(self,name,email):
		#this is the query to see if a user exists in the passenger's table
		query = "SELECT * FROM passengers WHERE TRIM(email)=:u_email and TRIM(name)=:u_name"
		
		#connect to SQL and execute query.
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(query, u_name=name, u_email=email)
		rows = curs.fetchone()
		
		#if number of hits ==0: user does not exit
		if (curs.rowcount ==0):
			curs.close()
			connection.close()
			return False
		else:
			return True
		
		
		
	def addUserToPassengerList(self,name,email,country):
		#this is the query to see if a user exists in the passenger's table
		query = "INSERT INTO  passengers VALUES(:u_email, :u_name, :u_Country)"
		
		
		#connect to SQL and execute query.
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		curs.execute(query, u_name=name, u_email=email, u_country=country)
		connection.commit()
		curs.close()
		connection.close()

	
	#String format for double from:
	#http://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
	def listExistingBookings(self,email):

		
		ItemNum = self.listAllUserBookings(email)
		while(ItemNum>0):
			ItemNum = self.listAllUserBookings(email)

	
	def viewBookingDetails(self,ticketNumber):
		#this is the query to view the full details of a specific booking
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
			print("\n%s %s %s %s %s" % ("Ticket No".ljust(11), "Flight No".ljust(11), "Fare".ljust(6), "Depart Date".ljust(12), "Seat"))
		
			#formats data
			flightno = rows[1].ljust(11)
			fare = rows[2].ljust(6)
			departDate = rows[3]
			departDateStr = str(int(departDate.day)) + "-" + str(int(departDate.month)) + "-" + str(int(departDate.year))
			seat = rows[4]
			
			#prints it
			print("%s %s %s %s %s" %(str(ticketNumber).ljust(11), flightno.ljust(11), fare.ljust(6), departDateStr.ljust(12), seat))


		
	def listAllUserBookings(self,email):
		#query merges ticket and booking tables and retrives the tno, name, dep_date, paid_price WHERE t.tno=b.tno
		query = "SELECT t.tno, t.name, b.dep_date, t.paid_price FROM tickets t, bookings b WHERE t.tno=b.tno and TRIM(t.email)=:u_email"
		
				
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
			print("\n%s %s %s %s %s" % ("Item No".ljust(8),"Ticket No".ljust(11), "Name".ljust(22), "Depart Date".ljust(12), "Price"))
			
			while (rows):
				itemNum += 1
				ticketArray.append(self.extractPartialBookingDetails(itemNum,rows))
				rows = curs.fetchone()
				
			curs.close()
			connection.close()
			userAction = input("\nWould you like to view a booking(v), cancel a booking(c) or return to the previous menu(q) :")
			if(userAction=='q' or userAction=='Q'):
				return 0
			else:
				userInput = self.verifyUInt("Please enter an item number or press 0 to return to the main menu.", len(ticketArray))
				if((userInput >0) and (userAction=='v' or userAction=='V')):
					self.viewBookingDetails(ticketArray[userInput-1])
					return 1
				elif((userInput >0) and (userAction=='c' or userAction=='C')):
					self.cancelTicketBooking(ticketArray[userInput-1])
					return 1
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
		
	
	#this verifies that a user input is an int between 0 and Max Size.
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
			

	#this is for selection from a list. This will not commit and thus keeps with specs		
	def bookAFlight(self,userName, email,flightNo, depDate, fareType, curs ):
		#this searches for the price of a ticket. if the booking is still available in that fare it will return a price, else nothing.
		searchQuery = "SELECT price FROM flight_fares WHERE Trim(flightno)=:u_flightno and Trim(fare)=:u_fare and limit > ALL (SELECT count(*) from bookings where TRIM(flightno)=:u_flightno and TRIM(fare)=:u_fare and dep_Date=:u_date)"

		#update table queries
		UpdateTicketsQuery = "INSERT INTO tickets VALUES(:u_ticketNum, :u_name, :u_email, :u_price)"
		UpdateBookingsQuery = "INSERT INTO bookings VALUES (:u_ticketNum, :u_flightno, :u_fare, :u_depDate, null)"
		
		#connection and launch of search
		curs.execute(searchQuery, u_fare=fareType,u_depDate=depDate, u_flightno=flightNo)
		rows = curs.fetchone()
		
		#If seat is available at selected fare, update tables and commits
		if (curs.rowcount>0):
			price = rows[0]
			ticketNum = self.getTicketNum(curs)	
			curs.execute(UpdateTicketsQuery,u_ticketNum = ticketNum, u_name=userName, u_email=email, u_price = price)
			curs.execute(UpdateBookingsQuery,u_ticketNum = ticketNum, u_flightno=flightNo, u_fare=fareType, u_depDate=depDate)
			print("\nFLight number %s has been booked. Your Ticket Number is %s" %(flightNo,ticketNum))
			return 1
		#if tickets sold out.
		else:
			print("\nWe were unable to book your flight. The seats in the requested fare are sold out for flight %s." %flightNo)
			return 0		
	
	def bookFromSearchResults(self,email,flightsList):		
		flightStatus = 1
		
		userName = input("Please input the name of the passenger:")
		country = ""
		
		#checks to see if a user is in the passenger list,if not a passenger it will add it to the database
		if(self.isUserAPassenger(userName,email)==False):
			country = input("\nPassenger is not found. Please input the passenger's country of residence:")
			self.addUserToPassengerList(userName, email, country)
		
		#connect to SQL and execute query.
		connection = cx_Oracle.connect(self.connectionString)
		curs = connection.cursor()
		
		#Do some stuff here  (Maybe a while or for loop with different arrays for flightNo, depDate, and fareType?. Break once flightStatus is False)
		for flight in flightsList:
			flightNo = flight[0]
			depDate = datetime.datetime(int(flight[1][6:10]), int(flight[1][3:5]), int(flight[1][0:2]))
			fareType = flight[2]
			flightStatus = flightStatus * self.bookAFlight(userName, email, flightNo, depDate, fareType, curs)
		
		if (flightStatus == 1):
			connection.commit()
		curs.close()
		connection.close()
		
