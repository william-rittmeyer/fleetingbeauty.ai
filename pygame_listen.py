import datetime
import time
import urllib3
import pygame
import requests
from io import BytesIO
from threading import Thread

database_url = 'https://fleeting-beauty-default-rtdb.firebaseio.com/'
url_endpoint = database_url + 'url.json'

previous_image = None
next_image = None

http = urllib3.PoolManager()

def handle_change(url):
    global previous_image, next_image
    painting_name = http.request('GET', database_url + 'painting_name.json').data.decode('utf-8')
    location = url
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H:%M:%S")
    next_image = load_image_from_url(location)
    print('handle_change: next_image loaded from', location)

def load_image_from_url(location):
    try:
        response = http.request('GET', str(location))
        image_data = response.data
    except urllib3.exceptions.HTTPError as e:
        return None

    try:
        image_file = BytesIO(image_data)
        image = pygame.image.load(image_file)
        print('load_image_from_url: image loaded from', location)
    except pygame.error as e:
        return None
    return image.convert()  # Convert the image to a Surface for hardware acceleration

def display_image(image):
    global previous_image
    screen_width, screen_height = pygame.display.get_surface().get_size()
    image = pygame.transform.scale(image, (screen_width, screen_height)) # resize the image to the screen size

    alpha = 0
    max_alpha = 255
    fade_speed = 5

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


def display_image_from_url(location):
    global previous_image, next_image

    if next_image is None:
        next_image = load_image_from_url(location)
        print('display_image_from_url: next_image loaded from', location)

    if next_image is not None:
        display_image(next_image)

    next_image = None

def display_error():
    print('error')


pygame.init()
screen = pygame.display.set_mode((1280, 720))  # Initialize a display surface
pygame.display.set_caption("Hello World")  # Optional caption for the window
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h)) # Set the display mode to match the screen resolution
print("Display resolution is:", info.current_w, "x", info.current_h)
pygame.mouse.set_visible(False)

location = requests.get(url_endpoint).json()
display_image_from_url(location)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                display_error()

    new_location = requests.get(url_endpoint).json()
    if new_location != location:
        handle_change(new_location)
        display_image_from_url(new_location)

    time.sleep(0.1)