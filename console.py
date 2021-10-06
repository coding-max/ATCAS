#!/usr/bin/python3
""" console """

import cmd
import json
import models
from models.aircraft import Aircraft
"""from models.airport import Airport"""

classes = {"Aircraft": Aircraft}

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
		avion2 = Aircraft()
		print(avion2.airline)
		if len(args) == 0:
			print("** No class selected **")
			return False
		if args[0] not in classes:
			print("**wrong class**")
			return False
		if len(args) == 1:
			print("**missing: type, registration, ariline, country, ICAO**")
			return False
		if len(args) == 2:
			print("**missing: registration, ariline, country, ICAO**")
			return False
		if len(args) == 3:
			print("**missing: ariline, country, ICAO**")
			return False
		if len(args) == 4:
			print("**missing: country, ICAO**")
			return False
		if len(args) == 5:
			print("**missing: ICAO**")
			return False
		if len(args) == 6:
			avion1 = Aircraft(args)
			avion1.aprint()
			s = json.dumps(avion1.__dict__)
			print(s)
			out_file = open("myfile{:}.json".format(avion1.id), "a")
			json.dump(s, out_file, indent = 6)
			out_file.close()
			ins_count = open("myfile.json".format(avion1.id), "w")
			json.dump(avion1.id, ins_count, indent = 6)
			ins_count.close()

	def do_print(self, arg):
		""" prints all flight information based on ID's given"""
		args = arg.split()
		if len(args) == 0:
			print("missing ID")
		if len(args) == 1:
			print(models.storage.aircraft_query_id(args[1]))


if __name__ == '__main__':
    ATCAScmd().cmdloop()
