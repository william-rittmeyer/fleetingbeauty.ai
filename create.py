import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'})

ref = db.reference('')


ref.set({'url': 'value1', 'time': 'value2'})


print('data has been added')




