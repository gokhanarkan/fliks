from .instance.config import *
import requests
import json


def check_services(name):
    url = service_check_url
    querystring = {"term": name}
    headers = service_check_headers
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)['results']
    except:
        return False

    if not data:
        return False

    final_result = []
    for item in data:
        result = {
            "name": item['name'],
            "picture": item['picture'],
        }
        location = []
        for l in item['locations']:
            location_model = [l['display_name'], l['url'], l['icon']]
            location.append(location_model)
        result['locations'] = location
        final_result.append(result)

    return final_result
