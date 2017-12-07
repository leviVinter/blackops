#!/usr/bin/env python3

""" Unittest for Weapon module """

import sys
sys.path.insert(0, "../classes")
import unittest
from weapon import Weapon
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestCase(unittest.TestCase):
    """ Submodule for unittest """
    engine = create_engine('sqlite:///../db/test-blackops.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    weapon = session.query(Weapon).filter_by(name='AK-12').first()

    def tearDown(self):
        self.session.rollback()

    def test_get_weapon_type(self):
        """ Test get_weapon_type method """
        weapon_type = self.weapon.get_weapon_type()
        self.assertEqual(weapon_type, "Assault Rifle")

    def test_get_ammo_type(self):
        """ Test get_ammo_type method """
        ammo_type = self.weapon.get_ammo_type()
        self.assertEqual(ammo_type, "5.45x39mm")

    def test_get_info(self):
        """ Test get_info method """
        info = """Weapon type: Assault Rifle. Model name: AK-12.
Ammunition used: 5.45x39mm"""
        self.assertEqual(self.weapon.get_info(), info)


if __name__ == "__main__":
    unittest.main()
