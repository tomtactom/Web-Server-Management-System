import os
import re
import csv
import time
from os import sys
from sys import platform
#test

if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

if not len(sys.argv) >= 3:
    print('Specify at least two parameters. $python script.py example.com mail@example.com [1|true|True|redirect](optional)')
    quit()

domainname = sys.argv[1]
mail = sys.argv[2]
if len(sys.argv) >= 4:
    redirect = sys.argv[3]
else:
    redirect = False

if not os.geteuid() == 0:
    print('You need root rights to start the script')

except_minus = True
for i in list(domainname):
    if i == '-' and except_minus:
        except_minus = False

        if not re.search("[abcdefghijklmnopqrstuvwxyz0123456789\-.]", i):
            print("NoValidSubname: Subdomain contains invalid characters")
            quit()

    else:
        if not re.search("[abcdefghijklmnopqrstuvwxyz0123456789.]", i):
            print("NoValidSubname: Subdomain contains invalid characters, the minus sign may only be used once")
            quit()
if list(domainname)[0] == '-' or list(domainname)[2] == '-' or list(domainname)[-1] == '-':
    print('NoValidSubname: The domainname may contain a "-" at the first, third, fourth and last place')
    quit()

if len(domainname) >= 63:
    print('NotValidSubname: The domainname can not be more than 63 characters long')
    quit()

if not re.search("^[\w\.\+\-]+\@[\w\-]+\.[a-z]{2,3}$", mail):
    print('NotValidEmail: This is not a valid e-mail address')
    quit()

if len(mail) > 128:
    print('NotValidEmail: The e-mail address may be up to 128 characters long')
    quit()

if redirect == '1' or redirect == 'true' or redirect == 'True' or redirect == 'redirect':
    redirect = True
    redirection = '1'
else:
    redirect = False
    redirection = '0'

os.makedirs('/var/www/' + domainname + '/httpd')
os.system('sudo chmod -R 777 /var/www/' + domainname)
with open('/etc/apache2/sites-available/' + domainname + '.conf', 'w') as file:
    file.write('<VirtualHost *:80>\n')
    file.write('    ServerName ' + domainname + '\n')
    file.write('    ServerAlias ' + domainname + '\n')
    file.write('    DocumentRoot /var/www/' + domainname + '/httpd\n')
    file.write('    <Directory /var/www/' + domainname + '/>\n')
    file.write('        AllowOverride All\n')
    file.write('    </Directory>\n')
    file.write('    ErrorLog ${APACHE_LOG_DIR}/' + domainname + '_error.log\n')
    file.write('    CustomLog ${APACHE_LOG_DIR}/' + domainname + '_access.log combined\n')
    file.write('</VirtualHost>\n')

os.system('sudo a2ensite ' + domainname + '.conf')
os.system('sudo systemctl reload apache2')
os.system('sudo letsencrypt --apache -d ' + domainname + ' --agree-tos -m ' + mail + ' --no-eff-email --no-redirect')
os.system('(crontab -u user -l ; echo "0 1 16 * * sudo letsencrypt --apache -d ' + domainname + ' --agree-tos -m ' + mail + ' --no-eff-email --no-redirect --renew-by-default") | crontab -u user -')
if redirect == True:
    with open('/var/www/' + domainname + '/.htaccess', 'w') as file:
        file.write('RewriteEngine On\n')
        file.write('RewriteCond %{HTTPS} !=on\n')
        file.write('RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n')

    os.system('sudo chmod 777 /var/www/' + domainname + '/.htaccess')

w = csv.writer(open('/var/www/' + domainname + '/.data.csv', 'w'))
w.writerow(['creation_timestamp', 'domainname', 'mail', 'redirection'])
w.writerow([time.strftime("%d.%m.%Y %H:%M:%S"), domainname, mail, redirection])
os.system('sudo chmod 777 /var/www/' + domainname + '/.data.csv')
