import os
import subprocess
import time

# Define the path to the wifi.txt file
txt_file_path = '/boot/wifi.txt'

# Define the path to the wpa_supplicant.conf file
conf_file_path = '/etc/wpa_supplicant/wpa_supplicant.conf'

# Read the contents of the wifi.txt file
with open(txt_file_path, 'r') as txt_file:
    txt_contents = txt_file.read()

# Read the contents of the wpa_supplicant.conf file
with open(conf_file_path, 'r') as conf_file:
    conf_contents = conf_file.read()

# Check if the contents of the files are different
if txt_contents != conf_contents:
    # Write the contents of the wifi.txt file to the wpa_supplicant.conf file
    with open(conf_file_path, 'w') as conf_file:
        conf_file.write(txt_contents)
    # Restart the networking service to apply the changes
    os.system('sudo service networking restart')
    print("WiFi credentials have been altered to match.")
else:
    print("WiFi credentials were the same.")


subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])
print('connected to Wifi network')
time.sleep(2)

os.system('python /boot/python/pygame_listen.py')
