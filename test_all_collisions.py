#!/usr/bin/python3
"""
Contains class BaseModel
"""

from console import ATCAScmd

ATCAScmd.do_create("create", "1")
ATCAScmd.do_create("create", "2")
ATCAScmd.do_create("create", "5")
ATCAScmd.do_create("create", "3")
ATCAScmd.do_create("create", "4")
ATCAScmd.do_allcollisons("allcollisions", "")
