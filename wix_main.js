import {fetch} from 'wix-fetch';
import wixLocation from 'wix-location';

// Replace with your Firebase project's API key and database URL
const apiKey = 'APIKEY';
const databaseUrl = 
'https://fleeting-beauty-default-rtdb.firebaseio.com/';

// Replace with the path to the field you want to retrieve
const databasePath = '';

$w.onReady(function () {
  fetch(`${databaseUrl}${databasePath}.json?auth=${apiKey}`, {method: 
'get'})
    .then(response => response.json())
    .then(data => {
      $w('#html1').src = data['url'];

    })
    .catch(error => {
      console.error(error);
    });
});
