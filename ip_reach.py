import sys
import subprocess

# Ping IP to see if available
def ip_reach(list):

    for ip in list:
        ip = ip.rstrip("\n")

        ping_reply = subprocess.call("ping %s -n 2" % (ip,), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if ping_reply == 0:
            print("\n* {} is reachable \n".format(ip))
            continue

        else:
            print('\n* {} is not reachable \n* exiting program\n'.format(ip))
            sys.exit