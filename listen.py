import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import time
import urllib.request
import pygame
from io import BytesIO
from threading import Thread

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'
})
ref = db.reference('')
ref_url = db.reference('url')

previous_image = None
next_image = None

def handle_change(event):
    global previous_image, next_image
    painting_name = ref.child('painting_name').get()
    location = ref.child('url').get()
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H:%M:%S")
    next_image = load_image_from_url(location)

def load_image_from_url(location):
    try:
        image_data = urllib.request.urlopen(location).read()
    except urllib.error.URLError as e:
        return None

    try:
        image_file = BytesIO(image_data)
        image = pygame.image.load(image_file)
    except pygame.error as e:
        return None
    return image

def display_image(image):
    global previous_image
    screen_width, screen_height = pygame.display.get_surface().get_size()
    image = pygame.transform.scale(image, (screen_width, screen_height))

    x = 0
    y = 0
    alpha = 0
    max_alpha = 255
    fade_speed = 5

    while alpha < max_alpha:
        alpha += fade_speed
        if alpha > max_alpha:
            alpha = max_alpha

        if previous_image is not None:
            pygame.display.get_surface().blit(previous_image, (x, y))  # Blit the previous image
        image.set_alpha(alpha)
        pygame.display.get_surface().blit(image, (x, y))
        pygame.display.flip()
        pygame.time.delay(50)

    previous_image = image.copy()

def display_image_from_url(location):
    global previous_image, next_image

    if next_image is None:
        next_image = load_image_from_url(location)

    if next_image is not None:
        display_image(next_image)

    next_image = None

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


while True:
    try:
        pygame.init()
        pygame.mouse.set_visible(False)
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        break
    except pygame.error as e:
        pass

location = ref_url.get()
display_image_from_url(location)

ref_url.listen(handle_change)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                display_error()

    new_location = ref_url.get()
    if new_location != location:
        handle_change(None)
        display_image_from_url(new_location)

    time.sleep(0.1)

