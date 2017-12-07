#!/usr/bin/env python3

"""
Module for Storage class
"""

from material import Material
from ordered_list import OrderedList

class Storage():
    """ Storage for material """

    def __init__(self):
        self.all_material = OrderedList()

    def add_material(self, new_material):
        """ Add new material to list """
        if not isinstance(new_material, Material):
            return False
        self.all_material.add(new_material)

    def remove_material(self, material_id):
        """ Remove material based on id """
        try:
            material_id = int(material_id)
        except ValueError:
            return False
        return self.all_material.remove(material_id)

    def get_all_material(self):
        """ Get all material """
        return self.all_material.get_all()
    
    def get_material_by_id(self, material_id):
        """ Get material by ID number """
        try:
            material_id = int(material_id)
        except ValueError:
            return False
        return self.all_material.get_by_id(material_id)

    def get_material_by_code(self, code):
        """ Get material by code string """
        if not isinstance(code, str):
            return False
        return self.all_material.get_by_code(code)
