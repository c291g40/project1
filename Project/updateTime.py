import datetime
import sys
import cx_Oracle

def updateTime (connectionString, changeType):
    print("Updating %s Time." %(changeType))
    validInput = False
    while not(validInput):
        flightNo = input("Enter the flight number: ")
        if len(flightNo) > 6:
            print("Invalid entry for flight number: ")
        else:
            validInput = True

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
    
    validInput = False
    while not(validInput):
        newTime = input("Please enter the %s time of the flight as HH:MM: " %(changeType)).strip()
        try:
            if int(newTime[11:13]) not in range(24):
                print("Invalid entry for hours.")
            elif int(newTime[14:]) not in range(60):
                print("Invalid entry for minutes.")
        except:
            print("Invalid entry.")
        else:
            validInput = True
    try:
        connection = cx_Oracle.connect(connectionString)
        curs = connection.cursor()
        if changeType == "Arrival":
            curs.execute("UPDATE sch_flights SET act_arr_time = TO_DATE('%s','DD/MM/YYYY HH24:MI') WHERE TO_CHAR(dep_date, 'DD/MM/YYYY') = '%s' AND flightno = '%s'" %(newTime,depart_date,flightNo))
        else:
            curs.execute("UPDATE sch_flights SET act_dep_time = TO_DATE('%s','DD/MM/YYYY HH24:MI') WHERE TO_CHAR(dep_date, 'DD/MM/YYYY') = '%s' AND flightno = '%s'" %(newTime,depart_date,flightNo))
        curs.execute("COMMIT")
        # close the connection
        curs.close
        connection.close()
        
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)

updateTime('abbasi1/c291database@gwynne.cs.ualberta.ca:1521/CRS',"Departure")
