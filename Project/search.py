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
                print(matchList[0].ljust(4),matchList[1].ljust(31),matchList[2].ljust(16))
            while not(validInput):
                print("/nThese airports matched your entry.")
                airport = input("Please type an ACODE from the above list: ")
                airport = airport.upper()
                if airport in [acode for acode=matchList[0] in matchList]:
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


def main ():
    source = input("Enter the source airport: ")
    #dest = input("Enter the destination airport: ")
    #depart_date = getDepartureDate()
    source = validAirport(source)
    #validAirport(dest)
main()
