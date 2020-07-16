# Module importieren
import os
from os import sys
from sys import platform
import zipfile
import urllib.request
import string
import random
from shutil import copyfile

# Das Script nur auf Linux laufen lassen
if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

# Überprüfe ob der Nutzer Root Rechte hat
if not os.geteuid() == 0:
    print('You need root rights to start the script. Try sudo :)')
    quit()

# Überprüfen ob alle Parameter angegeben werden
if not len(sys.argv) >= 3:
    print('Specify at least one parameters. $python script.py domainname mail@example.com')
    quit()
else:
    domainname = sys.argv[1]
    mail = sys.argv[2]

# Überprüfe ob config_sample.zip vorhanden ist
if not 'config_site.zip' in os.listdir('./'):
    print('The file "config_sample.zip" is missing. Please make sure that it is in the same directory as this file.')
    quit()

# Überprüfe ob bereits Dateien im vHost Verzeichnisordner sind
if 'www' in os.listdir('/var/'):
    print('There are still files in the /var/www/ folder. So that everything works smoothly, please make a backup manually and delete the files. Please delete the /www/ folder.')
    quit()

if 'apache2' in os.listdir('/etc/') or 'php' in os.listdir('/etc/'):
    decision = input('You have installed PHP and/or Apache2. The prerequisite for this system is that neither is installed. Attention, settings can be lost. Please make a backup if necessary. Should PHP and Apache be reinstalled? Type \'yes\' (recommended) or \'no\':')
    if 'yes' == decision or 'y' == decision:
        os.system('sudo apt purge apache2 -y')
        os.system('sudo apt purge php* -y')
        os.system('sudo rm -R /etc/apache2')
        os.system('sudo rm -R /etc/php')
    else:
        print('Unfortunately the program cannot be installed')
        quit()



# Apache, PHP, MySQL (MariaDB) und Certbot (letsencrypt) installieren
os.system('sudo apt install apache2 -y')
os.system('sudo apt install php7.3 php7.3-mysql php7.3-curl php7.3-gd php7.3-zip php7.3-fpm php7.3-cli php7.3-opcache php7.3-json php7.3-mbstring php7.3-xml libapache2-mod-php7.3 php-common -y')
os.system('sudo apt install mariadb-client mariadb-server mysql-common -y')
os.system('sudo apt install certbot letsencrypt python-certbot-apache -y')

# Schreibe die Datei um neue Subdomains anzulegen
with open('/etc/apache2/new_subdomain.py', 'w') as file:
    file.write('import os\n')
    file.write('import re\n')
    file.write('import csv\n')
    file.write('import time\n')
    file.write('from os import sys\n')
    file.write('from sys import platform\n')
    file.write('\n')
    file.write('domainname = \'' + str(domainname) + '\'\n')
    file.write('if not platform == "linux" and not platform == "linux2":\n')
    file.write('    print(\'This script only works on Linux systems\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if not len(sys.argv) >= 3:\n')
    file.write('    print(\'Specify at least two parameters. $python script.py subname mail@example.com [1|true|True|redirect](optional)\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('subname = sys.argv[1]\n')
    file.write('mail = sys.argv[2]\n')
    file.write('if len(sys.argv) >= 4:\n')
    file.write('    redirect = sys.argv[3]\n')
    file.write('else:\n')
    file.write('    redirect = False\n')
    file.write('\n')
    file.write('if not os.geteuid() == 0:\n')
    file.write('    print(\'You need root rights to start the script\')\n')
    file.write('\n')
    file.write('except_minus = True\n')
    file.write('for i in list(subname):\n')
    file.write('    if i == \'-\' and except_minus:\n')
    file.write('        except_minus = False\n')
    file.write('\n')
    file.write('        if not re.search("[abcdefghijklmnopqrstuvwxyz0123456789\-]", i):\n')
    file.write('            print("NoValidSubname: Subdomain contains invalid characters")\n')
    file.write('            quit()\n')
    file.write('\n')
    file.write('    else:\n')
    file.write('        if not re.search("[abcdefghijklmnopqrstuvwxyz0123456789]", i):\n')
    file.write('            print("NoValidSubname: Subdomain contains invalid characters, the minus sign may only be used once")\n')
    file.write('            quit()\n')
    file.write('if list(subname)[0] == \'-\' or list(subname)[2] == \'-\' or list(subname)[3] == \'-\' or list(subname)[-1] == \'-\':\n')
    file.write('    print(\'NoValidSubname: The subname may contain a "-" at the first, third, fourth and last place\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if len(subname + \'.\' + domainname) >= 63:\n')
    file.write('    print(\'NotValidSubname: The subname can not be more than \' + str(63 - len(\'.\' + domainname) - 1) + \' characters long\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if not re.search("^[\w\.\+\-]+\@[\w\-]+\.[a-z]{2,3}$", mail):\n')
    file.write('    print(\'NotValidEmail: This is not a valid e-mail address\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if len(mail) > 128:\n')
    file.write('    print(\'NotValidEmail: The e-mail address may be up to 128 characters long\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if redirect == \'1\' or redirect == \'true\' or redirect == \'True\' or redirect == \'redirect\':\n')
    file.write('    redirect = True\n')
    file.write('    redirection = \'1\'\n')
    file.write('else:\n')
    file.write('    redirect = False\n')
    file.write('    redirection = \'0\'\n')
    file.write('\n')
    file.write('os.makedirs(\'/var/www/\' + subname + \'.\' + domainname + \'/httpd\')\n')
    file.write('os.system(\'sudo chmod -R 777 /var/www/\' + subname + \'.\' + domainname)\n')
    file.write('with open(\'/etc/apache2/sites-available/\' + subname + \'.\' + domainname + \'.conf\', \'w\') as file:\n')
    file.write('    file.write(\'<VirtualHost *:80>\\n\')\n')
    file.write('    file.write(\'    ServerName \' + subname + \'.\' + domainname + \'\\n\')\n')
    file.write('    file.write(\'    ServerAlias \' + subname + \'.\' + domainname + \'\\n\')\n')
    file.write('    file.write(\'    DocumentRoot /var/www/\' + subname + \'.\' + domainname + \'/httpd\\n\')\n')
    file.write('    file.write(\'    <Directory /var/www/\' + subname + \'.\' + domainname + \'/>\\n\')\n')
    file.write('    file.write(\'        AllowOverride All\\n\')\n')
    file.write('    file.write(\'    </Directory>\\n\')\n')
    file.write('    file.write(\'    ErrorLog ${APACHE_LOG_DIR}/\' + subname + \'.\' + domainname + \'_error.log\\n\')\n')
    file.write('    file.write(\'    CustomLog ${APACHE_LOG_DIR}/\' + subname + \'.\' + domainname + \'_access.log combined\\n\')\n')
    file.write('    file.write(\'</VirtualHost>\\n\')\n')
    file.write('\n')
    file.write('os.system(\'sudo a2ensite \' + subname + \'.\' + domainname + \'.conf\')\n')
    file.write('os.system(\'sudo systemctl reload apache2\')\n')
    file.write('os.system(\'sudo letsencrypt --apache -d \' + subname + \'.\' + domainname + \' --agree-tos -m \' + mail + \' --no-eff-email --no-redirect\')\n')
    file.write('os.system(\'(crontab -u pi -l ; echo "0 1 16 * * sudo letsencrypt --apache -d \' + subname + \'.\' + domainname + \' --agree-tos -m \' + mail + \' --no-eff-email --no-redirect --renew-by-default") | crontab -u pi -\')\n')
    file.write('if redirect == True:\n')
    file.write('    with open(\'/var/www/\' + subname + \'.\' + domainname + \'/.htaccess\', \'w\') as file:\n')
    file.write('        file.write(\'RewriteEngine On\\n\')\n')
    file.write('        file.write(\'RewriteCond %{HTTPS} !=on\\n\')\n')
    file.write('        file.write(\'RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\\n\')\n')
    file.write('\n')
    file.write('    os.system(\'sudo chmod 777 /var/www/\' + subname + \'.\' + domainname + \'/.htaccess\')\n')
    file.write('\n')
    file.write('w = csv.writer(open(\'/var/www/\' + subname + \'.\' + domainname + \'/.data.csv\', \'w\'))\n')
    file.write('w.writerow([\'creation_timestamp\', \'subname\', \'domainname\', \'mail\', \'redirection\'])\n')
    file.write('w.writerow([time.strftime("%d.%m.%Y %H:%M:%S"), subname, domainname, mail, redirection])\n')
    file.write('os.system(\'sudo chmod 777 /var/www/\' + subname + \'.\' + domainname + \'/.data.csv\')\n')
    file.write('\n')

# Schreibe die Datei um eine automatische Weiterleitung (an https://) per .htaccess vorzunehmen
with open('/etc/apache2/add_https_redirect.py', 'w') as file:
    file.write('import os\n')
    file.write('import re\n')
    file.write('import csv\n')
    file.write('import time\n')
    file.write('from os import sys\n')
    file.write('from sys import platform\n')
    file.write('\n')
    file.write('domainname = \'' + str(domainname) + '\'\n')
    file.write('if not platform == "linux" and not platform == "linux2":\n')
    file.write('    print(\'This script only works on Linux systems\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if not len(sys.argv) == 2:\n')
    file.write('    print(\'Specify at least one parameter. $python script.py subname\')\n')
    file.write('    quit()\n')
    file.write('else:\n')
    file.write('    subname = sys.argv[1]\n')
    file.write('\n')
    file.write('if not os.path.isdir(\'/var/www/\' + subname + \'.\' + domainname):\n')
    file.write('    print(\'This subdomain does not exist\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('with open(\'/var/www/\' + subname + \'.\' + domainname + \'/.htaccess\', \'w\') as file:\n')
    file.write('    file.write(\'RewriteEngine On\\n\')\n')
    file.write('    file.write(\'RewriteCond %{HTTPS} !=on\\n\')\n')
    file.write('    file.write(\'RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\\n\')\n')
    file.write('\n')
    file.write('os.system(\'sudo chmod 777 /var/www/\' + subname + \'.\' + domainname + \'/.htaccess\')\n')
    file.write('\n')
    file.write('with open(\'/var/www/\' + subname + \'.\' + domainname + \'/.data.csv\') as csvfile:\n')
    file.write('    data = csvfile.readlines()\n')
    file.write('    value = []\n')
    file.write('    for i in data:\n')
    file.write('        value.append(data[1].replace(\'\\r\\n\', \'\').split(\',\'))\n')
    file.write('    value = value[0]\n')
    file.write('\n')
    file.write('w = csv.writer(open(\'/var/www/\' + subname + \'.\' + domainname + \'/.data.csv\', \'w\'))\n')
    file.write('w.writerow([\'creation_timestamp\', \'subname\', \'domainname\', \'mail\', \'redirection\'])\n')
    file.write('w.writerow([value[0], value[1], value[2], value[3], \'1\'])\n')
    file.write('print(\'The forwarding was successfully established\')\n')
    file.write('\n')

# Schreibe die Datzei um ein manuelles Backup zu machen
with open('/etc/apache2/make_manually_backup.py', 'w') as file:
    file.write('import os\n')
    file.write('import re\n')
    file.write('import csv\n')
    file.write('import time\n')
    file.write('from os import sys\n')
    file.write('from sys import platform\n')
    file.write('\n')
    file.write('domainname = \'' + str(domainname) + '\'\n')
    file.write('if not platform == "linux" and not platform == "linux2":\n')
    file.write('    print(\'This script only works on Linux systems\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if not len(sys.argv) == 2:\n')
    file.write('    print(\'Specify at least one parameter. $python script.py subname\')\n')
    file.write('    quit()\n')
    file.write('else:\n')
    file.write('    subname = sys.argv[1]\n')
    file.write('\n')
    file.write('if not os.path.isdir(\'/var/www/\' + subname + \'.\' + domainname):\n')
    file.write('    print(\'This subdomain does not exist\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('zip_name = \'backup_\' + subname + \'.\' + domainname + \'_\' + time.strftime(\'%Y_%m_%d_%H_%M_%S\') + \'_manually.zip\'\n')
    file.write('Zip = zipfile.ZipFile(\'/var/tmp/\' + zip_name, \'a\')\n')
    file.write('counter = 0\n')
    file.write('for dirname,dirs,filenames in os.walk(\'/var/www/\' + subname + \'.\' + domainname + \'/httpd\'):\n')
    file.write('    for filename in filenames:\n')
    file.write('        counter = counter + counter\n')
    file.write('        Zip.write(os.path.join(dirname,filename))\n')
    file.write('\n')
    file.write('Zip.close()\n')
    file.write('os.system(\'sudo mv /var/tmp/\' + zip_name + \' /var/www/config.\' + domainname + \'/httpd/backups/\' + zip_name)\n')
    file.write('print(zip_name)\n')
    file.write('\n')

# Schreibe die Datei um .htaccess Dateien zu entfernen (insbesondere um die https:// weiterleitung zu entfernen)
with open('/etc/apache2/remove_https_redirect.py', 'w') as file:
    file.write('import os\n')
    file.write('import csv\n')
    file.write('from os import sys\n')
    file.write('from sys import platform\n')
    file.write('\n')
    file.write('domainname = \'' + str(domainname) + '\'\n')
    file.write('if not platform == "linux" and not platform == "linux2":\n')
    file.write('    print(\'This script only works on Linux systems\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if not len(sys.argv) == 2:\n')
    file.write('    print(\'Specify at least one parameter. $python script.py subname\')\n')
    file.write('    quit()\n')
    file.write('else:\n')
    file.write('    subname = sys.argv[1]\n')
    file.write('\n')
    file.write('if not os.path.isdir(\'/var/www/\' + subname + \'.\' + domainname):\n')
    file.write('    print(\'This subdomain does not exist\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('with open(\'/var/www/\' + subname + \'.\' + domainname + \'/.data.csv\') as csvfile:\n')
    file.write('    data = csvfile.readlines()\n')
    file.write('    value = []\n')
    file.write('    for i in data:\n')
    file.write('        value.append(data[1].replace(\'\\r\\n\', \'\').split(\',\'))\n')
    file.write('    value = value[0]\n')
    file.write('\n')
    file.write('w = csv.writer(open(\'/var/www/\' + subname + \'.\' + domainname + \'/.data.csv\', \'w\'))\n')
    file.write('w.writerow([\'creation_timestamp\', \'subname\', \'domainname\', \'mail\', \'redirection\'])\n')
    file.write('w.writerow([value[0], value[1], value[2], value[3], \'0\'])\n')
    file.write('\n')
    file.write('os.system(\'sudo rm /var/www/\' + subname + \'.\' + domainname + \'/.htaccess\')\n')
    file.write('print("The redirect was successfully removed")\n')
    file.write('\n')

# Schreibe die Datei um Subdomains zu löschen
with open('/etc/apache2/remove_subdomain.py', 'w') as file:
    file.write('import os\n')
    file.write('import csv\n')
    file.write('from os import sys\n')
    file.write('from sys import platform\n')
    file.write('\n')
    file.write('domainname = \'' + str(domainname) + '\'\n')
    file.write('if not platform == "linux" and not platform == "linux2":\n')
    file.write('    print(\'This script only works on Linux systems\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('if not len(sys.argv) == 2:\n')
    file.write('    print(\'Specify at least one parameter. $python script.py subname\')\n')
    file.write('    quit()\n')
    file.write('else:\n')
    file.write('    subname = sys.argv[1]\n')
    file.write('\n')
    file.write('if not os.path.isdir(\'/var/www/\' + subname + \'.\' + domainname):\n')
    file.write('    print(\'This subdomain does not exist\')\n')
    file.write('    quit()\n')
    file.write('\n')
    file.write('with open(\'/var/www/\' + subname + \'.\' + domainname + \'/.data.csv\') as csvfile:\n')
    file.write('    data = csvfile.readlines()\n')
    file.write('    value = []\n')
    file.write('    for i in data:\n')
    file.write('        value.append(data[1].replace(\'\\r\\n\', \'\').split(\',\'))\n')
    file.write('    value = value[0]\n')
    file.write('\n')
    file.write('mail = value[3]\n')
    file.write('os.system(\'sudo rm -R /var/www/\' + subname + \'.\' + domainname)\n')
    file.write('os.system(\'sudo rm /etc/apache2/sites-available/\' + subname + \'.\' + domainname + \'.conf\')\n')
    file.write('os.system(\'sudo rm /etc/apache2/sites-enabled/\' + subname + \'.\' + domainname + \'.conf\')\n')
    file.write('\n')
    file.write('os.system(\'sudo systemctl reload apache2\')\n')
    file.write('os.system(\'sudo letsencrypt delete --cert-name \' + subname + \'.\' + domainname)\n')
    file.write('os.system(\'sudo rm /etc/apache2/sites-available/\' + subname + \'.\' + domainname + \'-le-ssl.conf\')\n')
    file.write('os.system(\'sudo rm /etc/apache2/sites-enabled/\' + subname + \'.\' + domainname + \'-le-ssl.conf\')\n')
    file.write('os.system(\'sudo systemctl reload apache2\')\n')
    file.write('\n')
    file.write('os.system(\'crontab -u pi -l | grep -v "sudo letsencrypt --apache -d \' + subname + \'.\' + domainname + \' --agree-tos -m \' + mail + \' --no-eff-email --no-redirect --renew-by-default"  | crontab -u pi -\')\n')
    file.write('\n')

# Schreibe die Hauptdomain config Datei
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

# Verzeichnisse für die Hauptdomain anlegen
os.mkdir('/var/www/' + domainname)
os.mkdir('/var/www/' + domainname + '/httpd')
os.system('sudo a2ensite ' + domainname + '.conf')
os.system('sudo systemctl reload apache2')

# Let's Encrypt für die Hauptdomain einrichten
os.system('sudo letsencrypt --apache -d ' + domainname + ' --agree-tos -m ' + mail + ' --no-eff-email --no-redirect')
os.system('(crontab -u pi -l ; echo "0 1 16 * * sudo letsencrypt --apache -d ' + domainname + ' --agree-tos -m ' + mail + ' --no-eff-email --no-redirect --renew-by-default") | crontab -u pi -')

# Schreibe die phpMyAdmin config Datei
with open('/etc/apache2/sites-available/phpmyadmin.conf', 'w') as file:
    file.write('<VirtualHost *:80>\n')
    file.write('      ServerName phpmyadmin\n')
    file.write('      ServerAlias phpmyadmin.*\n')
    file.write('      DocumentRoot /var/www/phpmyadmin/httpd\n')
    file.write('      <Directory /var/www/phpmyadmin/>\n')
    file.write('            AllowOverride All\n')
    file.write('      </Directory>\n')
    file.write('      ErrorLog ${APACHE_LOG_DIR}/phpmyadmin_error.log\n')
    file.write('      CustomLog ${APACHE_LOG_DIR}/phpmyadmin_access.log combined\n')
    file.write('</VirtualHost>\n')

# Verzeichnisse für die phpMyAdmin Seite anlegen
root_path = '/var/www/phpmyadmin/'
os.mkdir(root_path)
os.system('sudo a2ensite phpmyadmin.conf')
os.system('sudo systemctl reload apache2')

# Let's Encrypt für phpMyAdmin einrichten
os.system('sudo letsencrypt --apache -d phpmyadmin.' + domainname + ' --agree-tos -m ' + mail + ' --no-eff-email --no-redirect')
os.system('(crontab -u pi -l ; echo "0 1 16 * * sudo letsencrypt --apache -d phpmyadmin.' + domainname + ' --agree-tos -m ' + mail + ' --no-eff-email --no-redirect --renew-by-default") | crontab -u pi -')

# Lade die neuste Version von phpMyAdmin herunter
urllib.request.urlretrieve('https://www.phpmyadmin.net/downloads/phpMyAdmin-latest-all-languages.zip', root_path + 'phpMyAdmin-latest-all-languages.zip')

# Entpacke die phpMyAdmin-latest-all-languages.zip
with zipfile.ZipFile(root_path + 'phpMyAdmin-latest-all-languages.zip', 'r') as zfile:
    zfile.extractall(root_path)

# Die entpackte Zip-Datei löschen
os.remove(root_path + 'phpMyAdmin-latest-all-languages.zip')

# Ordner aus phpMyAdmin-latest-all-languages.zip in 'httpd' umbenennen und config.sample.inc.php zu config.inc.php erstellen
directory = os.listdir(root_path)[0]
os.rename(root_path + directory, root_path + 'httpd')
copyfile(root_path + 'httpd/config.sample.inc.php', root_path + 'httpd/config.inc.php')
with open(root_path + 'httpd/config.inc.php', 'r') as file:
    config_file = file.read()

# Blowfish secret und Sprache einstellen
config_file = config_file.split("$cfg['blowfish_secret'] = '';")
config_file = config_file[0] + "$cfg['blowfish_secret'] = '" + "".join(random.choices(string.ascii_letters + string.digits, k=32)) + "';" + config_file[1];
config_file = config_file.split("//$cfg['DefaultLang'] = 'de';")
config_file = config_file[0] + "$cfg['DefaultLang'] = 'de';\n$cfg['Servers'][$i]['AllowRoot'] = true;\n$cfg['TempDir'] = '/var/www/phpmyadmin/httpd/tmp/';\n$cfg['Servers'][$i]['hide_db'] = '(information_schema|phpmyadmin|mysql|performance_schema)';\n" + config_file[1];
with open(root_path + 'httpd/config.inc.php', 'w') as file:
    file.write(''.join(config_file))

os.mkdir('/var/www/phpmyadmin/httpd/tmp/')
# Automatische Weiterleitung für phpMyAdmin einrichten
with open(root_path + '.htaccess', 'w') as file:
    file.write('RewriteEngine On\n')
    file.write('RewriteCond %{HTTPS} !=on\n')
    file.write('RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n')

# config Subdomain anlegen
os.system('sudo python3 /etc/apache2/new_subdomain.py config ' + mail + ' true')
# Inhalt aus der config_site.zip in den httpd Ordner der config Subdomain entpacken
with zipfile.ZipFile('config_site.zip', 'r') as zfile:
    zfile.extractall('/var/www/config.' + domainname + '/httpd/')

os.system('sudo a2enmod auth_basic')
os.system('sudo a2enmod auth_digest')
os.system('sudo a2enmod autoindex')
os.system('sudo a2enmod rewrite')
os.system('sudo a2enmod webdav')
os.system('sudo systemctl reload apache2')

print("1. Drücke ENTER")
print("2. Gebe 'y' ein")
print("3. Gebe dein Root Passwort ein")
print("4. Gebe dein Root Passwort erneut ein")
print("5. Gebe 'y' ein")
print("6. Gebe 'n' ein")
print("7. Gebe 'y' ein")
print("8. Gebe 'y' ein")
os.system('sudo mysql_secure_installation')
os.system('sudo /etc/init.d/mysql restart')
print('MySQL konfigurieren...')
print('Bitte geben das Root Passwort ein')
os.system('sudo mysql -u root -p -e "use mysql; update user set plugin=\'\' where user=\'root\'; flush privileges;"')

# Die Berechtigung geben, dass auf die Dateien Zugegriffen werden kann (wenig Sicherheit = viel Freiheit)
os.system('sudo chmod -R 777 /etc/apache2')
os.system('sudo chmod -R 777 /var/www')
os.system('sudo chown -R pi:pi /var/www')
os.system('sudo chmod 755 /var/www/phpmyadmin/httpd/config.inc.php')
print('FERTIG')
print('')
print('#########################')
print('Bitte füge folgende Berechtigung in deine visudo Datei in die letzte Spalte.')
print('Gebe dazu den Befehl "sudo visudo" ein.')
print('####################')
print('')
print('www-data ALL=(ALL) NOPASSWD: ALL')
print('')
print('####################')
print('Dein System ist nicht gerade sicher und wenn du in deinem Code einen Fehler machst, kann ein Angreifer leicht die Kontrolle über deinen Pi übernehmen. Bitte achte also darauf, dass du selber für deinen Code verantwortlich bist. Der Vorteil dabei ist, dass du extrem viele Freiheiten hast.')
print('####################')
print('🅲🆁🅴🅳🅸🆃🆂')
print('Github: https://github.com/12tom12')
