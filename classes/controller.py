#!/usr/bin/evn python3

""" Module for Controller class """

from ordered_list import OrderedList
from storage import Storage
from soldier import Soldier
from assault import Assault
from engineer import Engineer
from recon import Recon
from material import Material
from weapon import Weapon
from explosive import Explosive
from equipment import Equipment

class Controller():
    """ Controller class """

    def __init__(self, session):

        self.soldiers = OrderedList()
        self.storage = Storage()
        self.session = session

        self.fetch_soldiers_from_db()
        self.fetch_material_from_db()
        self.fetch_material_to_soldiers()

    def fetch_soldiers_from_db(self):
        """ Get all soldiers from database """
        soldiers_list = self.session.query(Soldier).all()
        for soldier in soldiers_list:
            self.soldiers.add(soldier)
    
    def fetch_material_from_db(self):
        """ Get all material from database """
        material_list = self.session.query(Material).all()
        for material in material_list:
            if not material.is_booked():
                self.storage.add_material(material)

    def fetch_material_to_soldiers(self):
        """ Give booked material to soldiers """
        booked_material = self.session.query(Material).filter_by(booked=True)
        for material in booked_material:
            soldier_id = material.get_booked_by()
            soldier = self.soldiers.get_by_id(soldier_id)
            soldier.book_material(material)

    def hand_out_material(self, material_ids, soldier_id):
        """ Take material from storage and give to a soldier """
        material_for_soldier = []
        material_to_remove = []
        # Get Soldier instance
        soldier = self.soldiers.get_by_id(soldier_id)
        if not soldier:
            return False
        # Get material from storage with matching ids
        for material_id in material_ids:
            material = self.storage.get_material_by_id(material_id)
            if material:
                material_for_soldier.append(material)
        if len(material_for_soldier) == 0:
            return False
        # Give material to soldier
        for material in material_for_soldier:
            if soldier.book_material(material):
                db_material = self.session.query(Material)\
                              .filter_by(id=material.get_id()).first()
                db_material.book(int(soldier_id))
                material_to_remove.append(material)
        if len(material_to_remove) == 0:
            return False
        # Remove material from storage
        for material in material_to_remove:
            self.storage.remove_material(material.get_id())
        self.session.commit()
        return True

    def hand_in_material(self, material_ids, soldier_id):
        """ Remove material from soldier and put into storage """
        # Get Soldier instance or False
        soldier = self.soldiers.get_by_id(soldier_id)
        if not soldier:
            return False
        # Get material list
        material_for_storage = soldier.unbook_material(material_ids)
        if not material_for_storage:
            return False
        for material in material_for_storage:
            self.storage.add_material(material)
            db_material = self.session.query(Material)\
                          .filter_by(id=material.get_id()).first()
            db_material.unbook()
        self.session.commit() 
        return True

    def add_soldier(self, fname, lname, soldier_class):
        """ Add a soldier to soldier list """
        soldier = None
        if soldier_class == "assault":
            soldier = Assault(fname, lname)
        elif soldier_class == "engineer":
            soldier = Engineer(fname, lname)
        elif soldier_class == "recon":
            soldier = Recon(fname, lname)
        
        if not soldier:
            return False

        self.session.add(soldier)
        self.session.commit()
        self.session.query(Soldier).filter_by(id=soldier.get_id()).first()
        self.soldiers.add(soldier)
        return True

    def remove_soldier(self, soldier_id):
        """ Remove soldier from soldier list """
        try:
            soldier_id = int(soldier_id)
        except ValueError:
            return False
        soldier = self.soldiers.get_by_id(soldier_id)
        if not soldier:
            return False

        material_to_storage = soldier.unbook_material()
        if material_to_storage:
            for material in material_to_storage:
                db_material = self.session.query(Material)\
                              .filter_by(id=material.get_id()).first()
                db_material.unbook()
                self.storage.add_material(material)
        soldier = self.session.query(Soldier).filter_by(id=soldier_id).first()
        self.session.delete(soldier)
        self.session.commit()
        self.soldiers.remove(soldier_id)

        return True

    def change_soldier_type(self, soldier_id, soldier_type):
        """ Change a soldier's type """
        if not isinstance(soldier_type, str):
            return False
        try:
            soldier_id = int(soldier_id)
        except ValueError:
            return False
        soldier = self.soldiers.get_by_id(soldier_id)
        if not soldier:
            return False
        fname = soldier.get_fname()
        lname = soldier.get_lname()
        self.remove_soldier(soldier_id)
        self.add_soldier(fname, lname, soldier_type)
        return True

    def get_soldiers(self, code=None):
        """ Get soldiers, either all or by code"""
        if not code:
            return self.soldiers.get_all()
        if not isinstance(code, str):
            return False
        return self.soldiers.get_by_code(code)

    def get_soldier(self, soldier_id):
        """ Get soldier by ID """
        try:
            soldier_id = int(soldier_id)
        except ValueError:
            return False
        return self.soldiers.get_by_id(soldier_id)

    def add_material(self, name, code, attr_dict, material_type):
        """ Add material to storage """
        name_correct = isinstance(name, str)
        code_correct = isinstance(code, str)
        attr_dict_correct = isinstance(attr_dict, dict)
        if not name_correct or not code_correct \
           or not attr_dict_correct:
            return False

        material = None
        try:
            if material_type == "weapon":
                weapon_type = attr_dict["weapon_type"]
                ammo_type = attr_dict["ammo_type"]
                material = Weapon(name, code, weapon_type, ammo_type)
            elif material_type == "explosive":
                material = Explosive(name, code)
            elif material_type == "equipment":
                descr = attr_dict["description"]
                material = Equipment(name, code, descr)
        except KeyError:
            return False

        if not material:
            return False

        self.session.add(material)
        self.session.commit()
        self.session.query(Material).filter_by(id=material.get_id()).first()
        self.storage.add_material(material)
        return True


    def remove_material_by_id(self, material_id):
        """ Remove material by ID number """
        material_list = self.session.query(Material)\
                    .filter_by(id=material_id).all()
        return self.remove_material(material_list)

    def remove_material_by_name(self, material_name, limit):
        """ Remove material by name string """
        try:
            limit = int(limit)
        except ValueError:
            return False
        material_list = self.session.query(Material)\
                        .filter_by(name=material_name)\
                        .limit(limit).all()
        return self.remove_material(material_list)

    def remove_material(self, material_list):
        """ Remove material"""
        if not len(material_list) > 0:
            return False
        for material in material_list:
            material_id = material.get_id()
            if material.is_booked():
                soldier_id = material.get_booked_by()
                soldier = self.soldiers.get_by_id(soldier_id)
                soldier.unbook_material(material_id)
            self.storage.remove_material(material_id)
            self.session.delete(material)
        self.session.commit()
        return True

    def get_all_material(self, distinct=False):
        """ Get all material """
        material_list = self.storage.get_all_material()
        return self.get_material(material_list, distinct)

    def get_material_by_id(self, material_id):
        """ Get material by ID number """
        try:
            material_id = int(material_id)
        except ValueError:
            return False
        return self.storage.get_material_by_id(material_id)

    def get_material_by_code(self, code, distinct=False):
        """ Get material by code string """
        if not isinstance(code, str):
            return False
        material_list = self.storage.get_material_by_code(code=code)
        return self.get_material(material_list, distinct)

    def get_booked_material(self, distinct=False):
        """ Get booked material """
        material_list = []
        for soldier in self.get_soldiers():
            soldier_material = soldier.get_material()
            if soldier_material:
                for material in soldier_material:
                    material_list.append(material)
        return self.get_material(material_list, distinct)

    def get_material(self, material_list, distinct=False):
        """ Return material"""
        if len(material_list) == 0 or not distinct:
            # Return list of material
            return material_list
        # Return list of tuples
        return self.get_distinct_materials(material_list)

    def get_distinct_materials(self, material_list):
        """ Get tuples of each material and it's quantity """
        distinct_materials = []
        material_quantity = {}
        material_tuples = []
        for material in material_list:
            name = material.get_name()
            material_quantity[name] = material_quantity.get(name, 0) + 1
            if material_quantity[name] == 1:
                distinct_materials.append(material)

        for distinct in distinct_materials:
            quantity = material_quantity[distinct.get_name()]
            material_tuples.append((distinct, quantity))

        return material_tuples

    def material_name_exists(self, name):
        """ Check if material name already exists in db """
        if self.session.query(Material).filter_by(name=name).first():
            return True
        return False
