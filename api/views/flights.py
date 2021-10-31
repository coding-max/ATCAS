#!/usr/bin/python3
"""
This module contains all the endpoints of the RESTFUL API V1 of ATCAS web application,
which the web app frontend uses to load the processed data in backend
"""

from flask import jsonify, abort, request, make_response
from api.views import app_views
from models import storage
from models.airport import Airport
from models.aircraft import Aircraft
import json


@app_views.route('/airport', methods=['GET'], strict_slashes=False)
def create_airport():
    """returns information about the current working airport"""
    airport = Airport("MVD").to_dict()
    #airport = Aircraft.plane_list
    return jsonify(airport)


@app_views.route('/flights', methods=['GET'], strict_slashes=False)
def flights():
    """returns a json with information about all flights in the airspace"""
    with open("./api/views/output.json", 'r') as f:
        stat = json.load(f)
    return jsonify(stat)


