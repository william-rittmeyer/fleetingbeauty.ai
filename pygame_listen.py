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
    next_image = load_image_from_url(location, resolution)
    print('handle_change: next_image loaded from', location)

def display_image_from_url(location, resolution):
    global previous_image, next_image

    if next_image is None:
        next_image = load_image_from_url(location, resolution)
        print('display_image_from_url: next_image loaded from', location)

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
        print('load_image_from_url: image loaded from', location)
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


def display_error():
    global previous_image, next_image
    
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    font = pygame.font.SysFont(None, 50)
    line1 = font.render("Fleeting Beauty was disconnected from wifi! ", True, (255, 0, 0))
    line2 = font.render("Please troubleshoot with one of the few:", True, (0, 0, 0))
    line3 = font.render("    1. Unplug and plug device back in display. ", True, (0, 0, 0))
    line4 = font.render("    2. Check that your router is connected to the internet.", True, (0, 0, 0))
    line5 = font.render("    3. Plug in device to computer and re-type in password.", True, (0, 0, 0))

    # Calculate total height of text box
    total_height = line1.get_height() + line2.get_height() + line3.get_height() + line4.get_height() + line5.get_height()
    total_height += 60 # Add some padding

    box_width = screen_width // 2
    box_height = total_height // 5
    margin_left = (screen_width - box_width) // 2
    margin_top = (screen_height - total_height) // 2

    screen = pygame.display.get_surface()
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (255, 255, 255), (margin_left, margin_top, box_width, total_height))

    # Calculate y-coordinate of each line
    line1_y = margin_top + 20
    line2_y = line1_y + line1.get_height() + 10
    line3_y = line2_y + line2.get_height() + 10
    line4_y = line3_y + line3.get_height() + 10
    line5_y = line4_y + line4.get_height() + 10

    text_rect = line1.get_rect(topleft=(margin_left + 10, line1_y))
    screen.blit(line1, text_rect)

    text_rect = line2.get_rect(topleft=(margin_left + 10, line2_y))
    screen.blit(line2, text_rect)

    text_rect = line3.get_rect(topleft=(margin_left + 10, line3_y))
    screen.blit(line3, text_rect)

    text_rect = line4.get_rect(topleft=(margin_left + 10, line4_y))
    screen.blit(line4, text_rect)

    text_rect = line5.get_rect(topleft=(margin_left + 10, line5_y))
    screen.blit(line5, text_rect)

    pygame.display.flip()


pygame.init()

# Set the possible display resolutions in a dictionary
resolutions = {
    '8K': (7680, 4320),
    '4K': (3840, 2160),
    '1440p': (2560, 1440),
    '1080p': (1920, 1080),
    '720p': (1280, 720)
}

# Try setting the display to the highest available resolution first
for res in sorted(resolutions.values(), reverse=True):
    try:
        screen = pygame.display.set_mode(res)
        print(f"Display resolution set to {res[0]}x{res[1]}")
        resolution = res
        break
    except pygame.error:
        continue

# If none of the available resolutions work, set the resolution to (100, 100)
    else:
        screen = pygame.display.set_mode((100, 100))
        print("Display resolution set to 100x100")
        resolution = (100, 100)

pygame.display.set_caption("Hello World")  # Optional caption for the window
info = pygame.display.Info()
pygame.mouse.set_visible(False)

location = requests.get(url_endpoint).json()
display_image_from_url(location, resolution)

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
        display_image_from_url(new_location, resolution)

    time.sleep(0.1)

