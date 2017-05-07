#!/usr/bin/python

import time
import datetime

try:
    f = open('ActivatedAlarmTimes.log', 'r')
    lines = f.readlines()
    f.close()
    start = True
    
    while(start == True):
        method = raw_input("Enter what method you want to use to clean the log file. Delete line per line: 'line', or delete per date range: 'range'. \n")

	if(method == 'line'):
	    start = False
	    newLines = []
	    print("Method line per line: \n\n")
	
	    for line in lines:
		print("Next line from log: \n")
		print(line)
		option = raw_input("Delete (D) or keep (K) this line?")
		
		if (option == 'D'):
		    print("\nDELETED LINE")
		    #lines.remove(line)
		    		
		elif (option == 'K'):
		    newLines.append(line)
		    print("\nKEPT LINE")
		
		else:
		    print("Invalid request.")
	
	    f = open('ActivatedAlarmTimes.log', 'w')
       	    for line in newLines:
      	        f.write(line)
	    f.close
		    

	elif(method == 'range'):
	    start = False
	    newLines = []
	    print("method range")

	    startTimeStamp = time.strptime(raw_input("Start-time to delete logs.(dd-mm-yy hh:mm:ss): "), "%d-%m-%y %H:%M:%S")
	    endTimeStamp = time.strptime(raw_input("End-time to delete logs.(dd-mm-yy hh:mm:ss): "), "%d-%m-%y %H:%M:%S")
	    
	    for line in lines:
       	        #Ik krijg deze text objecten niet geparsed naar tijd object, op geen enkele manier. Veel opgezocht en niets werkt. Is het enige dat niet werkt van het labo.

    	        time = time.strptime(line, "%d-%m-%y %H:%M:%S")
		time.struct_time(tm_year=2000, tm_mon=11, tm_mday=30, tm_hour=0, tm_min=0,
                 tm_sec=0, tm_wday=3, tm_yday=335, tm_isdst=-1)
		if(time < startTimeStamp) or (time > endTimeStamp):
 	            newLines.append(line)
	
	    f = open('ActivatedAlarmTimes.log', 'w')
	    for line in newLines:
		f.write(line)
	    f.close
	
	else:
	    print("Invalid request. \n")


except KeyboardInterrupt:
    print("Exiting program")
