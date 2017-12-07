#!/usr/bin/env python3

""" Unittest for Controller module """

import sys
sys.path.insert(0, "../classes")
import unittest
from controller import Controller
from material import Material
from soldier import Soldier
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
engine = create_engine("sqlite:///../db/test-blackops.sqlite")


class TestCase(unittest.TestCase):
    """ Submodule for unittest """

    def setUp(self):
        # connect to the database
        self.connection = engine.connect()
        # begin a non-ORM transaction
        self.trans = self.connection.begin()
        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

        self.controller = Controller(self.session)

    def test_init(self):
        """ Test initialization """
        soldier = self.controller.soldiers.get_by_id(1)
        self.assertEqual(soldier.get_id(), 1)

    def test_hand_out_material(self):
        """ Test hand_out_material method """
        soldier_id = 1
        material_ids = [1, 2]
        self.controller.hand_out_material(material_ids, soldier_id)
        soldier = self.controller.soldiers.get_by_id(soldier_id)
        material1 = soldier.get_material(1)
        material2 = soldier.get_material(2)
        self.assertEqual(material1.get_id(), 1)
        self.assertFalse(material2)
        booked_material = self.session.query(Material)\
                          .filter_by(booked=True).one()
        self.assertEqual(booked_material.booked_by, soldier.get_id())

    def test_hand_in_material(self):
        """ Test hand_in_material method """
        # First hand out material
        self.controller.hand_out_material([1], 1)
        first_size = self.controller.storage.all_material.size()
        self.controller.hand_in_material([1, 2], 1)
        second_size = self.controller.storage.all_material.size()
        self.assertEqual(second_size, first_size + 1)

    def test_add_soldier(self):
        """ Test add_soldier method """
        first_size = self.controller.soldiers.size()
        self.controller.add_soldier("Thomas", "Hedlund", "assault")
        second_size = self.controller.soldiers.size()
        self.assertEqual(second_size, first_size + 1)
        new_soldier = self.session.query(Soldier)\
                      .filter_by(fname="Thomas").first()
        self.assertIsInstance(new_soldier, Soldier)

    def test_remove_soldier(self):
        """ Test remove_soldier method """
        soldier = self.session.query(Soldier)\
                  .filter_by(id=1).first()
        self.assertEqual(soldier.get_id(), 1)
        first_size = self.controller.soldiers.size()
        self.assertTrue(self.controller.remove_soldier(1))
        second_size = self.controller.soldiers.size()
        self.assertEqual(second_size, first_size - 1)
        soldier = self.session.query(Soldier)\
                  .filter_by(id=1).first()
        self.assertIsNone(soldier)

    def test_add_material(self):
        """ Test add_material method """
        name = "FY-JS"
        code = "R"
        a_dict = {
            "weapon_type": "Sniper Rifle",
            "ammo_type": "5.8x42mm"
        }
        self.controller.add_material(name, code, a_dict, "weapon")
        weapon = self.session.query(Material).filter_by(name="FY-JS").first()
        self.assertIsInstance(weapon, Material)

    def test_remove_material(self):
        """ Test remove_material method """
        # When material is NOT booked
        material = self.session.query(Material)\
                   .filter_by(id=1).first()
        self.assertIsNotNone(material)
        self.controller.remove_material(1)
        material = self.session.query(Material)\
                   .filter_by(id=1).first()
        self.assertIsNone(material)

        # When material IS booked
        self.controller.hand_out_material([2], 1)
        material = self.session.query(Material)\
                   .filter_by(id=2).first()
        self.assertIsInstance(material, Material)
        self.controller.remove_material(2)
        material = self.session.query(Material)\
                   .filter_by(id=2).first()
        self.assertIsNone(material)

    def test_change_soldier_type(self):
        """ Test change_soldier_type method """
        soldier = self.session.query(Soldier)\
                  .filter_by(fname="James").first()
        self.assertEqual(soldier.code, "A")
        self.assertEqual(soldier.get_fname(), "James")
        self.controller.change_soldier_type(1, "recon")
        soldier = self.session.query(Soldier)\
                  .filter_by(id=1).first()
        self.assertIsNone(soldier)
        soldier = self.session.query(Soldier)\
                  .filter_by(fname="James").first()
        self.assertEqual(soldier.code, "R")
        self.assertEqual(soldier.get_fname(), "James")

    def test_get_soldiers(self):
        """ Test get_soldiers method """
        # Get all soldiers
        soldiers = self.controller.get_soldiers()
        self.assertEqual(len(soldiers), 6)
        self.assertIsInstance(soldiers[0], Soldier)
        # Get soldiers based on type
        soldiers = self.controller.get_soldiers(code="A")
        self.assertEqual(len(soldiers), 2)
        self.assertIsInstance(soldiers[0], Soldier)

    def test_get_material(self):
        """ Test get_material method """
        # Get all material
        material = self.controller.get_material()
        self.assertEqual(len(material), 3)

        # Get material based on ID
        material = self.controller.get_material(material_id=1)
        self.assertIsInstance(material, Material)

        # Get material based on code
        material = self.controller.get_material(code="A")
        self.assertEqual(len(material), 1)

    def test_material_name_exists(self):
        """ material_name_exists method """
        exists = self.controller.material_name_exists("AK-12")
        self.assertTrue(exists)
        exists = self.controller.material_name_exists("hello")
        self.assertFalse(exists)

    def tearDown(self):
        self.session.close()
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()
        # return connection to the Engine
        self.connection.close()

if __name__ == "__main__":
    unittest.main()

