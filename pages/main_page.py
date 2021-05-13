from tools.log import logged
from tools.log import logged
from db import creating_scratch
from flask import Blueprint
import json
from tools.log import logged, logger
from flask import Blueprint
from flask import request, make_response
import requests
import uuid
import json
import base64
import os
from werkzeug.utils import secure_filename
from flask import request, make_response, Response
import numba
import json
import time

from globals import get_model

main_page = Blueprint('main_page', __name__, template_folder='templates')



@main_page.route('/init', methods=['GET','OPTIONS'])
@logged
def init():
    get_model().init_db()
    return make_response("",200)

@main_page.route('/predict_prices', methods=['POST','OPTIONS'])
@logged
def predict():
    if request.method=="OPTIONS":
        return make_response("",200)

    start = time.time()

    print(request.data)
    data = json.loads(request.data)
    origin = data['origin']
    dest = data['destination']
    flight_date = data['flight_date']
    current_date = data['date']
    days, prices = get_model().predict(origin, dest, current_date, flight_date)
    x, real_prices = get_model().show_real_prices(origin, dest, current_date, flight_date)

    end = time.time()
    print('elapsed: ', end - start)
    return make_response(json.dumps({"days": days, "prices": prices, "real_prices": real_prices}), 200)
