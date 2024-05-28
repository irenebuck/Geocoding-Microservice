import zmq
import requests

base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
api_key = 'AIzaSyDPHngadFjKeSDzYoIV2Y8ToXSWhx6ISmE'

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8080")

while True:
    # assigns string received from app.py file to message variable
    message = socket.recv_string()

    # replaces spaces with '+'s so we can build a properly formatted url
    prepped_address = '+'.join(message.split())

    # creates url for the API to read
    url = f"{base_url}{prepped_address}&key={api_key}"

    # sends request, captures JSON response from Geocoding API
    response = requests.get(url)
    data = response.json()

    # Reads the JSON response and sends string response to app.py
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        coordinates = f"Latitude: {location['lat']}, Longitude: {location['lng']}"
        socket.send_string(coordinates)
    else:
        socket.send_string("This address is incomplete. Please re-enter the address. "
                           "Acceptable entries include just the zip code, a city and state, or a complete address.")