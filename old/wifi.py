import subprocess

# Function to get Wi-Fi credentials from user
def get_wifi_credentials():
    ssid = input("Enter the Wi-Fi network name (SSID): ")
    password = input("Enter the Wi-Fi password: ")
    return ssid, password

# Function to update Wi-Fi configuration file with new credentials
def update_wifi_configuration(ssid, password):
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as f:
        f.write("\n\nnetwork={\n")
        f.write(f'\tssid="{ssid}"\n')
        f.write(f'\tpsk="{password}"\n')
        f.write("}\n")

# Main function to prompt user for Wi-Fi credentials and update configuration
def main():
    print("Please enter your Wi-Fi credentials below:")
    ssid, password = get_wifi_credentials()
    update_wifi_configuration(ssid, password)
    print("Wi-Fi configuration updated successfully.")

if __name__ == "__main__":
    main()
