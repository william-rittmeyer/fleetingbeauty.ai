import os

def forceFBI():
    os.system("sudo fbi -d /dev/fb0 -a -noverbose -T 1 /boot/splash.png")
#forceFBI()

import datetime
import time
import urllib3
import requests
from io import BytesIO
from threading import Thread
import http.client as httplib
import subprocess
import socket
import pygame


database_url = 'https://fleeting-beauty-default-rtdb.firebaseio.com/'
url_endpoint = database_url + 'url.json'
url_endpoint_premium = database_url + 'url2.json'
premium_boolean_endpoint = database_url + 'test.json'
MAX_TIME_WIFI = 10
previous_image = None
next_image = None
location = None

http = urllib3.PoolManager()
def isConnected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            #print('Clossing socket')
            sock.close
        return True
    except OSError:
        pass
    return False

def handle_change(url):
    global previous_image, next_image, location
    painting_name = http.request('GET', database_url + 'painting_name.json').data.decode('utf-8')
    location = url
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H:%M:%S")
    next_image = load_image_from_url(location, resolution)
    if next_image is not None:
         previous_image = pygame.display.get_surface().copy()
         display_image(next_image, resolution)

    #print('handle_change: next_image loaded from', location)

def display_image_from_url(location, resolution):
    global previous_image, next_image
    if location != location:
         handle_change(location)

    if next_image is None:
        next_image = load_image_from_url(location, resolution)
       # print('display_image_from_url: next_image loaded from', location)

    if next_image is not None:
        display_image(next_image, resolution)

    next_image = None

def load_image_from_url(location, resolution):
    try:
        response = http.request('GET', str(location))
        image_data = response.data
    except urllib3.exceptions.HTTPError as e:
        return None

    try:
        image_file = BytesIO(image_data)
        image = pygame.image.load(image_file)
        #print('load_image_from_url: image loaded from', location)
    except pygame.error as e:
        return None

    # Load a higher resolution image
    if resolution == (1280, 720):
        image = pygame.transform.scale(image, (2048, 2048))
    else:
        image = pygame.transform.scale(image, (4096, 4096))

    # Scale the image down to fit the screen size with anti-aliasing
    screen_width, screen_height = pygame.display.get_surface().get_size()

    image = pygame.transform.smoothscale(image, (screen_width, screen_height))

    return image.convert()


def display_image(image, resolution):
    global previous_image
    screen_width, screen_height = pygame.display.get_surface().get_size()
    image = pygame.transform.scale(image, (screen_width, screen_height)) # resize the image to the screen size

    alpha = 0
    max_alpha = 255
    fade_speed = 10

    while alpha < max_alpha:
        alpha += fade_speed
        if alpha > max_alpha:
            alpha = max_alpha

        if previous_image is not None:
            pygame.display.get_surface().blit(previous_image, (0, 0))  # Blit the previous image
        image.set_alpha(alpha)
        pygame.display.get_surface().blit(image, (0, 0))
        pygame.display.flip()

    previous_image = image.copy()

def display_error(isWifiWait = False):
    global previous_image, next_image
    screen_width, screen_height = pygame.display.get_surface().get_size()

    try:
        if isWifiWait:
            image = pygame.image.load("/boot/splash.png")
        else:
            image = pygame.image.load("/boot/python/error.png")
    except:
        # If the error image fails to load, display a solid red screen
        image = pygame.Surface((screen_width, screen_height))
        image.fill((255, 0, 0))
    image = pygame.transform.scale(image, (screen_width, screen_height))
    pygame.display.get_surface().blit(image, (0, 0))
    pygame.display.flip() 

lastTime = time.time()

while not isConnected():
    #time.sleep(0.1)
    if time.time() - lastTime >= MAX_TIME_WIFI:
        break   
# Set the possible display resolutions in a dictionary
forceFBI()
resolutions = {
    '8K': (100, 100),
    '4K': (3840, 2160),
    '1440p': (2560, 1440),
    '1080p': (1920, 1080),
    '720p': (1280, 720)
}
# Try setting the display to the highest available resolution first
for res in sorted(resolutions.values(), reverse=True):
    try:
        screen = pygame.display.set_mode((0,0)) #res)
        #print(f"Display resolution set to {res[0]}x{res[1]}")
        resolution = res
        break
    except pygame.error:
        continue

# If none of the available resolutions work, set the resolution to (100, 100)
    else:
        screen = pygame.display.set_mode((0,0))
        #print("Display resolution set to 100x100")
        resolution = (100, 100)

pygame.init()
pygame.mouse.set_visible(False)
location = None
display_error(True)
lastTime = time.time()

try:
    premium_boolean = requests.get(premium_boolean_endpoint).json()
    if (premium_boolean):
        location = requests.get(url_endpoint_premium).json()
    else:
        location = requests.get(url_endpoint).json()

    display_image_from_url(location, resolution)
except requests.exceptions.ConnectionError:
    display_error()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                display_error()

    success = False

    for _ in range(2):  # try to get new location twice
        try:
            premium_boolean = requests.get(premium_boolean_endpoint).json()
            if (premium_boolean):
                new_location = requests.get(url_endpoint_premium).json()
            else:
                new_location = requests.get(url_endpoint).json()
            success = True
            break
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            continue

    if not success:  # if failed to get new location, try to reestablish connection
        try:
            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])
            time.sleep(5)
            premium_boolean = requests.get(premium_boolean_endpoint).json()
            if (premium_boolean):
                new_location = requests.get(url_endpoint_premium).json()
            else:
                new_location = requests.get(url_endpoint).json()
        except requests.exceptions.ConnectionError:
            display_error()
            continue

    if new_location != location:
        handle_change(new_location)
        display_image_from_url(new_location, resolution)

    time.sleep(5)
