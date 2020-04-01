#!/bin/bash

######################################################################
# This script will check network devices to see if they are avilable #
# on the network. It will log all of the  pings with timestamps. If  #
# something is not working, the script will send the adminsitrator   #
# an email                                                           #
######################################################################


echo "Ping has started"


# Define the ping function.
# Declare now variable as current date. 


now=$(date)
echo "$now"

P1=Youtube.com
P2=Google.com
P3=83.79.9.3

ping_function(){
echo "Pinging $P1"
var1=$(ping $P1 -c3 | cut -d" " -f5-8 | tail -n2 | cut -d"," -f2 | cut -d"%" -f1 | cut -d"m" -f1)
echo $var1
echo "Pinging $P2"
var2=$(ping $P2 -c3 | cut -d" " -f5-8 | tail -n2 | cut -d"," -f2 | cut -d"%" -f1 | cut -d"m" -f1)
echo $var2
echo "Pinging $P3"
var3=$(ping $P3 -c3 | cut -d" " -f5-8 | tail -n2 | cut -d"," -f2 | cut -d"%" -f1 | cut -d"m" -f1)
echo $var3
}


# Call the ping function.


ping_function

echo "Ping has completed"


# Check if the site is up or down.
# If up echo that it is up, if down echo that is down and send email.


if [ $var1 -eq 0 ];
	then echo "$P1 is up"
		else mail -s "$P1 is down" davidskoro@local < pingcheck.txt
fi

if [ $var2 -eq 0 ];
	then echo "$P2 is up"
		else mail -s "$P2 is down" davidskoro@local < pingcheck.txt
fi

if [ $var3 -eq 0 ];
	then echo "$P3 is up"
		else mail -s "$P3 is down" davidskoro@local < pingcheck.txt
fi



# end the script

