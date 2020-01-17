from __init__ import *


def test_across_services(arr):
    for item in arr:
        json_value = check_services(item)
        if not json_value:
            return False


def test_netflix_search(arr):
    for item in arr:
        json_value = get_netflix_details(item)
        if not json_value:
            return False
        else:
            test_country_availability(json_value[0]['netflixid'])

def test_country_availability(netflixid):
    countries = get_country_availability(netflixid)
    if countries == ["Not Available"]:
        return False


def test_redis_connection():
    try:
        r1 = redis.from_url(heroku_redis)
        r2 = redis.from_url(redis_to_go)
    except:
        return False


def test_whats_new():
    json_value = get_whats_new()
    if not json_value:
        return False


movies = ['Inception', 'Planet Earth', 'Interstellar', 'Evil Dead', 'Departed']


if __name__ == "__main__":
    try:
        test_across_services(movies)
        test_netflix_search(movies)
        test_redis_connection()
        test_whats_new()
        print('All tests passed.')
    except Exception as e:
        print(e)
