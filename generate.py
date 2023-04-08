import openai
import requests
import json
import random

from requests.structures import CaseInsensitiveDict
openai.api_key = "USER-KEY"

def artwork_create(style, subject, colors, tone):

  output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": 
              "generate 8 extremely detailed ideas (with a title) of" + style + 
               "paintings involving" + subject + "with a color scheme of" + 
               colors + " and tone of" + tone

  }]
  )


  painting_ideas =  output['choices'][0]['message']['content']
  painting_idea_elements = painting_ideas.split('\n')

  del painting_idea_elements[1::2]
  #print(painting_elements_unsorted)

  index = random.randint(0,6)

  out = openai.Image.create(
    prompt= painting_idea_elements[index],
    n=1,
    size="1024x1024"
  )

  output = json.dumps(out)
  json_data = json.loads(output)

  image_title = painting_idea_elements[index].split('"')[1]

  selected_image_urls = []

  for item in json_data['data']:

      selected_image_urls.append(item['url'])

  return [selected_image_urls[0], image_title]

  #    print(item['url'])

  #image_url has the links to images generated (only 2)

  #need to have user input and user output
