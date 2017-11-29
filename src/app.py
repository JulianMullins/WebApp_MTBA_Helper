"""
A Web App for locating the nearest MBTA station to a given location
"""

from flask import Flask, render_template, request, redirect, url_for
from mbta_helper import get_lat_long, get_address, find_stop_near

app = Flask(__name__)

app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        address = request.form['address']

        nearest_stop = find_stop_near(address)

        if nearest_stop == "No stops nearby":
            return render_template('results.html')
        else:
            return render_template('results.html', start=address, stop_name=nearest_stop[0], stop_address=nearest_stop[1], dist=round(nearest_stop[2], 2))
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run()
