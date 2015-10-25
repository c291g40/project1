# Mustafa Abbasi
# This function searches for available flights
import cx_Oracle
import datetime

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


def validAirport (acode):
    try:
        acode = acode.upper()
        acodeList = []
        matchList = []
        validAirport = False

        # connect to database
        connection = cx_Oracle.connect('abbasi1/c291database@gwynne.cs.ualberta.ca:1521/CRS')
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

def searchDirectFlights (src, dst, dep_date):
    flightsList = []
    i = 0
    try:
        # connect to database
        connection = cx_Oracle.connect('abbasi1/c291database@gwynne.cs.ualberta.ca:1521/CRS')
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
    
def searchConnectFlights (src, dst, dep_date):
    flightsList = []
    i = 0
    try:
        # connect to database
        connection = cx_Oracle.connect('abbasi1/c291database@gwynne.cs.ualberta.ca:1521/CRS')
        curs = connection.cursor()
        
        # using official answer for A2Q7 for testing
        # get list of direct flights
        curs.execute("select f.flightno, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, fa.price, fa.limit-count(tno) from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2 where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and sf.dep_date=b.dep_date(+) and f.src ='"+src+"' and f.dst='"+dst+"' and to_char(sf.dep_date,'DD/MM/YYYY')='"+dep_date+"' group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, fa.price having fa.limit-count(tno) > 0")
        
        for row in curs:
            flightsList.append([ [] for i in range(9)])
            flightsList[i][0] = row[0] # flight number
            flightsList[i][1] = row[1] # source acode
            flightsList[i][2] = row[2] # dest acode
            flightsList[i][3] = row[3] # dep time
            flightsList[i][4] = row[4] # arr time
            flightsList[i][5] = "1" # number of stops
            layoverTime = row[4]-row[3]
            flightsList[i][6] = layoverTime # layover time
            flightsList[i][7] = row[5] # price
            flightsList[i][8] = row[6] # num seats avail
            #print(type(flightsList[0][3]))
            #print(flightsList[0][4].strftime("%d/%m/%Y"))
            #print(flightsList[0][6])
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
    
def sortFlights(sortBy, directFlights, connectFlights):
    if sortBy == "price":
        allFlights = directFlights + connectFlights
        allFlights.sort(key=lambda x: float(x[5]))
    else:
        directFlights.sort(key=lambda x: float(x[5]))
        connectFlights.sort(key=lambda x: float(x[5]))
        allFlights = directFlights + connectFlights
    print("Option","Flight Number","Source","Destination","Departure Time","Arrival Time","Stop","Layover Time","Price","Seats Left")
    for flight in allFlights:
        print(flight)
    return(allFlights)

def main ():
    # get user input for src, dst, date#
    source = "YEG" #input("Enter the source airport: ")
    dest = "YYZ" #input("Enter the destination airport: ")
    dep_date = "22/12/2015" #getDepartureDate()

    # check validity of ACODE
    source = validAirport(source.strip())
    dest = validAirport(dest.strip())

    # search for flights
    directFlights = searchDirectFlights (source, dest, dep_date)
    connectFlights = searchConnectFlights (source, dest, dep_date)

    # sort the lists
    sortBy = input("Sort by price or direct: ").strip().lower()
    allFlights = sortFlights(sortBy, directFlights, connectFlights)

main()
