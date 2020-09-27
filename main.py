# Module importieren Test123
import os
from os import sys
from sys import platform
import zipfile
import urllib.request
import string
import random
from shutil import copyfile
import subprocess

# Das Script nur auf Linux laufen lassen
if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

# Überprüfe ob der Nutzer Root Rechte hat
if not os.geteuid() == 0:
    print('You need root rights to start the script. Try sudo :)')
    quit()

# Überprüfe ob bereits Dateien im vHost Verzeichnisordner sind
if 'www' in os.listdir('/var/'):
    for i in os.listdir('/var/www/'):
        if 'config.' == i[:7]:
            with open('/var/www/' + i + '/.data.csv') as file:
                mail = file.read().split(',')[-2]

            domainname = i.replace('config.', '')
            update_system = True
            print('Then an update will now be carried out.')
            break
        else:
            update_system = False

else:
    update_system = False

# Überprüfen ob alle Parameter angegeben werden
if update_system == False:
    if not len(sys.argv) >= 3:
        print('Specify at least one parameters. $python script.py example.com mail@example.com')
        quit()
    else:
        domainname = sys.argv[1]
        mail = sys.argv[2]
else:
    pass # Hier muss noch die Variable `domainname` und die Variable `mail` ausgelesen werden (z. B. aus einer .data.csv)

print(os.listdir('./'))
# Überprüfe ob config_sample vorhanden ist
if not 'httpd' in os.listdir('./'):
    print('The directory "config_sample" is missing. Please make sure that it is in the same directory as this file.')
    quit()

    if update_system == False:
        print('There are still files in the /var/www/ folder. The system has probably already been installed. So that everything works smoothly, please make a backup manually and delete the files. Please delete the /www/ folder.')
        quit()

if update_system == False:
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
if not 'apache2' in os.listdir('/etc/'):
    os.system('sudo apt install apache2 -y')

if not 'php' in os.listdir('/etc/'):
    os.system('sudo apt install php7.3 php7.3-mysql php7.3-curl php7.3-gd php7.3-zip php7.3-fpm php7.3-cli php7.3-opcache php7.3-json php7.3-mbstring php7.3-xml libapache2-mod-php7.3 php-common -y')

if not 'mysql' in os.listdir('/etc/'):
    os.system('sudo apt install mariadb-client mariadb-server mysql-common -y')

if not 'letsencrypt' in os.listdir('/etc/'):
    os.system('sudo apt install certbot letsencrypt python-certbot-apache -y')

#                                                                               Muss noch überprüft werden, ob die Dateien überschrieben werden
# Kopiere die Python-Dateien in den apache Ordner
for i in os.listdir('./python_scripts/'):
	if not i == '.' or not i == '..':
		copyfile('./python_scripts/' + i, '/etc/apache2/' + i)

# Lege die Hauptdomain an.
if update_system == False:
    os.system('sudo python3 /etc/apache2/new_domain.py ' + domainname + ' ' + mail + ' true')

# Schreibe die phpMyAdmin config Datei
if not 'phpmyadmin.conf' in os.listdir('/etc/apache2/sites-available/'):# Überprüfe ob PhpMyAdmin schon installiert ist
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
        os.system('(crontab -u www-data -l ; echo "0 1 16 * * sudo letsencrypt --apache -d phpmyadmin.' + domainname + ' --agree-tos -m ' + mail + ' --no-eff-email --no-redirect --renew-by-default") | crontab -u www-data -')

if update_system == False: # PHP PhpMyAdmin installieren
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

if update_system == False: # Nur wenn config Subdomain noch nicht existiert
    # config Subdomain anlegen
    os.system('sudo python3 /etc/apache2/new_domain.py config.' + domainname + ' ' + mail + ' true')

# Auch als Update
# Inhalt aus httpd (config_site) in den httpd Ordner der config Subdomain entpacken
os.system('sudo cp -r ./httpd/ /var/www/config.' + domainname + '/')

# enable apache2 modules
if not 'auth_basic.load' in os.listdir('/etc/apache2/mods-available'):
    os.system('sudo a2enmod auth_basic')

if not 'auth_digest.load' in os.listdir('/etc/apache2/mods-available'):
    os.system('sudo a2enmod auth_digest')

if not 'autoindex.load' in os.listdir('/etc/apache2/mods-available'):
    os.system('sudo a2enmod autoindex')

if not 'rewrite.load' in os.listdir('/etc/apache2/mods-available'):
    os.system('sudo a2enmod rewrite')

if not 'webdav.load' in os.listdir('/etc/apache2/mods-available'):
    os.system('sudo a2enmod webdav')

# Starte Apache neu
os.system('sudo systemctl reload apache2')

# Service-Dienste Pfad anlegen
if not os.path.isdir('/var/python'):
    os.mkdir('/var/python')

if not 'mysql' in os.listdir('/etc/'):
    # Letzte MySQL Einstellungen manuell festlegen
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

if not os.path.isdir('/var/python/webservermanagementsystem'):
    os.system('sudo python3 /etc/apache2/new_service.py webservermanagementsystem')
    os.system('cd /var/python/webservermanagementsystem ; git clone https://github.com/tomtactom/Web-Server-Management-System.git')
    os.system('sudo rm -R /var/python/webservermanagementsystem/docs')
    os.system('mv /var/python/webservermanagementsystem/Web-Server-Management-System /var/python/webservermanagementsystem/docs/')

# Die Berechtigung geben, dass auf die Dateien Zugegriffen werden kann (wenig Sicherheit = viel Freiheit)
os.system('sudo chmod -R 777 /etc/apache2')
os.system('sudo chmod -R 777 /var/www')
os.system('sudo chmod -R 777 /var/python')
os.system('sudo chown -R www-data:www-data /var/www')
os.system('sudo chown -R www-data:www-data /var/python')
if 'config.inc.php' in os.listdir('/var/www/phpmyadmin/httpd/'):
    os.system('sudo chmod 755 /var/www/phpmyadmin/httpd/config.inc.php')

if not subprocess.Popen(['id', '-Gn', 'www-data'], stdout=subprocess.PIPE).communicate()[0].decode('utf8').replace('www-data ', '').replace('\n', '') == 'sudo':
    os.system('sudo adduser www-data sudo')

print('FERTIG')
if update_system == False:
    print('')
    print('#########################')
    print('Bitte füge folgende Berechtigung in deine visudo Datei in die letzte Spalte.')
    print('Gebe dazu den Befehl "sudo visudo" ein.')
    print('####################')
    print('')
    #print('www-data ALL=(ALL) NOPASSWD: ALL')
    print('%sudo ALL=(ALL) NOPASSWD:ALL')
    print('')
    print('####################')
else:
    print('Das Update wurde erfolgreich installiert.')

print('Dein System ist nicht gerade sicher und wenn du in deinem Code einen Fehler machst, kann ein Angreifer leicht die Kontrolle über deinen Server übernehmen. Bitte achte also darauf, dass du selber für deinen Code verantwortlich bist. Der Vorteil dabei ist, dass du extrem viele Freiheiten hast.')
print('####################')
print('🅲🆁🅴🅳🅸🆃🆂')
print('Github: https://github.com/tomtactom')
