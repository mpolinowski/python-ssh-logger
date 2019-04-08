import paramiko
import datetime
import os.path
import time
import sys
import re

# Check username/password file
user_file = input("\n# enter user login file path - e.g. ./userlogin.env : ")

# Verifying file exists
if os.path.isfile(user_file) == True:
    print("\n* login file accepted\n")

else:
    print("\n* file {} does not exist \n* exiting program \n".format(user_file))
    sys.exit()
        
# Check commands file
cmd_file = input("\n# enter commands file path - e.g. ./commands.env : ")

# Verifying file exists
if os.path.isfile(cmd_file) == True:
    print("\n* command file accepted\n")

else:
    print("\n* file {} does not exist \n* exiting program \n".format(cmd_file))
    sys.exit()
    
# Open SSHv2 connection to the server
def ssh_connection(ip):
    
    global user_file
    global cmd_file
    
    try:
        # Get SSH user login
        selected_user_file = open(user_file, 'r')
        
        # Read from beginning
        selected_user_file.seek(0)
        
        # Get username from file
        username = selected_user_file.readlines()[0].split(',')[0].rstrip("\n")
        
        #Read from beginning
        selected_user_file.seek(0)
        
        # Get password from file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        
        #Login
        session = paramiko.SSHClient()
        
        # This allows auto-accepting unknown host keys
        # Default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the device using username and password          
        session.connect(ip.rstrip("\n"), username = username, password = password)
        
        # Start an interactive shell session
        connection = session.invoke_shell()
        
        #Setting terminal length for entire output - disable pagination
        # connection.send("clear\n")
        # time.sleep(1)
        
        # Open command file for reading
        selected_cmd_file = open(cmd_file, 'r')
            
        # Read from beginning
        selected_cmd_file.seek(0)
        
        # Writing each line in the file to the shell
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        
        # Close the user file
        selected_user_file.close()
        
        # Close the command file
        selected_cmd_file.close()
        
        # Checking command output for syntax errors
        server_response = connection.recv(65535)
        
        if re.search(b"% Invalid input", server_response):
            print("* There was at least one syntax error in the given command {}".format(ip))
            
        else:
            print("\nServer {} Response:\n".format(ip))
            
        # Test for reading command output
        # print(str(server_response) + "\n")
        
        # Searching for the CPU utilization value within the output of "show processes top once"
        cpu = re.search(b"(%Cpu\(s\): ) (.+?)(us)", server_response)
        # cpu = server_response
        
        # Extracting the second group, which matches the actual value of the CPU utilization and decoding to the UTF-8 format from the binary data type
        utilization = cpu.group(2).decode("utf-8")
        # utilization = cpu.decode("utf-8")
        
        # Printing the CPU utilization value to the screen
        # print(utilization)
        
        # Opening the CPU utilization text file and appending the results
        with open("E:\\python-ssh-logger\\cpu-load.txt", "a") as f:
            # f.write("{},{}\n".format(str(datetime.datetime.now()), utilization))
            f.write(utilization + "\n")
        
        #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print("\n* invalid username or password \n* exiting program \n")