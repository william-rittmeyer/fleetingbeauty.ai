import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'})



ref = db.reference('')

field_ref = ref.child('url')
field_value = field_ref.get()


print(field_value)
