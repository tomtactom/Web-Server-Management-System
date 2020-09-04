import os
from sys import platform

# Check if the system is linux based
if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

# Check if the user have root rights
if not os.geteuid() == 0:
    print('You need root rights to start the script. Try sudo :)')
    quit()

print('The /var/www/ and /var/python/ directory must be deleted, please make a backup before delete.')
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
if os.path.isdir('/var/www/'):
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

else:
    print('No domains were found.')

os.system('sudo apt purge letsencrypt certbot -y')
os.system('sudo rm /var/spool/cron/crontabs/www-data')

# remove services
if os.path.isdir('/var/python/'):
    for service_name in os.listdir('/var/python/'):
    	if os.path.isdir('/var/python/'):
    		# remove autostart
    		if os.path.isfile('/etc/init.d/' + service_name + '.autostart'):
    			os.system('sudo update-rc.d -f ' + service_name + '.autostart remove')
    			os.remove('/etc/init.d/' + service_name + '.autostart')

    		os.system('sudo service ' + service_name + 'stop')
    		os.remove('/lib/systemd/system/' + service_name + '.service')

    os.system('sudo rm -R /var/python/')
else:
    print('No services were found.')

print('The system has been completely uninstalled.')
