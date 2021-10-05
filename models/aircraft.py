#!/usr/bin/python3
"""
Contains class BaseModel
"""

import models
import copy



class Aircraft:
    "Class model for all aircrafts"

    def __init__(self, *args, **status):
        self.type = 1
        self.registration = 1
        self.airline = 1
        self.country = 1
        self.ICAO = 1
        self.flightstatus  = copy.deepcopy(status)
