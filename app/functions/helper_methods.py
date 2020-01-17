from .instance.config import *
import redis


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
