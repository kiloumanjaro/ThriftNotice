import requests
import os
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def get_geocode(address):
    """Converts an address into latitude and longitude using Google Maps API."""
    if not API_KEY:
        return {"error": "API key is missing"}

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'key': API_KEY,
        'address': address
    }

    try:
        response = requests.get(base_url, params=params).json()

        if response['status'] == 'OK':
            geometry = response['results'][0]['geometry']
            return {
                "latitude": geometry['location']['lat'],
                "longitude": geometry['location']['lng'],
                "formatted_address": response['results'][0]['formatted_address']
            }
        else:
            return {"error": response['status']}
    except Exception as e:
        return {"error": f"Geocoding failed: {str(e)}"}
