#!/usr/bin/python3
"""
This module contains all the endpoints of the RESTFUL API V1 of ATCAS web application,
which the web app frontend uses to load the processed data in backend
"""

from flask import Flask, render_template, redirect, url_for, request, session
from flask import jsonify, abort, request, make_response, render_template
from api.views import app_views
from models import storage
from models.engine import db_queries
from models.airport import Airport
from models.aircraft import Aircraft


@app_views.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = db_queries.get_user(request.form['username'], request.form['password'])
        if user is not None:
            session['name'] = user[0] + ' ' + user[1]
            return redirect(url_for('app_views.index'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)