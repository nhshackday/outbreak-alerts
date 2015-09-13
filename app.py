# Smart Arse  Accurate Reporting Statistics of Epidemiology
import collections
import functools
import json
import os

from flask import Flask, abort, request, redirect, Response, make_response


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper



app = Flask(__name__)
app.debug = True

data = json.loads(open('alerts.json').read())
by_place = collections.defaultdict(list)
for alert in data: 
    by_place[alert['country'].lower().split(',')[-1].strip()].append(alert)



def jsonp(fn):
    @functools.wraps(fn)
    def with_callback_maybe(*args,**kwargs):
        results = fn(*args,**kwargs)
        results = json.dumps(results)
        if  request.args.get('callback', None):
            return '{0}({1})'.format(request.args.get('callback'), results)
        else:
            resp = Response(results, mimetype='application/json')
            h = resp.headers

            h['Access-Control-Allow-Origin'] = '*'
            return resp


    return with_callback_maybe


@app.route('/api/<place>')
@jsonp
def place(place):
    return by_place[place.lower()]

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
