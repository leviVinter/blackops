#!/usr/bin/env python3

"""
Module for Assault class
"""

from sqlalchemy import Column, Integer, ForeignKey
from soldier import Soldier

class Assault(Soldier):
    """ Assault class """
    __tablename__ = 'assaults'
    id = Column(Integer, ForeignKey('soldiers.id'), primary_key=True)
    code = "A"

    __mapper_args__ = {
        'polymorphic_identity':'assault',
    }

    def __init__(self, fname, lname):
        super().__init__(fname, lname)

    def get_info(self):
        """ Return string with info """
        info = "{fn} {ln}: Assault."
        return info.format(fn=self.fname, ln=self.lname)


