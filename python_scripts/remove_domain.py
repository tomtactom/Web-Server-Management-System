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

mail = value[3]
os.system('sudo rm -R /var/www/' + domainname)
os.system('sudo rm /etc/apache2/sites-available/' + domainname + '.conf')
os.system('sudo rm /etc/apache2/sites-enabled/' + domainname + '.conf')

os.system('sudo systemctl reload apache2')
os.system('sudo letsencrypt delete --cert-name ' + domainname)
os.system('sudo rm /etc/apache2/sites-available/' + domainname + '-le-ssl.conf')
os.system('sudo rm /etc/apache2/sites-enabled/' + domainname + '-le-ssl.conf')
os.system('sudo systemctl reload apache2')

os.system('crontab -u user -l | grep -v "sudo letsencrypt --apache -d ' + domainname + ' --agree-tos -m ' + mail + ' --no-eff-email --no-redirect --renew-by-default"  | crontab -u user -')

