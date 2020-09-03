import os
import re
import csv
import time
from os import sys
from sys import platform

if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

if not len(sys.argv) == 2:
    print('Specify at least one parameters. $python script.py example')
    quit()
else:
    service_name = sys.argv[1]

if not os.geteuid() == 0:
    print('You need root rights to start the script')

if not os.path.isfile('/lib/systemd/system/' + service_name + '.service'):
    print('This service does not exist')
    quit()

path = '/var/python/' + service_name
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
os.system('sudo update-rc.d -f ' + service_name + '.autostart remove')
os.system('sudo update-rc.d ' + service_name + '.autostart defaults')

w = csv.writer(open(path + '/.data.csv', 'w'))
w.writerow(['creation_timestamp', 'name', 'autostart'])
w.writerow([time.strftime("%d.%m.%Y %H:%M:%S"), service_name, '1'])
os.system('sudo chmod 777 ' + path)
