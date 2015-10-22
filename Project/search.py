# Mustafa Abbasi
# This function searches for available flights
import cx_Oracle
import datetime

def getDepartureDate ():
    validInput = False
    while not(validInput):
        depart_date = input("Enter the departure date as DD-MM-YEAR: ")
        try:
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

def searchFlights (src, dst, dep_date):
    try:
        # connect to database
        connection = cx_Oracle.connect('abbasi1/c291database@gwynne.cs.ualberta.ca:1521/CRS')
        curs = connection.cursor()
        # using official answer for A2Q7 for testing
        #directFlightsString = 

        # get list of direct flights
        curs.execute("select f.flightno, sf.dep_date, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, fa.fare, fa.limit-count(tno), fa.price from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2 where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and sf.dep_date=b.dep_date(+) and f.src ='"+src+"' and f.dst='"+dst+"' group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, fa.price having fa.limit-count(tno) > 0")
        
        for row in curs:
            print(row)
        
        # close the connection
        curs.close
        connection.close()

    
    # error catching sourced from cx_Oracle tutorial
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)
    

def main ():
    # get user input for src, dst, date
    source = input("Enter the source airport: ")
    dest = input("Enter the destination airport: ")
    dep_date = getDepartureDate()

    # check validity of ACODE
    source = validAirport(source)
    dest = validAirport(dest)

    # search for flights
    searchFlights (source, dest, dep_date)



main()
