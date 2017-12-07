#!/usr/bin/env python3

"""
Module for Soldier class
"""

from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.ext.declarative import declarative_base
from ordered_list import OrderedList
from material import Material

Base = declarative_base()

class Soldier(Base):
    """ Parent class for different soldiers """
    __tablename__ = 'soldiers'

    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'soldier',
        'polymorphic_on':type,
        'with_polymorphic':'*'
    }

    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
        self.material = OrderedList()

    @orm.reconstructor
    def init_on_load(self):
        """ When loaded from database """
        self.material = OrderedList()

    def book_material(self, material):
        """ Add material to list """
        if not isinstance(material, Material):
            return False
        material_code = material.get_code()
        if not self.code in material_code:
            return False
        material.book(self.id)
        self.material.add(material)
        return True

    def unbook_material(self, ids=None):
        """ Remove from material list """
        # Unbook all material
        if ids == None:
            # Get Material objects
            all_material = self.material.get_all()
            if not all_material:
                return False
            for material in all_material:
                material.unbook()
            self.material = OrderedList()
            return all_material
        
        # Unbook material based on ids
        unbooked = []
        for mat_id in ids:
            try:
                mat_id = int(mat_id)
            except ValueError:
                continue
            # Handle material object
            material = self.material.get_by_id(mat_id)
            if material:
                material.unbook()
                self.material.remove(mat_id)
                unbooked.append(material)

        if len(unbooked) == 0:
            return False
        return unbooked

    def get_material(self, material_id=None):
        """ Get from material list """
        if material_id == None:
            return self.material.get_all()
        try:
            material_id = int(material_id)
        except ValueError:
            return False
        return self.material.get_by_id(material_id)

    def get_id(self):
        """ Return id """
        return self.id

    def get_fname(self):
        """ Return fname """
        return self.fname

    def get_lname(self):
        """ Return lname """
        return self.lname

    def get_name(self):
        """ Return full name """
        return self.fname + " " + self.lname

    def get_type(self):
        """ Return type """
        return self.type

    def get_code(self):
        """ Return code """
        return self.code

    def __gt__(self, other):
        if self.type > other.type:
            return True
        if self.type == other.type:
            if self.lname > other.lname:
                return True
        return False
