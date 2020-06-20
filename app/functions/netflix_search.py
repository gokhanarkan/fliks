from .instance.config import *
import redis
import requests
import json


def get_netflix_details(name):
    url = netflix_url
    querystring = {"q": "{}-!1900,2020-!0,5-!0,10-!0-!Any-!Any-!Any-!gt100-!{}".format(name, '{downloadable}'),
                   "t": "ns", "cl": "all", "st": "adv", "ob": "Relevance", "p": "1", "sa": "or"}
    headers = netflix_headers
    try:
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)['ITEMS']
    except:
        return False

    if not data:
        return False

    final_result = []
    for item in data:
        result = {
            "netflixid": item['netflixid'],
            "title": item['title'],
            "image": item['image'],
            "synopsis": item['synopsis'],
            "rating": item['rating'],
            "type": item['type'],
            "release_date": item['released'],
            "time": item['runtime'],
            "download": item['download'],
            "large_image": item['largeimage'],
            "link": "https://www.netflix.com/title/" + item['netflixid']
        }

        final_result.append(result)

    return final_result


def redis_netflix_search(name):
    try:
        r = redis.from_url(redis_url)
        name = name.lower()
        if r.exists(name):
            unpacked_json = json.loads(r.get(name))
            return unpacked_json
        else:
            final_result = get_netflix_details(name)
            json_result = json.dumps(final_result)
            r.set(name, json_result)
            return final_result
    except:
        final_result = get_netflix_details(name)
        return final_result
