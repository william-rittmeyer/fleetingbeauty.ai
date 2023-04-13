\import openai
import requests
import json
import random
import time
import datetime
import webbrowser
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'})

from requests.structures import CaseInsensitiveDict
openai.api_key = "APIKEY"


def artwork_create(style, subject, colors, tone):

  output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content":
              'generate 11 detailed, professional landscape painting ideas that are 3 sentences each, with a title for each idea. The title must be in quotation marks like this "painting idea". Do not add any text other than the title and description. Start each description with the words, A painting'

  }]
  )



  painting_ideas =  output['choices'][0]['message']['content']
  painting_idea_elements = painting_ideas.split('\n')

  #print(painting_idea_elements)

  number_1= len(painting_idea_elements)
  first_element = painting_idea_elements[0]
  second_element = painting_idea_elements[1]

  del painting_idea_elements[1::2]
  del painting_idea_elements[:1]
  #print('------------------------')

  #print(painting_idea_elements)




  print("-----------------------------------------------")
  print("elements to choose from:")
  print(len(painting_idea_elements))
  index = random.randint(0,4)

  out = openai.Image.create(
    prompt= painting_idea_elements[index] + "The painting must fill the whole screen",
    n=1,
    size="1024x1024"
  )

  output = json.dumps(out)
  json_data = json.loads(output)

  image_title = painting_idea_elements[index].split('"')[1]

  selected_image_urls = []

  for item in json_data['data']:

    selected_image_urls.append(item['url'])

#  print(image_title)
#  print(selected_image_urls[0])


  return [selected_image_urls[0], image_title, number_1, first_element, second_element ]

while True:

  # get the current time
  now = datetime.datetime.now()

  # check if it's the top of the hour
  if now.second == 0:
  # run the function
    try:
      A = artwork_create('abstarct','galaxy', 'blue', 'chaotic')
#      webbrowser.open(A[0], new=0)

      ref = db.reference('')
      ref.update({'url': A[0]})
      ref.update({'painting_name': A[1]})

      print('picture updated')
      print("elements to start:")
      print(A[2])
      print("first element:")
      print(A[3])
      print("second element:")
      print(A[4])
      print("-----------------------------------------------")
      break



    except ValueError:
      print("error, trying again")
