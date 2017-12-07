#!/usr/bin/env python3

""" Unittest for Engineer module """

import sys
sys.path.insert(0, "../classes")
import unittest
from engineer import Engineer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestCase(unittest.TestCase):
    """ Submodule for unittest """
    engine = create_engine('sqlite:///../db/test-blackops.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()

    def tearDown(self):
        self.session.rollback()

    def test_get_info(self):
        """ Test get_info method """
        engineer = self.session.query(Engineer).filter_by(fname="Bill")\
                   .first()
        info = "{} {}: Engineer."
        self.assertEqual(engineer.get_info(), info.format("Bill", "Packett"))
        self.assertEqual(engineer.code, "E")


if __name__ == "__main__":
    unittest.main()

