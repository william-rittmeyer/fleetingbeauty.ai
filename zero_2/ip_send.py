import requests

database_url = 'https://fleeting-beauty-default-rtdb.firebaseio.com/'
url_endpoint = database_url + 'url.json'

def write_to_test_url_directory(data):
    """
    Writes the provided data to the `/test/url` directory using the URL endpoint.
    
    Parameters:
    data (str): The data to be written to the directory.
    """
    try:
        # Send the request to the URL endpoint with the data and directory path
        response = requests.patch(url_endpoint, json={ "test": { "url": data } })

        # Check the response status code for success
        if response.status_code == requests.codes.ok:
            print("Successfully wrote data to /test/url directory.")
        else:
            print("Failed to write data to /test/url directory. Response code:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print("Error writing data to /test/url directory:", e)

write_to_test_url_directory("Hello, world!")


