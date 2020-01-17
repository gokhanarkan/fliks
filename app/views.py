from __init__ import app
from flask import render_template, request
from functions import *


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        try:
            r = request.form['normal']  #  If it's a normal request, do the normal search
            result = request.form['flix']
            final_result = check_services(result)
            if final_result:
                return render_template('results.html', result=final_result, search=result)
            else:
                return render_template('notfound.html')
        except:
            r = request.form['netflix']
            result = request.form['flix']  # If it's a netflix request, do the netflix search
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
    final_result = redis_content()
    return render_template('whats_new.html', result=final_result)


@app.route('/flushcaches', methods=["GET"])
def clear_redis():
    if check_apikey(request.args):
        flush_redis()
        return "Cleared", 200
    else:
        return "Not Cleared", 400
