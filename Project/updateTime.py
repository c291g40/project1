import datetime
import sys
import cx_Oracle

# This function updates the actual arrival and departure time of flights.
def updateTime (connectionString, changeType):
    
    print("Updating %s Time." %(changeType))
    
    # Gets the flight number.
    validInput = False
    while not(validInput):
        flightNo = input("Enter the flight number: ").strip()
        if len(flightNo) > 6:
            print("Invalid entry for flight number: ")
        else:
            validInput = True

    # Gets the departure date.
    validInput = False
    while not(validInput):
        depart_date = input("Enter the departure date as DD-MM-YYYY: ")
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
    
    # Gets the time to set as act_arr or act_dep.
    validInput = False
    while not(validInput):
        newTime = input("Please enter the %s time of the flight as HH:MM: " %(changeType)).strip()
        try:
            if int(newTime[0:2]) not in range(24):
                print("Invalid entry for hours.")
            elif int(newTime[3:]) not in range(60):
                print("Invalid entry for minutes.")
        except:
            print("Invalid entry.")
        else:
            validInput = True

    # Updates the database.
    try:
        # Creating connection.
        connection = cx_Oracle.connect(connectionString)
        curs = connection.cursor()

        # Selects correct arr/dep time and updates in database.
        if changeType == "Arrival":
            curs.execute("UPDATE sch_flights SET act_arr_time = TO_DATE('%s','HH24:MI') WHERE TO_CHAR(dep_date, 'DD-MM-YYYY') = '%s' AND flightno = '%s'" %(newTime,depart_date,flightNo))
        else:
            curs.execute("UPDATE sch_flights SET act_dep_time = TO_DATE('%s','HH24:MI') WHERE TO_CHAR(dep_date, 'DD-MM-YYYY') = '%s' AND flightno = '%s'" %(newTime,depart_date,flightNo))
        connection.commit()

        # Close the connection.
        curs.close
        connection.close()
        
    # error catching sourced from cx_oracle tutorial
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)

# updateTime('abbasi1/c291database@gwynne.cs.ualberta.ca:1521/CRS',"Departure")
