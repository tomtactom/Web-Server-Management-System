import os
from os import sys
from sys import platform
import shutil

if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

if not len(sys.argv) == 2:
    print('Specify at least one parameters. $python script.py example')
    quit()

service_name = sys.argv[1]

if not os.geteuid() == 0:
    print('You need root rights to start the script')
    quit()

path = '/var/python/' + service_name
if not os.path.isdir(path):
    print('This service does not exist')
    quit()

# Autostart entfernen
if os.path.isfile('/etc/init.d/' + service_name + '.autostart'):
    os.system('sudo update-rc.d -f ' + service_name + '.autostart remove')
    os.remove('/etc/init.d/' + service_name + '.autostart')

os.system('sudo service ' + service_name + 'stop')
shutil.rmtree(path)
os.remove('/lib/systemd/system/' + service_name + '.service')
