import openai
import json
import random
import datetime
import requests
import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/',
    'storageBucket': 'fleeting-beauty.appspot.com'
})

openai.api_key = "APIKEY"


def artwork_create():

  output_titles = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content":
              'generate 9 titles of cubism painting ideas'
  }]
  )

  painting_titles =  output_titles['choices'][0]['message']['content']
  print(painting_titles)
  print("************************************************************************************************************************************************************")
  painting_titles = painting_titles.split('\n')
  print(painting_titles)
  print("************************************************************************************************************************************************************")
  num = random.randint(1, 8)

  title = painting_titles[num]
  title = title[3:]

  title = title.replace('"','')
  title = title.replace("'","'")

  print(title)

  output_description = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content":
              'generate a cubism painting' + title + '. Make the description 4 sentences long. Start the description with the words, A cubism painting'
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

      A = artwork_create()

      # Define the URL of the image you want to download and upload

      image_url = A[0]


      current_datetime = datetime.datetime.now()
      datetime_string = current_datetime.strftime("%m_%d_%Y_%H:%M:%S")


      filename = datetime_string + A[1].lower().replace(" ","_")
      folder_path = "cubism/"

      # Download the image from the URL
      response = requests.get(image_url, timeout=600)
      if response.status_code == 200:
        # Upload the image to Firebase storage
        bucket = storage.bucket()
        blob = bucket.blob(folder_path + filename)
        blob.upload_from_string(response.content, content_type=response.headers.get("content-type"))


        print("************************************************************************************************************************************************************")

        # Print the URL of the uploaded image
        print(f"Uploaded {filename} to {blob.public_url}")
      else:
        print(f"Failed to download image from {image_url}")


      # Create a signed URL for the blob that lasts for 1 hour
      url_google = blob.generate_signed_url(datetime.timedelta(hours=1), method='GET')

      ref = db.reference('')
      ref.update({'url_cubism': url_google})
      ref.update({'painting_name_cubism': A[1]})


      print("************************************************************************************************************************************************************")





      print('picture updated')
      print("##############################################################################################################################################")
      print("##############################################################################################################################################")
      print("##############################################################################################################################################")
      break

    except openai.error.InvalidRequestError:
      print("Request rejected by OpenAI safety system. Retrying...")
      continue

    except openai.error.RateLimitError:
      print("Rate limit exceeded. Waiting and retrying...")
      time.sleep(60)  # Wait for 60 seconds before retrying
      continue

    except openai.error.APIError:
      print("A network issue has occurred. Retrying...")
      time.sleep(60)  # Wait for 60 seconds before retrying
      continue

    except requests.exceptions.RequestException:
      print("HTTP request to download image failed. Retrying...")
      continue

    except openai.error.Timeout:
      print("OpenAI API request timed out. Waiting and retrying...")
      time.sleep(60)  # Wait for 60 seconds before retrying
      continue

    except ValueError:
      print("error, trying again")
      continue
