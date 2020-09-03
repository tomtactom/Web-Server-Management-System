import os
import re
import csv
import time
from os import sys
from sys import platform
import zipfile

if not platform == "linux" and not platform == "linux2":
    print('This script only works on Linux systems')
    quit()

if not len(sys.argv) == 3:
    print('Specify at least one parameter. $python script.py example.com standartdomainname.com')
    quit()
else:
    domainname = sys.argv[1]
    standartdomainname = sys.argv[2]

if not os.path.isdir('/var/www/' + domainname):
    print('This domain does not exist')
    quit()

zip_name = 'backup_' + domainname + '_' + time.strftime('%Y_%m_%d_%H_%M_%S') + '_manually.zip'
Zip = zipfile.ZipFile('/var/tmp/' + zip_name, 'a')
counter = 0
for dirname,dirs,filenames in os.walk('/var/www/' + domainname + '/httpd'):
    for filename in filenames:
        counter = counter + counter
        Zip.write(os.path.join(dirname,filename))

Zip.close()
os.system('sudo mv /var/tmp/' + zip_name + ' /var/www/config.' + standartdomainname + '/httpd/backups/' + zip_name)
print(zip_name)

