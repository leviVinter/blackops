#!/usr/bin/env python3

""" Unittest for Soldier module """

import sys
sys.path.insert(0, "../classes")
import unittest
from soldier import Soldier
from assault import Assault
from weapon import Weapon
from explosive import Explosive
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestCase(unittest.TestCase):
    """ Submodule for unittest """
    engine = create_engine('sqlite:///../db/test-blackops.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    soldier = session.query(Soldier).filter_by(fname="James").first()
    weapon = session.query(Weapon).filter_by(name="AK-12").first()

    def tearDown(self):
        self.soldier.unbook_material()
        self.session.rollback()

    def test_book_material(self):
        """ Test book_material method """
        assault = self.session.query(Assault).filter_by(fname="James").first()
        explosive = self.session.query(Explosive).filter_by(name="C4").first()
        first_size = assault.material.size()
        self.assertEqual(first_size, 0)
        booked = assault.book_material(self.weapon)
        self.assertTrue(booked)
        booked = assault.book_material(explosive)
        self.assertFalse(booked)
        second_size = assault.material.size()
        self.assertEqual(second_size, first_size + 1)

    def test_unbook_material(self):
        """ Test unbook_material method """
        weapon = self.session.query(Weapon).filter_by(name="AK-12").first()
        self.soldier.book_material(weapon)
        first_size = self.soldier.material.size()
        self.assertEqual(first_size, 1)
        self.soldier.unbook_material([1])
        second_size = self.soldier.material.size()
        self.assertEqual(second_size, first_size - 1)
        self.assertFalse(self.soldier.unbook_material())

    def test_get_material(self):
        """ Test get_material method """
        self.soldier.book_material(self.weapon)
        a_material = self.soldier.get_material(1)
        self.assertIs(a_material, self.weapon)

    def test_get_id(self):
        """ Test get_id method """
        an_id = self.soldier.get_id()
        self.assertEqual(an_id, 1)

    def test_get_fname(self):
        """ Test get_fname method """
        fname = self.soldier.get_fname()
        self.assertEqual(fname, "James")

    def test_get_lname(self):
        """ Test get_lname method """
        lname = self.soldier.get_lname()
        self.assertEqual(lname, "Becker")

    def test_get_name(self):
        """ Test get_name method """
        name = self.soldier.get_name()
        self.assertEqual(name, "James Becker")

    def test_get_type(self):
        """ Test get_type method """
        a_type = self.soldier.get_type()
        self.assertEqual(a_type, "assault")

    def test_get_code(self):
        """ Test get_code method """
        a_code = self.soldier.get_code()
        self.assertEqual(a_code, "A")

if __name__ == "__main__":
    unittest.main()
