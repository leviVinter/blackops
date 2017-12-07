#!/usr/bin/env python3

"""
Module for Engineer class
"""

from sqlalchemy import Column, Integer, ForeignKey
from soldier import Soldier

class Engineer(Soldier):
    """ Engineer class """
    __tablename__ = 'engineers'
    id = Column(Integer, ForeignKey('soldiers.id'), primary_key=True)
    code = "E"

    __mapper_args__ = {
        'polymorphic_identity':'engineer',
    }

    def __init__(self, fname, lname):
        super().__init__(fname, lname)

    def get_info(self):
        """ Return string with info """
        info = "{fn} {ln}: Engineer."
        return info.format(fn=self.fname, ln=self.lname)


