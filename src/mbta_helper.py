import urllib.request   # urlencode function
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"
GMAPS_API_KEY = "AIzaSyBTI7VclW4BKfBrq9xyQIichYqFh5UWtis"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    
    #create url
    place_arr = place_name.split()
    place_string = "+".join(place_arr)
    params = "?address="+place_string+"&key="+GMAPS_API_KEY
    url = GMAPS_BASE_URL + params

    json_res = get_json(url)
    
    location = json_res['results'][0]['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']

    return (latitude, longitude)

# print(get_lat_long("Babson Park, Wellesley"))