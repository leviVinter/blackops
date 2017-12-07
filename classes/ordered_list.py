#!/usr/bin/env python3

"""
Module for OrderedList class
"""

# Imports
from node import Node

class OrderedList:
    """ Ordered list """
    def __init__(self):
        self.head = None

    def is_empty(self):
        """ Checks if list is empty """
        return self.head is None

    def add(self, item):
        """
        Add item to list
        """
        temp = Node(item)
        temp.set_next(self.head)
        self.head = temp
        # Sort the list
        for i in range(self.size()-1):
            current_item = self.get(i)
            next_item = self.get(i+1)
            if current_item > next_item:
                self._set(i, next_item)
                self._set(i+1, current_item)

    def size(self):
        """ Return size of list """
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.get_next()
        return count

    def _set(self, index, newdata):
        """
        Set node-data in list at specific index
        """
        # Här gäller det att sätta nodens data till 'newdata' på rätt
        # index-position.
        current = self.head
        count = 0
        while count < index and current != None:
            count += 1
            current = current.get_next()
        if current == None:
            print("Index out of range")
            return False
        current.set_data(newdata)
        return True

    def get(self, index):
        """
        Returns node data based on index
        """
        # Likt 'set()' gäller det att traversera listan men här ska du
        # returnera datan för värdet på rätt index-plats
        current = self.head
        count = 0
        while count < index and current != None:
            count = count + 1
            current = current.get_next()
        if current == None:
            return False
        else:
            return current.get_data()

    def get_all(self):
        """ Returns all data """
        current = self.head
        all_data = []
        while current != None:
            all_data.append(current.get_data())
            current = current.get_next()
        if len(all_data) == 0:
            return False
        return all_data

    def get_by_id(self, an_id):
        """ Return node data base on id """
        try:
            an_id = int(an_id)
        except ValueError:
            return False
        current = self.head
        while current != None and \
              current.get_data().id != an_id:
            current = current.get_next()
        if current == None:
            return False
        return current.get_data()

    def get_by_code(self, code):
        """ Return node data who all shares code """
        current = self.head
        matches = []
        while current != None:
            if code in current.get_data().code:
                matches.append(current.get_data())
            current = current.get_next()
        if len(matches) == 0:
            return False
        return matches

    def remove(self, an_id):
        """
        Removes item from list
        """
        current = self.head
        previous = None
        while current != None and \
              current.get_data().id != an_id:
            previous = current
            current = current.get_next()
        if current == None:
            return False
        if previous == None:
            self.head = self.head.get_next()
        else:
            previous.set_next(current.get_next())
        return True
