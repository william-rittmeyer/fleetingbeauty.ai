import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://fleeting-beauty-default-rtdb.firebaseio.com/'})

ref = db.reference()

# Define the list of directories to update


def add_to_list_elements(lst):
    new_lst = []
    for elem in lst:
        new_elem = "version_2/model_number/" + str(elem)
        new_lst.append(new_elem)
    return new_lst


directories = [#MODEL NUMBERS]

paths = add_to_list_elements(directories)

# Loop through the list and update each directory with new data
for x in paths:
    ref.child(x).update({'painting_name': 'undefined', 'url': 'undefined', 'custom': False, 'color': 'undefined', 'subject': 'undefined', 'tone': 'undefined', 'style': 'undefined', 'ip_addr': 'undefined'})

print('data has been added')
