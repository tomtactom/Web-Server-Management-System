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

if not os.path.isfile('/etc/init.d/' + service_name + '.autostart'):
    print('This autostart are not seted')
    quit()

# Autostart entfernen
os.system('sudo service ' + service_name + ' stop')
os.system('sudo update-rc.d -f ' + service_name + '.autostart remove')
os.remove('/etc/init.d/' + service_name + '.autostart')
os.system('sudo service ' + service_name + ' start')

# In .data.csv eintragen, dass autostart deaktiviert wurde
path = '/var/python/' + service_name
w = csv.writer(open(path + '/.data.csv', 'w'))
w.writerow(['creation_timestamp', 'name', 'autostart'])
w.writerow([time.strftime("%d.%m.%Y %H:%M:%S"), service_name, '0'])
os.system('sudo chmod 777 ' + path)
