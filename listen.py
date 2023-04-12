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

    new_location = ref_url.get()
    if new_location != location:
        handle_change(None)
        display_image_from_url(new_location)

    time.sleep(0.1)
