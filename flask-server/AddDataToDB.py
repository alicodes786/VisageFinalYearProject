import requests
import json

# Define the URL for the Firebase Realtime Database REST API endpoint
url = 'https://facialrecognitionapp-e148f-default-rtdb.firebaseio.com/Accounts.json'

# Prepare the data to send to the database
data = {
    "12345": {
        "name": "Mirza Raza",
        "bank": "Emirates NBD",
        "card_details": "5156829191234591",
        "cvv":"423",
        "expiry":"1223"
    },
    "85271": {
        "name": "Amitabh Bachhan",
        "bank": "Starling",
        "card_details": "5569213453456789",
        "cvv":"678",
        "expiry":"1223"
    },
    "91234": {
        "name": "Elon Musk",
        "bank": "Lloyds",
        "card_details": "5214567876678912",
        "cvv":"577",
        "expiry":"1223"
    },
    "98765": {
        "name": "Hrithik Roshan",
        "bank": "Natwest",
        "card_details": "5356999991234565",
        "cvv":"536",
        "expiry":"1223"
    },
    "989876": {
        "name": "Asgar Raza",
        "bank": "Mashreq",
        "card_details": "4356987877692562",
        "cvv":"426",
        "expiry":"1223"
    }
}

# Convert data to JSON format
json_data = json.dumps(data)

# Make a POST request to send the data to the database
response = requests.put(url, data=json_data)

# Handle the response
if response.ok:
    print('Data sent successfully')
else:
    print('Failed to send data:', response.text)
