#!/usr/bin/python3
"""
Contains class BaseModel
"""

import models
import copy



class Aircraft:
    "Class model for all aircrafts"

    def __init__(self, *args, **status):
        self.id = 0 """query of ID in Aircrafts table"""
        self.type = 1 """query of type in Aircrafts table"""
        self.registration = 1 """query of regi in Aircrafts table"""
        self.airline = 1 """query of airline in Aircrafts table"""
        self.country = 1 """query of country in Aircrafts table"""
        self.ICAO = 1 """query of ICAO in Aircrafts table"""
        self.flightstatus  = {} """copy.deepcopy(status)""" """data base query"""

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
    def update(self):
        """updates information of an aircraft"""
        self.country = 2 """query of country in Aircrafts table"""
