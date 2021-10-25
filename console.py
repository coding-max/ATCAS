#!/usr/bin/python3
""" console """

import cmd
import json
import models
import pandas as pd
from models.aircraft import Aircraft
from models.airport import Airport
import math

aeropuerto = Airport("MVD")

class ATCAScmd(cmd.Cmd):
	prompt = '(^--|-->) '

	def do_EOF(self, arg):
		"""Exits console"""
		return True

	def emptyline(self):
		""" overwriting the emptyline method """
		return False

	def do_quit(self, arg):
		"""Quit command to exit the program"""
		return True

	def do_create(self, arg):
		"""creates a plane based in its id, if id is none, create all planes"""
		args = arg.split()
		Airport.reload(aeropuerto)
		if len(args) == 0:
			for plane in Airport.airplane_list:
				if plane not in Airport.mapped_planes:
					avion = Aircraft(str(plane))
					Airport.mapped_planes.append(plane)
					avion.create_estimated_flightpath()
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

	def do_add(self, arg):
		"""adds a plane to the current airspace"""
		args = arg.split()
		if len(args) == 0:
			print("**Missing: id**")
			return False
		for obj in Aircraft.plane_list:
			if str(obj.FlightID)  == str(args[0]):
				if aeropuerto.can_add(obj):
					print("Adding plane to airspace...")
					aeropuerto.add_plane(obj)

	def do_planes(self, arg):
		""" prints all flight information based on ID's given"""
		args = arg.split()
		if len(args) == 0:
			for obj in Aircraft.plane_list:
				print(obj)
		if len(args) == 1:
			for obj in Aircraft.plane_list:
				if str(obj.FlightID) == str(args[0]):
					print(obj)

	#this method creates an instance of a new airport, each time it tryes to print it
	def do_airports(self, arg):
		"""prints planes in current workspace"""
		args = arg.split()
		if len(args) == 0:
			print(aeropuerto)
		else:
			for airports in args:
				print(Airport(airports))

	def do_update(self, arg):
		"""updates the current location and time of a given aircraft"""
		args = arg.split()
		pos = 0
		if len(args) == 0:
			while (Aircraft.plane_list[pos]):
				pos += Aircraft.plane_list[pos].update()
				try:
					Aircraft.plane_list[pos]
				except:
					break
		if len(args) == 1:
			for obj in Aircraft.plane_list:
				if str(obj.FlightID)  == str(args[0]):
					obj.update()
		
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
		ATCAScmd.do_update("", "")
		Aircraft.all_collision(Aircraft.plane_list)
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
			print(avion1.suggested_flightpath)
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
						if (avion.FlightID == "IB420"):
							doc = "420"
						elif (avion.FlightID == "IB969"):
							doc = "969"
						else:
							avion.suggested_flightpath = []
							return False
						with open("././test_flights/{:}.json".format(doc), 'w') as f:
							json.dump("changed", f)
						avion.switch_manifesto()
						avion.suggested_flightpath = []
						print("**Instructions given, awaiting for pilot to obey**")
						return False
					else:
						print("**Flight {:}, has no suggested flightpath**".format(avion.FlightID))
						return False
			print("**Wrong FlightID, run fids for valid ones**")

	def do_takeoff(self, arg):
		"""selects a runway for takeoff"""
		args = arg.split()
		if len(args) == 0:
			print("**Missing FlightID**")
			return False
		for avion in Aircraft.plane_list:
			if str(avion.FlightID) == str(args[0]):
				aeropuerto.desired_runway(avion)


	#method used for tests
	def do_test(self, arg):
		""""method for testing"""
		plane = Aircraft("E480D1")
		print(plane.to_geojson())
		#plane.accept_route()

if __name__ == '__main__':
    ATCAScmd().cmdloop()
