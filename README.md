# Ping-Traceroute
README.txt

Both the programs have been developed and tested in Windows environment.
Raw sockets have been used to create ICMP packets so that these programs work like the ping and tracert (trace route application in Windows)
In Mac or Linux environment, we need root privileges.
If python command does not work, try python3 command


darryl_ping.py:
=================================================================

Usage: python darryl_ping.py [-c count] [-i swait] [-s packetsize] [-t timeout] [-z soc_timeout] target_name

To run the ping application type the following command on Windows:
    python darryl_ping.py target_name

To access the help menu type the following command
    python darryl_ping.py

On Mac try the following command:
	sudo python3 darryl_ping.py target_name


darryl_traceroute.py
=================================================================

Usage: python darryl_traceroute.py [-n] [-q nqueries] [-S] [-h maxhops] [-z soc_timeout] target_name

To run the trace route application type the following command:
    python darryl_traceroute.py target_name

To access the help menu type the following command:
    python darryl_traceroute.py

On Mac try the following command:
	sudo python3 darryl_traceroute.py target_name
