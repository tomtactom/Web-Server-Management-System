# Webserver Verwaltungssystem
> Ein Webserver Verwaltungssystem für deinen Homeserver (z. B. Raspberry Pi). Erstelle Subdomains, nutze Apache, PHP, MySQL, PhpMyAdmin, Certbot/Letsencrypt, GitHub + Webhook-Link & Python-Dienste vollautomatisch.

Hiermit kannst du in Kombination mit einem Dynamischen DNS Service deinen Linux Server als Webserver von zu Hause aus laufen lassen.

## Installation

Debian; Rasperian, Kali etc.:

The email address is used by letsencrypt

If you have a dynamic IP and no Dynamic DNS Service:
	You can Use [ddnss.de/](https://ddnss.de/)
	Register a Domain and setup your Domain on your Router
	!!!IMPORTANT!!!: at https://ddnss.de/ua/vhosts_list.php you have to set "Wildcard :" at True.
	Leite alle Anfragen über die Domain für die Ports 80 und 443 an deinen Server weiter.
	Make sure the domain is forwarded correctly. There is no subsequent check.

Else If you have a static IP and a Domain:
	You can use your Domain. You must open your Ports 80 and 443 at your Router and your Server.

```sh
sudo update && sudo upgrade -your
sudo apt install git
sudo apt purge apache*
sudo apt purge php*
sudo apt purge mysql*
sudo apt purge letsencrypt* certbot*
sudo rm -R /etc/apache2
mkdir webserververwaltungsystem
cd ./webserververwaltungsystem
git https://github.com/12tom12/webserververwaltungsystem.git
sudo python3 webserver_by_tom.py YOURDOMAINNAME mail@example.com
```
Follow the setup instruction


## Usage example

Dieses Script ist durch seine geringe Sicherheit nicht für wichtige öffentliche Projekte gedacht, sondern zum privaten entwickeln.

## Release History

* 0.1.0
    * CHANGE: System has been completed
* 0.1.1
    * CHANGE: Instructions to allow the user www-data via visudo sudo rights
    * ADD: Credit information
* 0.2.0
    * CHANGE: Works on more Linux systems
    * CHANGE: files optimized
    * CHANGE: bug fix
    * ADD: Python services added
    * CHANGE: Add all possible domains
    * CHANGE: Optimized for static IPs
    * ADD: clone directly from GitHub
    * ADD: Webhook link management

## Meta

Tom – [GITHUB - 12tom12](https://github.com/12tom12)
