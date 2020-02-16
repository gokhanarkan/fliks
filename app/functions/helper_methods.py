from .instance import *
import redis
import json
from ip2geotools.databases.noncommercial import DbIpCity


def create_html_result(json_file):

    html = '<ul>'
    for i in json_file['country_list']:
        html += '<li>' + i + '</li>'
    html += '</ul>'
    return html


def flush_redis():

    r1 = redis.from_url(heroku_redis)
    r1.flushall()
    r2 = redis.from_url(redis_to_go)
    r2.flushall()
    return True


def check_apikey(key):

    try:
        if key['apikey'] == apikey:
            return True
        else:
            return False
    except:
        return False


def cache_details(key, value):

    r = redis.from_url(redis_to_go)
    r.set(key, json.dumps(value))


# Scale this function for across services
def check_user_location(ip_address):

    r = redis.from_url(redis_to_go)
    user = r.get(ip_address)

    if user:

        unpacked_user = json.loads(user)
        return unpacked_user

    else:

        try:
            response = DbIpCity.get(ip_address, api_key='free')
            details = {
                "ip_address": response.ip_address,
                "city": response.city,
                "region": response.region,
                "country": response.country.lower(),
                "latitude": response.latitude,
                "longitude": response.longitude
            }
            cache_details(ip_address, details)
            return details
        except:
            # If something's wrong it returns False
            return False


def check_ip(ip):
    response = DbIpCity.get(ip, api_key='free')
    if response:
        country = response.country.lower()
        if country == 'gb':
            return 'uk'
        else:
            if country in ondemand_supported_countries:
                return country
            else:
                return False
    else:
        return False
