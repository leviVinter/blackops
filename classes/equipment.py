#!/usr/bin/env python3

"""
Module for Equipment class
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from material import Material

class Equipment(Material):
    """ Weapon class """
    __tablename__ = 'equipment'
    id = Column(Integer, ForeignKey('material.id'), primary_key=True)
    description = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'equipment',
    }

    def __init__(self, name, code, description):
        super().__init__(name, code)
        self.description = description

    def get_description(self):
        """ Return description """
        return self.description

    def get_info(self):
        """ Return info about object """
        my_string = "Equipment. Model name: {}. Description: {}"
        return my_string.format(self.name, self.description)


