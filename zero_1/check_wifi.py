import subprocess
import time

while True:
    try:
        output = subprocess.check_output(["iwgetid", "-r"])
        print("Connected to WiFi with SSID:", output.decode("utf-8").strip())
    except subprocess.CalledProcessError:
        print("Not connected to WiFi")
    time.sleep(10)
