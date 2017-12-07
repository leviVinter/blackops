#!/usr/bin/env python3

""" Unittest for Recon module """

import sys
sys.path.insert(0, "../classes")
import unittest
from recon import Recon
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
        recon = self.session.query(Recon).filter_by(fname="Sami").first()
        info = "{} {}: Recon."
        self.assertEqual(recon.get_info(), info.format("Sami", "Salo"))
        self.assertEqual(recon.code, "R")


if __name__ == "__main__":
    unittest.main()

