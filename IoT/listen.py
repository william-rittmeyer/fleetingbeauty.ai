import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import time

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the Firebase app with the credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'
})

# Get a reference to the Firebase Realtime Database
ref = db.reference('')
ref_url = db.reference('url')

print('------------------------------------------------------------------------')

# Define a function to handle changes to the data
def handle_change(event):
    
    time.sleep(10)

    painting_name = ref.child('painting_name').get()
    location = ref.child('url').get()

    current_time = datetime.datetime.now()
    time_str = current_time.strftime("%H:%M:%S")
    
    print('Updated at: ' + time_str)
    print('Painting Name: ' + painting_name)
    print('Picture located at: ' + location)

    print('------------------------------------------------------------------------')


	

# Listen for changes to the data and call the handle_change function when it changes
ref_url.listen(handle_change)

# Keep the script running to continue listening for changes
while True:
    pass
