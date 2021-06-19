#!/usr/bin/env python3
'''
Functions and classes for handling `Record` folders
Niema Moshiri 2021
'''
from .OpenData import OpenData
from glob import glob
from os.path import isdir

class Record:
    '''Class to represent `Record` folder'''
    def __init__(self, path):
        '''``Record`` constructor'''
        if not isdir(path):
            raise ValueError("Record folder not found: %s" % path)
        self.path = path.rstrip('/')
        self.contents = OpenData('%s/contents' % self.path)
        print(self.contents.get_dict())
