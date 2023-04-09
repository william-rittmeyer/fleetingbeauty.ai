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
              "generate 10 extremely detailed ideas of 3 sentences each (with a title for each idea in quotation marks) of" + style + 
               "paintings involving" + subject + "with a color scheme of" + 
               colors + " and tone of" + tone + ". Do not add any text other than the title and description."

  }]
  )


  painting_ideas =  output['choices'][0]['message']['content']
  painting_idea_elements = painting_ideas.split('\n')

  del painting_idea_elements[1::2]

  print(painting_idea_elements)

  index = random.randint(0,4)

  out = openai.Image.create(
    prompt= painting_idea_elements[index] + "make sure the painting covers the whole image (this is necessary)",
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
