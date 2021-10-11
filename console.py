#!/usr/bin/python3
""" console """

import cmd
import json
import models
import pandas as pd
from models.aircraft import Aircraft
from models.airport import Airport

classes = {"Aircraft": Aircraft}
obj_list = []
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
		avion = Aircraft(args[0])
		obj_list.append(avion)

	def do_add(self, arg):
		args = arg.split()
		if len(args) == 0:
			print("**Missing: id**")
			return False
		for obj in obj_list:
			if str(obj.id)  == str(args[0]):
				if aeropuerto.can_add(obj):
					print("Adding plane to airspace...")
					aeropuerto.add_plane(obj)

	def do_planes(self, arg):
		""" prints all flight information based on ID's given"""
		args = arg.split()
		if len(args) == 0:
			print("missing ID")
		if len(args) == 1:
			for obj in obj_list:
				if str(obj.id)  == str(args[0]):
					print(obj)

	def do_airports(self, arg):
		print(aeropuerto)

	def do_update(self, arg):
		args = arg.split()
		if len(args) == 0:
			print("missing ID")
		if len(args) == 1:
			for obj in obj_list:
				if str(obj.id)  == str(args[0]):
					obj.update()
					print(obj)

	def do_collision(self, arg):
		args = arg.split()
		avion1 = avion2 = None
		if len(args) <= 1:
			print("missing ID´s")
		if len(args) == 2:
			for obj in obj_list:
				if str(obj.id)  == str(args[0]):
					avion1 = obj				
				if str(obj.id)  == str(args[1]):
					avion2 = obj
			if avion1 and avion2:
				avion1.collision(avion2)

	def do_allcollisons(self, arg):
		"""checks collisions between all aicrafts"""
		Aircraft.all_collision(obj_list)


if __name__ == '__main__':
    ATCAScmd().cmdloop()
