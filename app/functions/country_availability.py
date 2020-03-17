from .instance.config import *
import redis
import requests
import json


def get_country_availability(netflixid):
    url = country_url
    querystring = {"netflixid": netflixid}
    headers = country_headers
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)['results']
    except:
        return ["Not Available"]

    if not data:
        return ["Not Available"]

    country_list = []
    for item in data:
        country = item['country'].replace(' ', '')
        country_list.append(country)

    return country_list


def redis_entry(key):
    try:
        r = redis.from_url(redis_url)
        if r.exists(key):
            unpacked_json = json.loads(r.get(key))
            return unpacked_json
        else:
            final_result = sort_jsonify_list(key)
            json_country_list = json.dumps(final_result)
            r.set(key, json_country_list)
            return final_result
    except:
        final_result = sort_jsonify_list(key)
        return final_result


def sort_jsonify_list(key):
    country_list = get_country_availability(key)
    country_list.sort()
    final_result = {'country_list': country_list}

    return final_result
