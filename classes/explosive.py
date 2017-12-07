#!/usr/bin/env python3

"""
Module for Explosive class
"""

from sqlalchemy import Column, Integer, ForeignKey
from material import Material

class Explosive(Material):
    """ Weapon class """
    __tablename__ = 'explosives'
    id = Column(Integer, ForeignKey('material.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'explosive',
    }

    def __init__(self, name, code):
        super().__init__(name, code)

    def get_info(self):
        """ Return info about object """
        my_string = "Explosive. Model name: {}."
        return my_string.format(self.name)



