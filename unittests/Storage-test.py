#!/usr/bin/env python3

""" Unittest for Material module """

import sys
sys.path.insert(0, "../classes")
import unittest
from storage import Storage
from material import Material
from weapon import Weapon
from equipment import Equipment
from explosive import Explosive
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestCase(unittest.TestCase):
    """ Submodule for unittest """
    engine = create_engine('sqlite:///../db/test-blackops.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        self.storage = Storage()
        for material in self.session.query(Material).all():
            self.storage.all_material.add(material)

    def tearDown(self):
        self.session.rollback()

    def test_get_material(self):
        """ Test get_material method """
        explosive = self.session.query(Explosive)\
                   .filter_by(id=2).first()
        self.assertEqual(self.storage.get_material(material_id=2), explosive)
        equipment = self.session.query(Equipment)\
                   .filter_by(id=3).first()
        self.assertEqual(self.storage.get_material(material_id=3), equipment)
        self.assertEqual(len(self.storage.get_material(code="A")),
                         1)

    def test_add_material(self):
        """ Test add_material method """
        weapon = Weapon("Mk22", "AE", "Handgun", "56x22")
        first_size = self.storage.all_material.size()
        self.assertEqual(first_size, 3)
        self.storage.add_material(weapon)
        self.assertEqual(self.storage.all_material.size(), first_size + 1)
        
    def test_remove_material(self):
        """ Test remove_material method """
        first_size = self.storage.all_material.size()
        self.storage.remove_material(1)
        new_size = self.storage.all_material.size()
        self.assertEqual(new_size, first_size - 1)


if __name__ == "__main__":
    unittest.main()

