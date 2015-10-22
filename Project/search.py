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


def validAirport ():
    try:
        connection = cx_Oracle.connect('abbasi1/c291database@gwynne.cs.ualberta.ca:1521/CRS')
        curs = connection.cursor()
        # get list of airports
        curs.execute("SELECT acode FROM airports")
        for row in curs:
            print(row)
        # if airport exists return code
        # else look for matches and get user to choose
        curs.close
        connection.close()
    # error catching sourced from cx_Oracle tutorial
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)    


def main ():
    #source = input("Enter the source airport: ")
    #dest = input("Enter the destination airport: ")
    #depart_date = getDepartureDate()
    validAirport()
main()