import zmq
import requests

base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
api_key = 'AIzaSyDPHngadFjKeSDzYoIV2Y8ToXSWhx6ISmE'

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8080")


def make_url(a_message):
    """
    Parameter: string received through a socket
    String is formatted, replacing spaces with '+'s, and URL is built with it for API call
    Returns: URL for Google Geocoding API call
    """
    prepped_address = '+'.join(message.split())
    url = f"{base_url}{prepped_address}&key={api_key}"
    return url


def send_API_response(api_json):
    """
    Parameter: JSON file sent from API
    Sends a string with coordinates or error response to app.py
    """
    if api_json['status'] == 'OK':
        location = api_json['results'][0]['geometry']['location']
        coordinates = f"Latitude: {location['lat']}, Longitude: {location['lng']}"
        socket.send_string(coordinates)
    else:
        socket.send_string("This address is incomplete. Please re-enter the address. "
                           "Acceptable entries include just the zip code, a city and state, or a complete address.")


while True:
    # assigns string received from app.py file to message variable
    message = socket.recv_string()
    # format a URL for the API call
    url = make_url(message)
    # sends request, captures JSON response from Geocoding API, uses JSON to create response and sends to app.py
    response = requests.get(url)
    data = response.json()
    send_API_response(data)
