import os
# Überprüfe ob der Nutzer Root Rechte hat
if os.geteuid() == 0:
    print('Please run this script with your standard user. Without sudo.')
    quit()

os.system('sudo pip install zipfile')
os.system('sudo pip install urllib')
os.system('sudo pip install string')
os.system('sudo pip install random')
os.system('sudo pip install shutil')
#with open('username.txt', 'w') as file:
#    file.write(str(os.system('whoami')))
