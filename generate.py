import openai
import requests
import json

from requests.structures import CaseInsensitiveDict
openai.api_key = "USER_KEY"

def artwork_create(style, subject):

  output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": 
              "generate 10 extremely detailed ideas of" + style + "paintings involving" + subject

  }]
  )


  painting_ideas =  output['choices'][0]['message']['content']
  painting_idea_elements = painting_ideas.split('\n')

  del painting_idea_elements[1::2]
  #print(painting_elements_unsorted)

  out = openai.Image.create(
    prompt= painting_idea_elements[4],
    n=2,
    size="1024x1024"
  )

  output = json.dumps(out)
  json_data = json.loads(output)

  image_url = []

  for item in json_data['data']:

      image_url.append(item['url'])

  return image_url
  #    print(item['url'])

  #image_url has the links to images generated (only 2)

  #need to have user input and user output
