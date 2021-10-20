#!/usr/bin/python3
"""view for 'Flights'"""

import cmd
import json
import models
from models.aircraft import Aircraft
from models.airport import Airport
import math
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.aircraft import Aircraft
from models import storage


@app_views.route('/airport', methods=['GET'], strict_slashes=False)
def create_airport():
    """ #todo """
    airport = Airport("MVD").to_dict()
    return jsonify(airport)

@app_views.route('/flights', methods=['GET'], strict_slashes=False)
def flights():
    """ prints all flight information based on ID's given"""
    flights_list = []
    for flight in Aircraft.plane_list:
        flights_list.append(flight.to_dict())
    return jsonify(flights_list)

@app_views.route('/flight/<string:flight_id>', methods=['GET'], strict_slashes=False)
def flight(flight_id):
    """ prints all flight information based on ID's given"""
    for flight in Aircraft.plane_list:
        if flight.FlightID == flight_id:
            return jsonify(flight)
    abort(404)

@app_views.route('/create', methods=['GET'], strict_slashes=False)
def do_create(self, arg):
    """creates a plane based in its id, if id is none, create all planes"""
    args = arg.split()
    Airport.reload(aeropuerto)
    if len(args) == 0:
        for plane in Airport.airplane_list:
            if plane not in Airport.mapped_planes:
                avion = Aircraft(str(plane))
                Airport.mapped_planes.append(plane)
        return False
    for pos in range(len(args)):
        if (args[pos] not in Airport.airplane_list):
            print("**Invalid FlightID: {:}. Run callsigns for valid id's**".format(args[pos]))
        else:
            if args[pos] not in Airport.mapped_planes:
                avion = Aircraft(args[pos])
                Airport.mapped_planes.append(args[pos])
                avion.create_estimated_flightpath()
            else:
                print("**{:} Already mapped".format(args[pos]))

def do_planes(self, arg):
    """ prints all flight information based on ID's given"""
    args = arg.split()
    if len(args) == 0:
        for obj in Aircraft.plane_list:
            print(obj)
    if len(args) == 1:
        for obj in Aircraft.plane_list:
            if str(obj.FlightID)  == str(args[0]):
                print(obj)

def do_update(self, arg):
    """updates the current location and time of a given aircraft"""
    args = arg.split()
    if len(args) == 0:
        print("missing ID")
    if len(args) == 1:
        for obj in Aircraft.plane_list:
            if str(obj.FlightID)  == str(args[0]):
                obj.update()
                print(obj)
    
#this method breaks the list generated of collisions, double imput
def do_collision(self, arg):
    """prints collision between 2 given aircrafts"""
    args = arg.split()
    avion1 = avion2 = None
    if len(args) <= 1:
        print("missing ID´s")
    if len(args) == 2:
        for obj in Aircraft.plane_list:
            if str(obj.FlightID)  == str(args[0]):
                avion1 = obj				
            if str(obj.FlightID)  == str(args[1]):
                avion2 = obj
        if avion1 and avion2:
            collision_list = avion1.collision(avion2)
        for elem in collision_list:
            #arcoseno = math.acos(float(float(elem["crash_longitude"] / 111319.444)))
            print("collision ID = {:}, between {:} and {:}".format(elem["crash_id"], elem["ID1"], elem["ID2"]), end="")
            print(" at {:}, on {:} lat, {:} long, {:} alt".format(elem["crash_time"],
                                                                    elem["crash_latitude"],
                                                                    elem["crash_longitude"],
                                                                    elem["crash_altitude"]))

def do_allcollisions(self, arg):
    """checks collisions between all aicrafts"""
    #allcollision_list = Aircraft.all_collision(Aircraft.plane_list)
    allcollision_list = Airport.map_collisions
    for elem in allcollision_list:
        #arcoseno = math.acos(float(elem["crash_longitude"] / 111319.444))
        print("collision between {:} and {:}".format(elem["ID1"], elem["ID2"]), end="")
        print(" at {:}, on {:} lat, {:} long, {:} alt".format(elem["crash_time"],
                                                                elem["crash_latitude"],
                                                                elem["crash_longitude"],
                                                                elem["crash_altitude"]))

def do_newroute(self, arg):
    """new route suggestion"""
    args = arg.split()
    avion1 = None
    if len(args) == 0:
        print("missing ID´s")
    for obj in Aircraft.plane_list:
        if str(obj.FlightID)  == str(args[0]):
            avion1 = obj
    if avion1 is not None:
        print(avion1.collision_l) #if self.new_route(self):
    
def do_fids(self, arg):
    """prints a list of all airplanes available for creadtion"""
    Airport.airplane_list = models.storage.all_ids()
    print(Airport.airplane_list)

def do_accept_newpath(self, arg):
    """"accepts new route of changes"""
    args = arg.split()
    if (len(args) == 0):
        for avion in Aircraft.plane_list:
            if len(avion.suggested_flightpath) > 0:
                avion.switch_manifesto()
                avion.suggested_flightpath = []
    else:
        for avion in Aircraft.plane_list:
            if str(avion.FlightID) == str(args[0]):
                if len(avion.suggested_flightpath) > 0:
                    avion.switch_manifesto()
                    avion.suggested_flightpath = []
