#!/usr/bin/python3
"""
Contains class BaseModel
"""

from console import ATCAScmd

ATCAScmd.do_create("create", "1")
ATCAScmd.do_create("create", "2")
ATCAScmd.do_print("print", "1")
ATCAScmd.do_collision("collision", "1 2")
