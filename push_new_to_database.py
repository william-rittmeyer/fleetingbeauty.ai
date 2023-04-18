import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'})

ref = db.reference('version_1/abstract')

new_data = {'painting_name': 'value1', 'url': 'value2'}
ref.update(new_data)

print('data has been added')
