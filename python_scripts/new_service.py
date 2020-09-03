import os
import re
import csv
import time
from os import sys
from sys import platform

if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

if not len(sys.argv) >= 2:
    print('Specify at least two parameters. $python script.py example [1|true|True|autostart](optional)')
    quit()

service_name = sys.argv[1]
if len(sys.argv) >= 3:
    autostart = sys.argv[2]
else:
    autostart = False

if not os.geteuid() == 0:
    print('You need root rights to start the script')

for i in list(service_name):
    if not re.search("[abcdefghijklmnopqrstuvwxyz0123456789]", i):
        print("NotValidServiceName: Servicenames contains invalid characters.")
        quit()

if len(service_name) >= 42:
    print('NotValidServiceName: The servicename can not be more than 42 characters long')
    quit()

if autostart == '1' or autostart == 'true' or autostart == 'True' or autostart == 'autostart':
    autostart = True
    autostarting = '1'
else:
    autostart = False
    autostarting = '0'

path = '/var/python/' + service_name

if os.path.isdir(path):
    print('These service already exists')
    quit()

os.makedirs(path + '/docs')
os.system('sudo chmod -R 777 ' + path)
#Überprüfen ob Service schon existiert...
with open('/lib/systemd/system/' + service_name + '.service', 'w') as file:
    file.write('[Unit]\n')
    file.write('Description=' + service_name + '\n')
    file.write('\n')
    file.write('[Install]\n')
    file.write('WantedBy=multi-user.target\n')
    file.write('\n')
    file.write('[Service]\n')
    file.write('User=www-data\n') # ACHTUNG: Hier muss ggf. der Nutzername ausgetauscht werden...
    file.write('PermissionsStartOnly=true\n')
    file.write('ExecStart=sudo python3 ' + path + '/docs/main.py\n') # ACHTUNG: Hier muss ggf. das 'sudo' entfernt werden...
    file.write('TimeoutSec=600\n')
    file.write('Restart=on-failure\n')
    file.write('RuntimeDirectoryMode=755\n')
	
os.system('sudo systemctl daemon-reload');

if autostart == True:
    with open('/etc/init.d/' + service_name + '.autostart', 'w') as file:
        file.write('! /bin/sh\n')
        file.write('### BEGIN INIT INFO\n')
        file.write('# Provides:          ' + service_name + '.autostart\n')
        file.write('# Required-Start:    $start\n')
        file.write('# Required-Stop:     $shutdown\n')
        file.write('# Default-Start:     2 3 4 5\n')
        file.write('# Default-Stop:      0 1 6\n')
        file.write('# Short-Description: undefined\n')
        file.write('# Description:       undefined\n')
        file.write('### END INIT INFO\n')
        file.write('# Author: unknown\n')
        file.write('\n')
        file.write('# Aktionen\n')
        file.write('sudo service ' + service_name + ' start\n')

    os.system('sudo chmod 755 /etc/init.d/' + service_name + '.autostart')
    os.system('sudo update-rc.d ' + service_name + '.autostart defaults')

w = csv.writer(open(path + '/.data.csv', 'w'))
w.writerow(['creation_timestamp', 'name', 'autostart'])
w.writerow([time.strftime("%d.%m.%Y %H:%M:%S"), service_name, autostarting])
os.system('sudo chmod 777 -R ' + path)
