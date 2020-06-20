from .instance.config import *
import requests
import json
import time
import redis


def get_whats_new(country):

    if country in supported_countries:
        url = netflix_url
        querystring = {"q": "get:new7:{}".format(
            country), "p": "1", "t": "ns", "st": "adv"}
        headers = netflix_headers
        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)['ITEMS']
        except:
            return False

        final_result = []

        for item in data:
            synopsis = item['synopsis'].split("<br>")

            result = {
                "netflixid": item['netflixid'],
                "title": item['title'],
                "image": item['image'],
                "synopsis": synopsis[0],
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
    else:
        # Recursively sending the default value
        return get_whats_new('uk')


def redis_content(country):
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y", named_tuple)
    time_string += country

    try:
        r = redis.from_url(redis_url)
        if r.exists(time_string):
            unpacked_json = json.loads(r.get(time_string))
            return unpacked_json
        else:
            final_result = get_whats_new(country)
            jsonify = json.dumps(final_result)
            r.set(time_string, jsonify)
            return final_result
    except:
        return get_whats_new(country)
