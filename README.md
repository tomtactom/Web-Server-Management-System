# Web Server Management System - Webserver Verwaltungssystem
> Ein Webserver Verwaltungssystem für deinen Homeserver (z. B. Raspberry Pi). Erstelle Subdomains, nutze Apache, PHP, MySQL, PhpMyAdmin, SSH-Konsole, Dateimanager, Certbot/Letsencrypt, GitHub + Webhook-Link & Python-Dienste vollautomatisch. Egal ob statische oder dynamische IP.

![](https://repository-images.githubusercontent.com/242197618/84720600-f616-11ea-83d6-a143e05564cc)
Hiermit kannst du in Kombination mit einem Dynamischen DNS Service oder einer Domain in kombination einer statischen IP deinen Linux Server als Webserver von zu Hause aus laufen lassen.

## Voraussetzungen
* Deutsch Kenntnisse, da das gesamte System auf Deutsch läuft. (Knowledge of German, as the entire system runs in German.)
* Ein internetfähiger Linuxbasierter Computer + Root Rechte (Am besten mit Debian o. ä.)
* Zugriff auf die Router Einstellungen (Ein Router wie FRITZ!Box oder Speedport wird benötigt.)
* Python, PHP & GitHub Kenntnisse (optional)
* Kenntnisse im Umgang mit der Shell Konsole & grundlegende Erfahrung in der Webentwicklung

## Installation
Für alle auf Debian basierenden Systeme:

Die E-Mail-Adresse wird für Let's Encrypt benötigt

Wenn du eine Dynamische IP und keinen Dynamischen DNS Service hast (Wenn du nicht weißt worum es geht, nehme diese Option):
* Du kannst [ddnss.de](https://ddnss.de/) benutzen
* Erstelle dir dort einen Account
* Registriere dir eine dynamische Domain. Z. B. [example.ddnss.de](http://example.ddnss.de/)
* Wichtig: Setze auf der Seite [ddnss.de/ua/vhosts_list.php](https://ddnss.de/ua/vhosts_list.php) bei der Checkbox "Wildcard :" einen Haken.
* Richte die dynamische DNS bei deinem Router ein (z. B. Fritz!Box). Eine entsprechende Anleitung findest du auf [ddnss.de/ua/help.php](https://ddnss.de/ua/help.php).
* Leite alle Anfragen über die Domain für die Ports 80 und 443 an deinen Server weiter. (Portfreigabe)
Stelle sicher, dass alles Funktioniert. Es gibt keine automatische Überprüfung mehr.

Wenn du eine statische IP und eine Domain hast:
* Richte einen A-Type für deine Domain auf die Statische IP ein, die auf das Netzwerk von dem Server angemeldet ist.
* Wichte einen Wildcard Eintrag für deine Domain ein.
* Sollte dies nicht gehen, musst du mindestens die Subdomains config.* und phpmyadmin.* einrichten.
* Beim Erstellen neuer Subdomains, muss die Konfiguration bei den DNS-Einstellungen manuell vorgenommen werden
* Leite alle Anfragen über die Domain für die Ports 80 und 443 an deinen Server weiter. (Portfreigabe)
Stelle sicher, dass alles Funktioniert. Es gibt keine automatische Überprüfung mehr.

```sh
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y
sudo apt install git
sudo apt purge apache*
sudo apt purge php*
sudo apt purge mysql*
sudo apt purge letsencrypt* certbot*
sudo rm -R /etc/apache2
```

Für die Release-Version (Stabil, allerdings nicht die neuste)(empfohlen)
```sh
wget https://github.com/12tom12/web-server-management-system/releases/download/0.2.1/web-server-management-system-master-0.2.1.zip
unzip web-server-management-system-master-0.2.1.zip
rm web-server-management-system-master-0.2.1.zip
cd ./Web-Server-Management-System-master
sudo python3 main.py example.com mail@example.com
```

Für die Beta-Version (Instabil, allerdings immer die neuste)
```sh
git clone https://github.com/12tom12/Web-Server-Management-System.git
cd ./Web-Server-Management-System
sudo python3 main.py example.com mail@example.com
```

Es müssen manuell noch einige Einstellungen während der Installation vorgenommen werden (z. B. Passwort Eingabe usw.). Achte dabei auch auf die Anweisungen im Installationsscript.

Wenn alles installiert wurde, gehe auf [config.example.com](https://config.example.com) und gebe das Passwort "start" ein.

## Anwendungsbeispiele
Dieses Script ist durch seine geringe Sicherheit nicht für wichtige öffentliche Projekte gedacht, sondern zum privaten Entwickeln.
* Webserver zum Ausprobieren
* Python Scripte mit Webseiten verknüpfen
* Webentwicklung lernen
* SSH-Konsole nutzen

## Release History

* 0.1.0
    * CHANGE: System has been completed
* 0.1.1 - pre Release
    * CHANGE: Instructions to allow the user www-data via visudo sudo rights
    * ADD: Credit information
* 0.2.0
    * CHANGE: Works on more Linux systems
    * CHANGE: Files optimized
    * CHANGE: Bug fix
    * ADD: Python services added
    * CHANGE: Add all possible domains
    * CHANGE: Optimized for static IPs
    * ADD: Clone directly from GitHub
    * ADD: Webhook link management
* 0.2.1 - Release
    * CHANGE: Bug fix (installation)
    * CHANGE: Optimise README.md
* 0.3.0
    * ADD: Automatic update function via GitHub Webhook (for auto update: please contact me)
    * CHANGE: Many Bugfixes
    * CHANGE: Webhook copy bugfix (JavaScript)
    * CHANGE: Bugfix: Overwrite password by update & more password security
    * CHANGE: Responsive Design
    * ADD: New Font
    * ADD: WebSSH Console
    * ADD: Responsive Header and Footer & Menu
    * ADD: Social Media Buttons
    * ADD: Logout Button
    * ADD: Tiny File Manager (Thanks [@prasathmani](https://github.com/prasathmani))
    * CHANGE: In German we say "Entmüllt"

## Meta
Entwickler:
Tom – [GITHUB - tomtactom](https://github.com/tomtactom)
