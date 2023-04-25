import requests


database_url = 'https://fleeting-beauty-default-rtdb.firebaseio.com/'

def check_custom_value():
    # Construct the full URL for the custom value
    url = f"{database_url}version_1/model_number/DuoZqxgk3hzcVOUU/custom.json"

    # Use requests library to get the value from the URL
    response = requests.get(url)

    # Check the value of the response
    if response.status_code == 200:
        custom_value = response.json()

    return custom_value


print(check_custom_value())