#!/usr/bin/env python3

"""
Module for Material class
"""

from sqlalchemy import Column, String, Integer, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Material(Base):
    """ Parent class for different material """
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    booked = Column(BOOLEAN)
    booked_by = Column(Integer)
    code = Column(String)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'material',
        'polymorphic_on':type,
        'with_polymorphic':'*'
    }

    def __init__(self, name, code):
        self.name = name
        self.booked = False
        self.booked_by = None
        self.code = code
    
    def book(self, booked_by):
        """ Book this material """
        self.booked = True
        self.booked_by = booked_by

    def unbook(self):
        """ Unbook this material """
        self.booked = False
        self.booked_by = None

    def is_booked(self):
        """ Return booked status """
        return self.booked

    def get_booked_by(self):
        """ Return booked_by """
        return self.booked_by

    def get_id(self):
        """ Return id """
        return self.id

    def get_name(self):
        """ Return name """
        return self.name

    def get_code(self):
        """ Return code """
        return self.code

    def get_type(self):
        """ Return type """
        return self.type

    def __gt__(self, other):
        if self.type > other.type:
            return True
        if self.type == other.type:
            if self.name.lower() > other.name.lower():
                return True
        return False
