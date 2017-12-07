#!/usr/bin/env python3

"""
Module for Weapon class
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from material import Material

class Weapon(Material):
    """ Weapon class """
    __tablename__ = 'weapons'
    id = Column(Integer, ForeignKey('material.id'), primary_key=True)
    weapon_type = Column(String)
    ammo_type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'weapon',
    }

    def __init__(self, name, code, weapon_type, ammo_type):
        super().__init__(name, code)
        self.weapon_type = weapon_type
        self.ammo_type = ammo_type

    def get_weapon_type(self):
        """ Return weapon_type """
        return self.weapon_type

    def get_ammo_type(self):
        """ Return ammo_type """
        return self.ammo_type

    def get_info(self):
        """ Return info about object """
        my_string = """Weapon type: {}. Model name: {}.
Ammunition used: {}"""
        return my_string.format(self.weapon_type, self.name, self.ammo_type)


