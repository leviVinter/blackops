#!/usr/bin/env python3

""" Unittest for Explosive module """

import sys
sys.path.insert(0, "../classes")
import unittest
from explosive import Explosive
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
        explosive = self.session.query(Explosive)\
                    .filter_by(name='C4').first()
        info = "Explosive. Model name: {}."
        self.assertEqual(explosive.get_info(),
                         info.format("C4"))


if __name__ == "__main__":
    unittest.main()
