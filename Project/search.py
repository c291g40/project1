# Mustafa Abbasi
# This function searches for available flights
import cx_Oracle
import datetime
import sys

# Gets user to enter valid date using datetime. 
def getDate (dateType):
    validInput = False
    while not(validInput):
        flightDate = input("Enter the %s date as DD-MM-YYYY: " %(dateType)).strip()
        try:
            day = int(flightDate[0:2])
            month = int(flightDate[3:5])
            year = int(flightDate[6:])
            datetime.datetime(year, month, day)
        except:
            print("Invalid input for date. Please try again.")
        else:
            validInput = True
            return(flightDate)

# Checks if the acode provided is valid/ exists in DB.
def validAirport (acode, connectionString):
    try:
        acode = acode.upper()
        acodeList = []
        matchList = []
        validAirport = False

        # connect to database
        connection = cx_Oracle.connect(connectionString)
        curs = connection.cursor()

        # get list of airports
        curs.execute("SELECT UPPER(acode) FROM airports")
        for row in curs:
            acodeList.append(row[0])
        
        # if airport exists return code
        if acode in acodeList:
            validAirport = True
        
        if not(validAirport):
            # get list of matching airports' name, city
            curs.execute("SELECT UPPER(acode),UPPER(name),UPPER(city) FROM airports")
            for row in curs:
                if acode in row[1] or acode in row[2]:
                    temp = [row[0], row[1], row[2]]
                    matchList.append(temp)
        
            # get user to select a matching airport
            validInput = False
            print("ACODE".ljust(4),"Airport".ljust(31),"City".ljust(16))
            for match in matchList:
                print(match[0].ljust(4),match[1].ljust(31),match[2].ljust(16))
            while not(validInput):
                print("\nThese airports matched your entry.")
                airport = input("Please type an ACODE from the above list: ")
                airport = airport.upper()
                if airport in [match[0] for match in matchList]:
                    validInput = True
                    acode = airport
             
        # close the connection
        curs.close
        connection.close()

        # return the airport code
        return(acode)
    
    # error catching sourced from cx_Oracle tutorial
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)

# Searches for direct flights between src and dst on dep_date.
def searchDirectFlights (src, dst, dep_date,connectionString):
    flightsList = []
    i = 0
    try:
        # connect to database
        connection = cx_Oracle.connect(connectionString)
        curs = connection.cursor()
        
        # using modified solution from assignment 2
        # get list of direct flights
        curs.execute("SELECT trim(f.flightno), f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, fa.price, fa.limit-count(tno), trim(TO_CHAR(sf.dep_date, 'DD-MM-YYYY')), trim(fa.fare) FROM flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2 WHERE f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and sf.dep_date=b.dep_date(+) and f.src ='"+src+"' and f.dst='"+dst+"' and to_char(sf.dep_date,'DD-MM-YYYY')='"+dep_date+"' GROUP BY f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, fa.price having fa.limit-count(tno) > 0")
        
        # add each flight and attributes to a list 
        for row in curs:
            flightsList.append([ [] for i in range(11)])
            flightsList[i][0] = row[0]
            flightsList[i][1] = row[1]
            flightsList[i][2] = row[2]
            flightsList[i][3] = row[3]
            flightsList[i][4] = row[4]
            flightsList[i][5] = "0"
            flightsList[i][6] = "N/A"
            flightsList[i][7] = row[5]
            flightsList[i][8] = row[6]
            flightsList[i][9] = row[7]
            flightsList[i][10] = row[8]
            i += 1
        
        # close the connection
        curs.close
        connection.close()
        
        # returns the flight list for display
        return(flightsList)
    
    # error catching sourced from cx_Oracle tutorial
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)
    
# Searches for connection flights between src and dst on dep_date.
def searchConnectFlights (src, dst, dep_date,connectionString):
    nameList = []
    flightsList = []
    i = 0
    try:
        # connect to database
        connection = cx_Oracle.connect(connectionString)
        curs = connection.cursor()
        
        # gets list of flights with one connection from src to dst on dep_date
        curs.execute("select s1.flightno, s2.flightno, to_char(s1.dep_date,'DD-MM-YYYY'), to_char(s2.dep_date,'DD-MM-YYYY') from sch_flights s1, sch_flights s2, flights f1, flights f2, airports a1, airports a2 where f1.src=a1.acode and f1.dst=a2.acode and s1.flightno = f1.flightno and s2.flightno = f2.flightno and f1.dst=f2.src and f1.src ='"+src+"' and f2.dst='"+dst+"' and to_char(s1.dep_date,'DD-MM-YYYY')='"+dep_date+"' and (trunc(s2.dep_date)+(f2.dep_time-trunc(f2.dep_time))) >= (trunc(s1.dep_date)+(f1.dep_time-trunc(f1.dep_time))+(f1.est_dur/60+a2.tzone-a1.tzone+1.5)/24) and (trunc(s1.dep_date)+(f1.dep_time-trunc(f1.dep_time))+(f1.est_dur/60+a2.tzone-a1.tzone+5)/24) >= (trunc(s2.dep_date)+(f2.dep_time-trunc(f2.dep_time)))") 
        
        # adds all flight combinations to a list 
        for row in curs:
            nameList.append(row)
            
        # using modified solution from assignment 2
        # uses the namelist to look up other attributes of the flights
        for flight in nameList:
            flightsList.append([])
            for x in [0,1]:
                flightsList[i].append([])
                curs.execute("select trim(f.flightno), f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, fa.price, fa.limit-count(tno), trim(TO_CHAR(sf.dep_date, 'DD-MM-YYYY')), trim(fa.fare) from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2 where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and sf.dep_date=b.dep_date(+) and f.flightno ='"+flight[x]+"' and to_char(sf.dep_date,'DD-MM-YYYY')='"+flight[x+2]+"' group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, fa.price having fa.limit-count(tno) > 0")    
                y = 0                    
                for row in curs:
                    flightsList[i][x].append([ [] for i in range(11)])
                    flightsList[i][x][y][0] = row[0] # flight number
                    flightsList[i][x][y][1] = row[1] # source acode
                    flightsList[i][x][y][2] = row[2] # dest acode
                    flightsList[i][x][y][3] = row[3] # dep time
                    flightsList[i][x][y][4] = row[4] # arr time
                    flightsList[i][x][y][5] = "" # number of stops
                    flightsList[i][x][y][6] = "" #layoverTime
                    flightsList[i][x][y][7] = row[5] # price
                    flightsList[i][x][y][8] = row[6] # num seats avail
                    flightsList[i][x][y][9] = row[7] # dep_date
                    flightsList[i][x][y][10] = row[8] # fare
                    y += 1
            i += 1
        
        # close the connection
        curs.close
        connection.close()

        # returns the flight list for display
        return(flightsList)
    
    # error catching sourced from cx_Oracle tutorial
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)
    
# prints all direct and connection flights 
def printFlights(sortBy, directFlights, connectFlights):

    # combines the two flights in each connection flights
    # to display as single entry
    # stores each combination as list in connectCombos
    connectCombos = []
    for option in connectFlights:
        for flight1 in option[0]:
            for flight2 in option[1]:
                flightNum = flight1[0]+"/"+flight2[0]
                source = flight1[1]
                dest = flight2[2]
                depTime = flight1[3]
                arrTime = flight2[4]
                numStops = "1"
                layoverTime = flight2[3]-flight1[4]
                price = flight1[7]+flight2[7]
                numSeats = min(flight1[8],flight2[8])
                depDate = [flight1[9], flight2[9]]
                fare = [flight1[10], flight2[10]]
                connectCombos.append([flightNum,source,dest,depTime,arrTime,numStops,
                                    layoverTime,price,numSeats,depDate,fare])
    connectFlights = connectCombos

    # combines the lists for direct and connection flights 
    # sorts the resulting list by increasing price
    if sortBy == "price":
        allFlights = directFlights + connectFlights
        allFlights.sort(key=lambda x: float(x[7]))

    # sorts the direct and connection flights list separately
    # combines the list so direct flights are displayed first
    elif sortBy == "direct":
        directFlights.sort(key=lambda x: float(x[7]))
        connectFlights.sort(key=lambda x: float(x[7]))
        allFlights = directFlights + connectFlights

    # prints the header for the flights list
    print("Option",
        "Flight Number",
        "Source",
        "Destination",
        "Departure",
        "Arrival",
        "Stops",
        "Layover Time",
        "Total Price",
        "Seats Left")

    # prints all the flights found
    for flight in allFlights:
        print(str(allFlights.index(flight)).ljust(7)+
        flight[0].ljust(14)+
        flight[1].ljust(7)+
        flight[2].ljust(12)+
        flight[3].strftime("%H:%M").ljust(10)+
        flight[4].strftime("%H:%M").ljust(8)+
        flight[5].ljust(6)+
        str(flight[6]).ljust(13)+
        str(flight[7]).ljust(12)+
        str(flight[8]))

    # returns the flights found
    return(allFlights)

# Gets user to select a flight they want to book and return list of attributes.
def selectFlights(flightsList, totalFlights):
    
    # get user to enter a valid option number
    validInput = False
    while not(validInput):
        option = int(input("Please enter the option number for the flight you want to book: "))
        if option < totalFlights and option > -1:
            validInput = True
        else:
            print("Invalid entry, please try again.")
        
    # extracts flightno, dep_date and fare from connect flight entry
    if len(flightsList[option][9]) == 2:
        flightNo1,flightNo2 = flightsList[option][0].split("/")
        depDate1 = flightsList[option][9][0]
        fare1 = flightsList[option][10][0]
        depDate2 = flightsList[option][9][1]
        fare2 = flightsList[option][10][1]
        # returns info in list for booking
        return([[flightNo1,depDate1,fare1],[flightNo2,depDate2,fare2]])
    # extracts flightno, dep_date and fare from direct flight entry
    else:
        flightNo = flightsList[option][0]
        depDate = flightsList[option][9]
        fare = flightsList[option][10]
        # returns info in list for booking
        return([[flightNo,depDate,fare]])

def main (connectionString):

    # print header info
    print("\nSearching for flights: ")
	
    # get user input for src and dst acodes
    source = input("Enter the source airport: ")
    dest = input("Enter the destination airport: ")
    
    # check validity of ACODE
    source = validAirport(source.strip(), connectionString)
    dest = validAirport(dest.strip(), connectionString)
    
    # get departure date
    dep_date = getDate("departure")
    
    # search for flights from src to dst on dep_date
    directFlights = searchDirectFlights (source, dest, dep_date, connectionString)
    connectFlights = searchConnectFlights (source, dest, dep_date, connectionString)

    # check if user wants to search for round trips
    searchRoundtrip = input("\nDo you want to search for round trips? Enter y or n: ").lower()
    if searchRoundtrip == "y":
        # get return date
        return_date = getDate("return")

        # search for return flights
        directReturns = searchDirectFlights (dest, source, return_date, connectionString)
        connectReturns = searchConnectFlights (dest, source, return_date, connectionString)  
        
        # sort & print departing and returning flights seperately
        print("\nDEPARTING FLIGHTS:")
        departingFlights = printFlights("price", directFlights, connectFlights)
        if len(departingFlights) == 0:
            print("No flights were found.")            
        print("\nRETURNING FLIGHTS:")
        returningFlights = printFlights("price", directReturns, connectReturns)
        if len(returningFlights) == 0:
            print("No flights were found.")        
        # if flights are not found then return empty without booking
        if len(departingFlights) == 0 or len(returningFlights) == 0:
            return([])        

    else:
        # in case of one way flight only
        # get sort preference from user, sort and print the flights
        sortBy = input("\nSort by price or direct: ").strip().lower()
        print("\nDEPARTING FLIGHTS:")
        departingFlights = printFlights(sortBy, directFlights, connectFlights)
        if len(departingFlights) == 0:
            print("No flights were found.") 
            # if flights are not found then return empty without booking
            return([])

    # book flights if wanted by user
    selectedDeparting = []
    selectedReturning = []     
    bookFlights = input("Do you want to book any flights? Enter y or n: ").lower()
    if bookFlights == "y":
        # get user to pick a flight to book for departing flights
        print("\nNow selecting outbound flight.") 
        selectedDeparting = selectFlights(departingFlights, len(departingFlights))
        # get user to pick a flight to book for returning flights
        if searchRoundtrip == "y":
            print("\nNow selecting inbound flight.") 
            selectedReturning = selectFlights(returningFlights, len(returningFlights))
            # return the results which is a list of flightno, dep_date and fare of selected flights
            return(selectedDeparting+selectedReturning)            

    # return the results which is a list of flightno, dep_date and fare of selected flights
    return(selectedDeparting)

