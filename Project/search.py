# Mustafa Abbasi
# This function searches for available flights
import cx_Oracle
import datetime
import sys

# to-do
# check seats>0
# check times of connecting flights
# use connectstring from main


def getDepartureDate ():
    validInput = False
    while not(validInput):
        depart_date = input("Enter the departure date as DD/MM/YEAR: ")
        try:
            depart_date = depart_date.strip()
            day = int(depart_date[0:2])
            month = int(depart_date[3:5])
            year = int(depart_date[6:])
            datetime.datetime(year, month, day)
        except:
            print("Invalid input for date. Please try again.")
        else:
            validInput = True
            return depart_date


def validAirport (acode , connectionString):
    try:
        acode = acode.upper()
        acodeList = []
        matchList = []
        validAirport = False

        # connect to database
        connection = cx_Oracle.connect(connectionString)
        curs = connection.cursor()

        # get list of airports
        curs.execute("SELECT acode FROM airports")
        for row in curs:
            acodeList.append(row[0].upper())
        
        # if airport exists return code
        if acode in acodeList:
            validAirport = True
        
        if not(validAirport):
            # get list of matching airports' name, city
            curs.execute("SELECT acode,name,city FROM airports")
            for row in curs:
                if acode in row[1].upper() or acode in row[2].upper():
                    temp = [row[0].upper(), row[1].upper(), row[2].upper()]
                    matchList.append(temp)
        
            # get user to select a matching airport
            validInput = False
            for match in matchList:
                print(match[0].ljust(4),match[1].ljust(31),match[2].ljust(16))
            while not(validInput):
                print("\nThese airports matched your entry.")
                airport = input("Please type an ACODE from the above list: ")
                airport = airport.upper()
                if airport in [match[0] for match in matchList]:
                    validInput = True
             
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

def searchDirectFlights (src, dst, dep_date,connectionString):
    flightsList = []
    i = 0
    try:
        # connect to database
        connection = cx_Oracle.connect(connectionString)
        curs = connection.cursor()
        
        # using official answer for A2Q7 for testing
        # get list of direct flights
        curs.execute("select f.flightno, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, fa.price, fa.limit-count(tno) from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2 where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and sf.dep_date=b.dep_date(+) and f.src ='"+src+"' and f.dst='"+dst+"' and to_char(sf.dep_date,'DD/MM/YYYY')='"+dep_date+"' group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, fa.price having fa.limit-count(tno) > 0")
        
        for row in curs:
            flightsList.append([ [] for i in range(9)])
            flightsList[i][0] = row[0]
            flightsList[i][1] = row[1]
            flightsList[i][2] = row[2]
            flightsList[i][3] = row[3]
            flightsList[i][4] = row[4]
            flightsList[i][5] = "0"
            flightsList[i][6] = "N/A"
            flightsList[i][7] = row[5]
            flightsList[i][8] = row[6]
            #print(type(flightsList[0][3]))
            #print(flightsList[0][4].strftime("%d/%m/%Y"))
            i += 1
        
        # close the connection
        curs.close
        connection.close()

        return(flightsList)
    
    # error catching sourced from cx_Oracle tutorial
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)
    
def searchConnectFlights (src, dst, dep_date,connectionString):
    nameList = []
    flightsList = []
    i = 0
    try:
        # connect to database
        connection = cx_Oracle.connect(connectionString)
        curs = connection.cursor()
        
        # using official answer for A2Q9/10 for testing
        # get list of direct flights
        curs.execute("select s1.flightno, s2.flightno, s1.dep_date, s2.dep_date from sch_flights s1, sch_flights s2, flights f1, flights f2, airports a1, airports a2 where f1.src=a1.acode and f1.dst=a2.acode and s1.flightno = f1.flightno and s2.flightno = f2.flightno and f1.src ='"+src+"' and f2.dst='"+dst+"' and f1.dst=f2.src and to_char(s1.dep_date,'DD/MM/YYYY')='"+dep_date+"'") 
# and f1.dep_time+(trunc(s1.dep_date)-trunc(f1.dep_time)) +1.5/24 <=f2.dep_time and (f1.dep_time+(trunc(s1.dep_date)-trunc(f1.dep_time))+(f1.est_dur/60+a2.tzone-a1.tzone)/24)+5/24 >=f2.dep_time")
        
        for row in curs:
            nameList.append(row)
            
        for flight in nameList:
            flightsList.append([])
            for x in [0,1]:
                flightsList[i].append([])
                curs.execute("select f.flightno, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, fa.price, fa.limit-count(tno) from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2 where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and sf.dep_date=b.dep_date(+) and f.flightno ='"+flight[x]+"' and to_char(sf.dep_date,'DD/MM/YYYY')='"+flight[x+2].strftime("%d/%m/%Y")+"' group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, fa.price having fa.limit-count(tno) > 0")    
                y = 0                    
                for row in curs:
                    flightsList[i][x].append([ [] for i in range(9)])
                    flightsList[i][x][y][0] = row[0].strip() # flight number
                    flightsList[i][x][y][1] = row[1] # source acode
                    flightsList[i][x][y][2] = row[2] # dest acode
                    flightsList[i][x][y][3] = row[3] # dep time
                    flightsList[i][x][y][4] = row[4] # arr time
                    flightsList[i][x][y][5] = "" # number of stops
                    #layoverTime = row[4]-row[3]
                    flightsList[i][x][y][6] = "" #layoverTime # layover time
                    flightsList[i][x][y][7] = row[5] # price
                    flightsList[i][x][y][8] = row[6] # num seats avail
                    #print(type(flightsList[0][3]))
                    #print(flightsList[0][4].strftime("%d/%m/%Y"))
                    #print(flightsList[0][6])
                    y += 1
            i += 1
        
        # close the connection
        curs.close
        connection.close()

        return(flightsList)
    
    # error catching sourced from cx_Oracle tutorial
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)
    
def selectFlights(sortBy, directFlights, connectFlights):
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
                connectCombos.append([flightNum,source,dest,depTime,arrTime,numStops,layoverTime,price,numSeats])
    connectFlights = connectCombos

    if sortBy == "price":
        allFlights = directFlights + connectFlights
        allFlights.sort(key=lambda x: float(x[7]))
    else:
        directFlights.sort(key=lambda x: float(x[7]))
        connectFlights.sort(key=lambda x: float(x[7]))
        allFlights = directFlights + connectFlights
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
    return(allFlights)

def main (email, connectionString):
	
    # get user input for src, dst, date#
    source = input("Enter the source airport: ")
    dest = input("Enter the destination airport: ")
    dep_date = getDepartureDate()

    # check validity of ACODE
    source = validAirport(source.strip(), connectionString)
    dest = validAirport(dest.strip(), connectionString)
	
	
    # search for flights
    directFlights = searchDirectFlights (source, dest, dep_date, connectionString)
    connectFlights = searchConnectFlights (source, dest, dep_date, connectionString)

    # sort the lists
    sortBy = input("Sort by price or direct: ").strip().lower()
    allFlights = selectFlights(sortBy, directFlights, connectFlights)

#main(email, connectio)
