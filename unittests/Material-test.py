#!/usr/bin/env python3

""" Unittest for Material module """

import sys
sys.path.insert(0, "../classes")
import unittest
from material import Material
from weapon import Weapon
from explosive import Explosive
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestCase(unittest.TestCase):
    """ Submodule for unittest """
    engine = create_engine('sqlite:///../db/test-blackops.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    material = session.query(Material).filter_by(id=1).first()

    def tearDown(self):
        self.session.rollback()

    def test_book(self):
        """ Test book method """
        self.assertFalse(self.material.booked)
        self.assertIsNone(self.material.booked_by)
        self.material.book("Darth Vader")
        self.assertTrue(self.material.booked)
        self.assertEqual(self.material.booked_by, "Darth Vader")

    def test_unbook(self):
        """ Test unbook method """
        self.material.booked = True
        self.material.booked_by = ("Darth Vader")
        self.assertTrue(self.material.booked)
        self.assertEqual(self.material.booked_by, "Darth Vader")
        self.material.unbook()
        self.assertFalse(self.material.booked)
        self.assertIsNone(self.material.booked_by)

    def test_is_booked(self):
        """ Test is_booked method """
        self.assertFalse(self.material.is_booked())
        self.material.booked = True
        self.assertTrue(self.material.is_booked())

    def test_get_id(self):
        """ Test get_id method """
        material1 = self.session.query(Weapon)\
                    .filter_by(id=1).one()
        material2 = self.session.query(Explosive)\
                    .filter_by(id=2).one()
        self.assertEqual(material1.get_id(), 1)
        self.assertEqual(material2.get_id(), 2)

    def test_get_name(self):
        """ Test get_name method """
        name = self.material.get_name()
        self.assertEqual(name, "AK-12")

    def test_get_code(self):
        """ Test get_code method """
        self.assertEqual(self.material.get_code(), "A")

    def test_get_type(self):
        """ Test get_type method """
        a_type = self.material.get_type()
        self.assertEqual(a_type, "weapon")


if __name__ == "__main__":
    unittest.main()
