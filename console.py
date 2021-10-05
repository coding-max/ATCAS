#!/usr/bin/python3
""" console """

import cmd
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
		"creates a new class"
		args = arg.split()
		if len(args) == 0:
			print("** No class selected **")
			return False
		if args[0] not in classes:
			print("**wrong class**")
			return False
		if len(args) == 1:
			print("**Created empty class, run update to set values**")
		if len(args) == 2:
			print("**Created with ID**")
		if len(args) == 3:
			print("**ID and type**")
		if len(args) == 4:
			print("**ID, type and registration**")
		if len(args) == 5:
			print("**ID, type, registration, ariline**")
		if len(args) == 6:
			print("**ID, type, registration, ariline, country**")
		if len(args) == 7:
			print("**ID, type, registration, ariline, country, ICAO**")
	
	def do_update(self):
		self.update


if __name__ == '__main__':
    ATCAScmd().cmdloop()
