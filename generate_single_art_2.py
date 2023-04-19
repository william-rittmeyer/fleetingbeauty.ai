import openai
import json
import random
import datetime
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/',
    'storageBucket': 'fleeting-beauty.appspot.com'
})

openai.api_key = "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"


def artwork_create(style, subject, colors, tone):

  output_titles = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content":
              'generate 9 titles of landscape painting ideas'
  }]
  )

  painting_titles =  output_titles['choices'][0]['message']['content']

  painting_titles = painting_titles.split('\n')
  
  num = random.randint(1, 8)
  
  title = painting_titles[num]
  title = title[3:]

  title = title.replace('"','')
  title = title.replace("'","'")

  print(title)

  output_description = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content":
              'generate a landscape painting idea from the following title, ' + title + '. Make the description 3 sentences long. Start the description with the words, A landscape painting'
  }]
  )

  painting_description =  output_description['choices'][0]['message']['content']
  
  print(painting_description)


  out = openai.Image.create(
    prompt= painting_description + " The painting must fill the whole screen",
    n=1,
    size="1024x1024"
  )

  output = json.dumps(out)
  json_data = json.loads(output)

  selected_image_urls = []

  for item in json_data['data']:

    selected_image_urls.append(item['url'])

  return [selected_image_urls[0], title]

while True:

  # get the current time
  now = datetime.datetime.now()

  # check if it's the top of the hour
  if now.second == 0:
  # run the function
    try:
      A = artwork_create('abstarct','galaxy', 'blue', 'chaotic')

      ref = db.reference('')
      ref2 = db.reference('version_1/landscape')
      ref.update({'url': A[0]})
      ref.update({'painting_name': A[1]})

      ref2.update({'url': A[0]})
      ref2.update({'painting_name': A[1]})

      # Define the URL of the image you want to download and upload

      image_url = A[0]


      current_datetime = datetime.datetime.now()
      datetime_string = current_datetime.strftime("%m_%d_%Y_%H:%M:%S")


      filename = datetime_string + A[1].lower().replace(" ","_")
      folder_path = "prototype/"

      # Download the image from the URL
      response = requests.get(image_url)
      if response.status_code == 200:
        # Upload the image to Firebase storage
        bucket = storage.bucket()
        blob = bucket.blob(folder_path + filename)
        blob.upload_from_string(response.content, content_type=response.headers.get("content-type"))

        # Print the URL of the uploaded image
        print(f"Uploaded {filename} to {blob.public_url}")
      else:
        print(f"Failed to download image from {image_url}")


      print('picture updated')
      break

    except ValueError:
      print("error, trying again")

