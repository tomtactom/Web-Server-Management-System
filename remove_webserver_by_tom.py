import os
from sys import platform

# Das Script nur auf Linux laufen lassen
if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

# Ueberpruefe ob der Nutzer Root Rechte hat
if not os.geteuid() == 0:
    print('You need root rights to start the script. Try sudo :)')
    quit()

print('The /var/www/ directory must be deleted, please make a backup beforehand.')
delete_www = input('Do you want to delete it? (yes(recommended)/no/leave blank is equal as yes): ')
if delete_www == '' or delete_www == 'yes' or delete_www == 'y' or delete_www == 'Yes' or delete_www == 'Y':
    delete_www = True
    print('The directory will be deleted, if you have not yet made a backup, cancel the script as soon as possible.')
else:
    delete_www = False
    print('The directory will not be deleted.')

os.system('sudo apt purge apache2* -y')
os.system('sudo apt purge php* -y')
os.system('sudo rm -R /etc/apache2')
os.system('sudo rm -R /etc/php')
os.system('sudo apt purge mariadb-client -y')
os.system('sudo apt purge mariadb-server -y')
os.system('sudo apt purge mysql* -y')
os.system('sudo rm -R /etc/mysql')
length = 100000
domains = []
for l in os.listdir('/var/www/'):
    if l == 'html' or l == 'phpmyadmin':
        pass
    else:
        domains.append(l)
        if len(l) < length:
            length = len(l)
            result = l

domains.append('phpmyadmin.' + result)
for domain in domains:
    os.system('sudo certbot delete -d ' + domain)

if delete_www == True:
    os.system('sudo rm -R /var/www')

os.system('sudo apt purge letsencrypt certbot -y')
os.system('sudo rm /var/spool/cron/crontabs/pi')
print('The system has been completely uninstalled')

