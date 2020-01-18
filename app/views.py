from __init__ import app
from flask import render_template, request
from functions import *


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        try:
            #  If it's a normal request, do the normal search
            r = request.form['normal']
            result = request.form['flix']
            final_result = check_services(result)
            if final_result:
                return render_template('results.html', result=final_result, search=result)
            else:
                return render_template('notfound.html')
        except:
            r = request.form['netflix']
            # If it's a netflix request, do the netflix search
            result = request.form['flix']
            final_result = redis_netflix_search(result)
            if final_result:
                return render_template('netflix-results.html', result=final_result, search=result)
            else:
                return render_template('notfound.html')
    else:
        return render_template('layout.html')


@app.route('/get_country_list', methods=["POST"])
def get_country_list():
    if request.method == 'POST':
        result = request.form['netflixid']
        final_result = create_html_result(redis_entry(result))
        if final_result:
            return final_result
        else:
            result = create_html_result({'country_list': ['Not Found']})
            return result


@app.route('/whats_new', methods=["GET"])
def whats_new():
    try:
        user_location = check_user_location(
            request.headers['X-Forwarded-For'])['country']
        if user_location:
            final_result = redis_content(user_location)
            country = supported_countries[user_location]
            return render_template('whats_new.html', result=final_result, country=country, supported_countries=supported_countries)
        else:
            final_result = redis_content('us')
            return render_template('whats_new.html', result=final_result, country=False, supported_countries=supported_countries)
    except:
        # Couldn't detect the country
        final_result = redis_content('us')
        return render_template('whats_new.html', result=final_result, country=False, supported_countries=supported_countries)


@app.route('/change_country', methods=["POST"])
def change_country():
    if request.method == 'POST':
        country = request.form['country']
        what_new_data = redis_content(country)
        return json.dumps(what_new_data)


@app.route('/flushcaches', methods=["GET"])
def clear_redis():
    if check_apikey(request.args):
        flush_redis()
        return "Cleared", 200
    else:
        return "Not Cleared", 400
