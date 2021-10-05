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
		if args[0] in classes:
			if len(args) != 5:
				print("** missing atribute**")
				return False
		print("llegue")
		print(args)

if __name__ == '__main__':
    ATCAScmd().cmdloop()
