#!/usr/bin/python3
""" console """

import cmd
import json
import models
import pandas as pd
from models.aircraft import Aircraft
from models.airport import Airport
import math

aeropuerto = Airport(1)

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
		args = arg.split()
		if len(args) == 0:
			print("**Missing: id**")
			return False
		if (args[0] not in Airport.airplane_list):
			print("**Invalid: id. Run callsigns for valid id's**")
			return False
		for pos in range(0, len(args)):
			avion = Aircraft(args[pos])

	def do_add(self, arg):
		args = arg.split()
		if len(args) == 0:
			print("**Missing: id**")
			return False
		for obj in Aircraft.plane_list:
			if str(obj.id)  == str(args[0]):
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
				if str(obj.id)  == str(args[0]):
					print(obj)

	def do_airports(self, arg):
		print(aeropuerto)

	def do_update(self, arg):
		args = arg.split()
		if len(args) == 0:
			print("missing ID")
		if len(args) == 1:
			for obj in Aircraft.plane_list:
				if str(obj.id)  == str(args[0]):
					obj.update()
					print(obj)
		

	def do_collision(self, arg):
		args = arg.split()
		avion1 = avion2 = None
		if len(args) <= 1:
			print("missing ID´s")
		if len(args) == 2:
			for obj in Aircraft.plane_list:
				if str(obj.id)  == str(args[0]):
					avion1 = obj				
				if str(obj.id)  == str(args[1]):
					avion2 = obj
			if avion1 and avion2:
				collision_list = avion1.collision(avion2)
			for elem in collision_list:
				#arcoseno = math.acos(float(float(elem["crash_longitude"] / 111319.444)))
				print("collision between {:} and {:}".format(elem["ID1"], elem["ID2"]), end="")
				print(" at {:}, on {:} lat, {:} long, {:} alt".format(elem["crash_time"],
																 	  elem["crash_latitude"],
																 	  elem["crash_longitude"],
																	  elem["crash_altitude"]))

	def do_allcollisions(self, arg):
		"""checks collisions between all aicrafts"""
		allcollision_list = Aircraft.all_collision(Aircraft.plane_list)
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
			if str(obj.id)  == str(args[0]):
				avion1 = obj
		if avion1 is not None:
			print(avion1.collision_l) #if self.new_route(self):
		
	def do_callsigns(self, arg):
		print(Airport.airplane_list)

if __name__ == '__main__':
    ATCAScmd().cmdloop()
