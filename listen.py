import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import time
import urllib.request
import pygame
from io import BytesIO

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'
})
ref = db.reference('')
ref_url = db.reference('url')

print('------------------------------------------------------------------------')
def handle_change(event):
    painting_name = ref.child('painting_name').get()
    location = ref.child('url').get()
    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H:%M:%S")
    print('Updated at: ' + time_str)
    print('Painting Name: ' + painting_name)
    print('Picture located at: ' + location)
    print('------------------------------------------------------------------------')


def display_image_from_url(location):
    try:
        image_data = urllib.request.urlopen(location).read()
    except urllib.error.URLError as e:
        return
    try:
        pygame.init()
        pygame.mouse.set_visible(False)
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill((0, 0, 0))  # Fill the screen with black
    except pygame.error as e:
        return
    image_file = BytesIO(image_data)

    try:
        image = pygame.image.load(image_file)
    except pygame.error as e:
        return

    time.sleep(1)
    screen_width, screen_height = screen.get_size()
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
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
        pygame.display.flip()
        pygame.time.delay(50)

    while pygame.event.peek(pygame.USEREVENT) == []:
        time.sleep(0.1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        new_location = ref_url.get()
        if new_location != location:
            display_image_from_url(new_location)
            return

location = ref_url.get()
display_image_from_url(location)
ref_url.listen(handle_change)
location = ref.child('url').get()
display_image_from_url(location)
while True:
    pass
