import sys
import time

# Importing our modules
from ip_file_valid import ip_file_valid
from ip_addr_valid import ip_addr_valid
from ip_reach import ip_reach
from ssh_connect import ssh_connection
from create_threads import create_threads

# Saving the list of IP addresses to a variable
ip_list = ip_file_valid()

# Verifying the validity of each IP address in the list
try:
    ip_addr_valid(ip_list)
    
except KeyboardInterrupt:
    print("\n\n* Program aborted by user. Exiting...\n")
    sys.exit()

# Verifying the reachability of each IP address in the list
try:
    ip_reach(ip_list)
    
except KeyboardInterrupt:
    print("\n\n* Program aborted by user. Exiting...\n")
    sys.exit()

# Calling threads creation function for one or multiple SSH connections
while True:
    # while loop will keep running querying CPU utilization every 10 sec
    create_threads(ip_list, ssh_connection)
    time.sleep(10)

# End of program