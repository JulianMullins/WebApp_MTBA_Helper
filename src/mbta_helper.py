import urllib.request   # urlencode function
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_API_KEY = "VRDnOahZm0eZUIltYACIGQ"
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

    if place_name == "":
        return "No Address Given"
    
    #create url
    place_arr = place_name.split()
    place_string = "+".join(place_arr)
    params = "?address="+place_string+"&key="+GMAPS_API_KEY
    url = GMAPS_BASE_URL + params

    json_res = get_json(url)
    
    if len(json_res['results']) == 0:
        return "No Results"
    
    location = json_res['results'][0]['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']

    return (latitude, longitude)

def get_address(lat, lng):
    """
    Given a latitude and longitude, return a human readable address.
    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """

    #create url
    params = "?latlng=" + str(lat) + "," + str(lng) + "&key="+GMAPS_API_KEY
    url = GMAPS_BASE_URL + params

    json_res = get_json(url)

    address = json_res['results'][0]['formatted_address']

    return address


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, address, distance)
    tuple for the nearest MBTA station to the given coordinates.
    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API in 'MBTA-realtime API v2 Documentation'.
    """

    #create url
    params = "?api_key="+MBTA_API_KEY+"&format=json&lat=" + str(latitude) + "&lon=" + str(longitude)
    url = MBTA_BASE_URL + params

    json_res = get_json(url)
    print(json_res)

    if len(json_res['stop']) == 0:
        return "No stops nearby"

    station_name = json_res['stop'][0]['stop_name']
    station_lat_lon = (json_res['stop'][0]['stop_lat'], json_res['stop'][0]['stop_lon'])
    station_address = get_address(station_lat_lon[0], station_lat_lon[1])
    distance = json_res['stop'][0]['distance']

    return (station_name, station_address, float(distance))


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop name, the stop address and the 
    distance from the given place to that stop.
    """
    lat_lon = get_lat_long(place_name)

    if lat_lon == "No Address Given":
        return "No stops nearby"

    nearest_stop = get_nearest_station(lat_lon[0], lat_lon[1])
    return nearest_stop


# print(find_stop_near("677 Centre Street, Jamaica Plain, MA 02130"))

# print(find_stop_near("231 Forest St."))

print(find_stop_near(""))