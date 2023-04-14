import { fetch } from 'wix-fetch';
import wixWindow from 'wix-window';

// Replace with your Firebase project's API key and database URL
const apiKey = 'APIKEY';
const databaseUrl = 'https://fleeting-beauty-default-rtdb.firebaseio.com/';

// Replace with the path to the field you want to retrieve
const databasePath = '';
setInterval(() => {
    $w.onReady(function () {
        fetch(`${databaseUrl}${databasePath}.json?auth=${apiKey}`, { method: 'get' })
            .then(response => response.json())
            .then(data => {

                $w('#image1').src = data['url'];
                console.log(data['painting_name'])
                $w('#text41').text = data['painting_name'];
                $w("#image1").show("fade", { duration: 2000, delay: 100 });
                //$w('#image1').show('fade');
                $w('#text41').show('fade', { duration: 2000, delay: 100 });

                $w('#button3').onClick(() => {
                    wixWindow.openLightbox('LargeImage', data['url']);
                });
            })

    });
}, 400);