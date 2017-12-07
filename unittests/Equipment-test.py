#!/usr/bin/env python3

""" Unittest for Equipment module """

import sys
sys.path.insert(0, "../classes")
import unittest
from equipment import Equipment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestCase(unittest.TestCase):
    """ Submodule for unittest """
    engine = create_engine('sqlite:///../db/test-blackops.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    equipment = session.query(Equipment)\
                .filter_by(name='Motion Sensor').first()

    def tearDown(self):
        self.session.rollback()

    def test_get_description(self):
        """ Test get_description method """
        descr = self.equipment.get_description()
        self.assertEqual(descr, "Signals if there are any movements.")

    def test_get_info(self):
        """ Test get_info method """
        info = "Equipment. Model name: {}. Description: {}"
        descr = "Signals if there are any movements."
        self.assertEqual(self.equipment.get_info(),
                         info.format("Motion Sensor", descr))


if __name__ == "__main__":
    unittest.main()
