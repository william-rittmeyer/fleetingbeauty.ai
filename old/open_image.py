import urllib.request
import pygame
from io import BytesIO

# Define the URL of the image you want to download
url_name = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-WAeUl1zBjHST0i3HRAvcHsId/user-EQQItIiQIfXAECUABpDJS8Oy/img-esHq5t1Aroo8zodhlshkV3jr.png?st=2023-04-11T21%3A02%3A25Z&se=2023-04-11T23%3A02%3A25Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-04-11T17%3A09%3A48Z&ske=2023-04-12T17%3A09%3A48Z&sks=b&skv=2021-08-06&sig=kBDDCcyMWsqhzVOD8RnKcpkHSsmpSiwdUuaBqq8UQl0%3D"

import urllib.request
import pygame
from io import BytesIO

def display_image_from_url(url):
    # Download the image from the URL
    try:
        image_data = urllib.request.urlopen(url).read()
    except urllib.error.URLError as e:
        print(f"Error downloading image: {e}")
        return

    # Initialize Pygame
    pygame.init()
    pygame.mouse.set_visible(False)

    # Create a Pygame display surface with the same dimensions as the screen
    try:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    except pygame.error as e:
        print(f"Error initializing Pygame: {e}")
        return

    # Save the image data to a file in the current directory
    with open('image.png', 'wb') as f:
        f.write(image_data)

    # Load the image from the file
    try:
        image = pygame.image.load('image.png')
    except pygame.error as e:
        print(f"Error loading image: {e}")
        return

    # Scale the image to fit the screen while maintaining the aspect ratio
    screen_width, screen_height = screen.get_size()
    image_width, image_height = image.get_size()
    if screen_width / screen_height > image_width / image_height:
        image = pygame.transform.scale(image, (int(screen_height * image_width / image_height), screen_height))
    else:
        image = pygame.transform.scale(image, (screen_width, int(screen_width * image_height / image_width)))

    # Center the image on the screen
    x = (screen_width - image.get_width()) / 2
    y = (screen_height - image.get_height()) / 2

    # Blit the image to the screen
    screen.blit(image, (x, y))
    pygame.display.flip()

    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
display_image_from_url(url_name)
