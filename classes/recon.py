#!/usr/bin/env python3

"""
Module for Recon class
"""

from sqlalchemy import Column, Integer, ForeignKey
from soldier import Soldier

class Recon(Soldier):
    """ Recon class """
    __tablename__ = 'recons'
    id = Column(Integer, ForeignKey('soldiers.id'), primary_key=True)
    code = "R"

    __mapper_args__ = {
        'polymorphic_identity':'recon',
    }

    def __init__(self, fname, lname):
        super().__init__(fname, lname)

    def get_info(self):
        """ Return string with info """
        info = "{fn} {ln}: Recon."
        return info.format(fn=self.fname, ln=self.lname)


