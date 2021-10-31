#!/usr/bin/python3
"""views module"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/')

from api.views.flights import *
from api.views.login import *
