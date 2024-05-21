
Geocode Microservice
*****
This project builds a basic GUI app using tkinter and is coded in Python.
The user enters an address and that address is communicated through a ZeroMQ REQ socket to a microservice.
The microservice listens for a message on port 8080. When one is received, it prepares a properly formatted url
to call the Google Geocoding API. The API converts the address to the location's latitude and longitude and sends
it back to the microservice in a JSON object. The microservice reads the JSON file and if the status code in it is 'OK',
sends the app.py the latitude and longitude coordinates in a string; if the status is not OK, a string with directions
to resubmit the location is sent in a string. The receiving app.py then shares the received string in the GUI.


Guides in the creation of this program:
*****
Google Geocoding API
Directions on using the Google Geocoding API are found at
https://developers.google.com/maps/documentation/geocoding/requests-geocoding
API Request format: https://maps.googleapis.com/maps/api/geocode/outputFormat?parameters
Example: https://maps.googleapis.com/maps/api/geocode/json?address=Mountain+View,+CA&amp;key=YOUR_API_KEY

ZeroMQ
Directions for using the REQ and REP sockets are found at https://zeromq.org/socket-api/

tkinter
Documentation for this Python package is found at https://docs.python.org/3/library/tkinter.html


How to use this program:
*****
- Run the microservice.py file
- Run the app.py simultaneously
- A small box will appear prompting the user to enter a location and click 'Submit Address' button.

    Example entry: 1600 Amphitheatre Parkway, Mountain View, CA 94043

- Once the button is clicked, the value that was in the box will be sent through a ZeroMQ REQ socket connected to
    a localhost:8080.
- In the microservice.py file, a REP ZeroMQ socket will be listening to the localhost:8080 socket.
    It will collect the location string that was sent by the app.py file, format a URL with the address,
    and send an API request to the Google Geocoding API.

    Example URL created and sent to API:
    https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&amp;key=YOUR_API_KEY

- The Google Geocoding API will receive the location, process it, and send back a JSON object.
    If the location was validated by the Geocoding API, the status in the JSON object will be 'OK'
    and the latitude and longitude coordinates will be in the JSON object.

    Example JSON response from the API:
    {
        "results": [
            {
                "address_components": [
                    {
                        "long_name": "1600",
                        "short_name": "1600",
                        "types": [
                            "street_number"
                        ]
                    },
                    {
                        "long_name": "Amphitheatre Parkway",
                        "short_name": "Amphitheatre Pkwy",
                        "types": [
                            "route"
                        ]
                    },
                    {
                        "long_name": "Mountain View",
                        "short_name": "Mountain View",
                        "types": [
                            "locality",
                            "political"
                        ]
                    },
                    {
                        "long_name": "Santa Clara County",
                        "short_name": "Santa Clara County",
                        "types": [
                            "administrative_area_level_2",
                            "political"
                        ]
                    },
                    {
                        "long_name": "California",
                        "short_name": "CA",
                        "types": [
                            "administrative_area_level_1",
                            "political"
                        ]
                    },
                    {
                        "long_name": "United States",
                        "short_name": "US",
                        "types": [
                            "country",
                            "political"
                        ]
                    },
                    {
                        "long_name": "94043",
                        "short_name": "94043",
                        "types": [
                            "postal_code"
                        ]
                    },
                    {
                        "long_name": "1351",
                        "short_name": "1351",
                        "types": [
                            "postal_code_suffix"
                        ]
                    }
                ],
                "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
                "geometry": {
                    "location": {
                        "lat": 37.4222804,
                        "lng": -122.0843428
                    },
                    "location_type": "ROOFTOP",
                    "viewport": {
                        "northeast": {
                            "lat": 37.4237349802915,
                            "lng": -122.083183169709
                        },
                        "southwest": {
                            "lat": 37.4210370197085,
                            "lng": -122.085881130292
                        }
                    }
                },
                "place_id": "ChIJRxcAvRO7j4AR6hm6tys8yA8",
                "plus_code": {
                    "compound_code": "CWC8+W7 Mountain View, CA",
                    "global_code": "849VCWC8+W7"
                },
                "types": [
                    "street_address"
                ]
            }
        ],
        "status": "OK"
    }

- The microservice will read the JSON file. If the status in it is 'OK', the microservice will send a string with
     the coordinates back through the ZeroMQ pipe/socket. If the status is other than 'OK', the microservice will
     send a string with directions to resubmit the request.

     Example response from microservice when status is 'OK':
     Latitude: 37.4222804, Longitude: -122.0843428

     Example response from microservice when status is other than 'OK':
     This address is incomplete. Please re-enter the address. Acceptable entries include just the zip code, a city and state, or a complete address.

- The app.py listening on the 8080 port will receive the response and display it for the user to read on their screen.


