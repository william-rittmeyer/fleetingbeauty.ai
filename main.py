import os
import sys
import time

def check_wifi_connection():
    # Check if the Raspberry Pi Zero W is connected to Wi-Fi
    output = os.popen('iwgetid -r').read()
    if output.strip() == '':
        return False
    else:
        return True

def prompt_change_wifi_credentials():
    # Prompt user to change Wi-Fi credentials
    while True:
        response = input('Wi-Fi credentials already present. Do you want to change them? (yes/no) ')
        if response.lower() == 'yes':
            ssid = input("Enter Wi-Fi SSID: ")
            password = input("Enter Wi-Fi password: ")
            write_wifi_config_to_file(ssid, password)
            print('Wi-Fi credentials changed.')
            break
        elif response.lower() == 'no':
            break
        else:
            print('Invalid input. Please enter "yes" or "no".')

def write_wifi_config_to_file(ssid, password):
    # Write Wi-Fi configuration to wpa_supplicant.conf file
    with open('/Volumes/boot/wpa_supplicant.conf', 'w') as f:
        f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
        f.write('update_config=1\n')
        f.write('country=US\n\n')
        f.write('network={\n')
        f.write(f'\tssid="{ssid}"\n')
        f.write(f'\tpsk="{password}"\n')
        f.write('}')

if __name__ == '__main__':
    # Check if the Raspberry Pi Zero W is connected to a monitor or a computer
    if os.environ.get('DISPLAY'):
        # Check if the Raspberry Pi Zero W is connected to Wi-Fi
        if check_wifi_connection():
            # Execute generate.py
            os.system('python listen.py')
        else:
            print('Error: Raspberry Pi Zero W is not connected to Wi-Fi. Before connecting to display monitor please connect to computer/laptop to input wifi credentials')
    else:
        print('Waiting for Raspberry Pi Zero W to become available...')
        while not os.path.exists('/Volumes/boot'):
            time.sleep(1)
        print('Raspberry Pi Zero W detected.')
        
        # Check if Wi-Fi credentials are already present
        if os.path.exists('/Volumes/boot/wpa_supplicant.conf'):
            prompt_change_wifi_credentials()
        else:
            ssid = input("Enter Wi-Fi SSID: ")
            password = input("Enter Wi-Fi password: ")
            write_wifi_config_to_file(ssid, password)
            print('Wi-Fi credentials saved to wpa_supplicant.conf.')
        
        # Eject boot partition
        os.system('diskutil unmountDisk /dev/disk2')

