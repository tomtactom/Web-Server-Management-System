import os
import csv
from os import sys
from sys import platform

if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

if not len(sys.argv) == 2:
    print('Specify at least one parameter. $python script.py example.com')
    quit()
else:
    domainname = sys.argv[1]

if not os.path.isdir('/var/www/' + domainname):
    print('This subdomain does not exist')
    quit()

with open('/var/www/' + domainname + '/.data.csv') as csvfile:
    data = csvfile.readlines()
    value = []
    for i in data:
        value.append(data[1].replace('\r\n', '').split(','))
    value = value[0]

w = csv.writer(open('/var/www/' + domainname + '/.data.csv', 'w'))
w.writerow(['creation_timestamp', 'domainname', 'mail', 'redirection'])
w.writerow([value[0], value[1], value[2], '0'])

os.system('sudo rm /var/www/' + domainname + '/.htaccess')
print("The redirect was successfully removed")

