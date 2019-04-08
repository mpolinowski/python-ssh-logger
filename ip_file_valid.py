import sys
import os.path

# Check if the IP address file is available and valid


def ip_file_valid():
    # Prompt for file path
    ip_file = input("\n# please enter server IP file - e.g. ./serverip.env : ")

    # Check file available
    if os.path.isfile(ip_file) == True:
        print("\n* filepath is valid")

    else:
        print("\n* file {} does not exist. \n* exiting program \n".format(ip_file))
        sys.exit()

    # Open IP file for reading
    selected_ip_file = open(ip_file, 'r')

    # Read from the beginning
    selected_ip_file.seek(0)

    # Read all lines
    ip_list = selected_ip_file.readlines()

    #Closing the file
    selected_ip_file.close()

    return ip_list
