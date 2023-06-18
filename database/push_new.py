import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'})

ref = db.reference()

# Add the new Boolean 'test' element at the root level and set it to False
ref.update({
    'test': False
})
print('data has been added')
