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
        if 'data' in self.contents and '__type__' in self.contents['data'] and self.contents['data']['__type__'] == 'PxStream':
            self.contents['data']['opendata'] = OpenData('%s/%s' % (self.path, self.contents['data']['__value__'])).get_dict()
        if 'layout' in self.contents and '__type__' in self.contents['layout'] and self.contents['layout']['__type__'] == 'PxStream':
            self.contents['layout']['opendata'] = OpenData('%s/%s' % (self.path, self.contents['layout']['__value__'])).get_dict()

    def get_dict(self):
        '''Get a `dict` representation of this `OpenData` object

        Returns:
            A `dict` representation of this `OpenData object
        '''
        return {'path': self.path, 'contents': self.contents.get_dict()}
