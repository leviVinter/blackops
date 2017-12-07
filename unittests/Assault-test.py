#!/usr/bin/env python3

""" Unittest for Assault module """

import sys
sys.path.insert(0, "../classes")
import unittest
from assault import Assault
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
        assault = self.session.query(Assault).filter_by(fname="James").first()
        info = "{} {}: Assault."
        self.assertEqual(assault.get_info(), info.format("James", "Becker"))
        self.assertEqual(assault.code, "A")


if __name__ == "__main__":
    unittest.main()

