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
    
def main ():
    connection = cx_Oracle.connect('abbasi1/c291database@gwynne.cs.ualberta.ca:1521/CRS')
    
    source = input("Enter the source airport: ")
    dest = input("Enter the destination airport: ")
    depart_date = getDepartureDate()
    
    # check if source is valid, check if source in get airport codes from DB
    
    # check if dest is valid

main()