from __init__ import app
from flask import render_template, request
from functions import *

# Main page
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        try:
            #  If it's a normal request, do the normal search
            r = request.form['normal']
            result = request.form['flix']
            try:
                ip = request.headers['X-Forwarded-For']
                country = check_ip(ip)
                if not country:
                    country = "uk"
            except:
                country = "uk"
            # This function will be improved with ip address
            final_result = check_services(result, country)
            return render_template('results.html', result=final_result, search=result, existing_search=result, country=country.upper(), supported_countries=ondemand_supported_countries)
        except:
            r = request.form['netflix']
            # If it's a netflix request, do the netflix search
            result = request.form['flix']
            final_result = redis_netflix_search(result)
            if final_result:
                return render_template('netflix-results.html', result=final_result, search=result, existing_search=result)
            else:
                return render_template('notfound.html', existing_search=result)
    else:
        return render_template('layout.html')

# Ajax query for getting country information
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

# What's New on Netflix
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

# Changing country in What's New
@app.route('/change_country', methods=["POST"])
def change_country():
    if request.method == 'POST':
        country = request.form['country']
        what_new_data = redis_content(country)
        return json.dumps(what_new_data)

# Changing country in Across Services
@app.route('/ondemand_change_country', methods=["POST"])
def ondemand_change_country():
    if request.method == 'POST':
        term = request.form['search']
        country = request.form['country']
        service_data = check_services(term, country)
        return json.dumps(service_data)

# Flushing caches
@app.route('/flushcaches', methods=["GET"])
def clear_redis():
    if check_apikey(request.args):
        flush_redis()
        return "Cleared", 200
    else:
        return "Not Cleared", 400

# Service worker file for PWA settings
@app.route('/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')
