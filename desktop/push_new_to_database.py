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
        new_elem = "version_1/model_number/" + str(elem)
        new_lst.append(new_elem)
    return new_lst


directories = [#list of model Numbers goes here]

paths = add_to_list_elements(directories)

# Loop through the list and update each directory with new data
for x in paths:
    ref.child(x).update({'painting_name': 'value1', 'url': 'value2'})

print('data has been added')
