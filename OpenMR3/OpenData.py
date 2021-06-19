#!/usr/bin/env python3
'''
Functions and classes for handling `OpenData` files (e.g. `contents`, `layout`, etc.)
Niema Moshiri 2021
'''
from lark import Lark, Transformer
from os.path import isfile

opendata_dict_parser = Lark(r'''
    ?value : opendata
           | typedvalue
           | varname
           | dict
           | list
           | ESCAPED_STRING
           | SIGNED_INT
           | SIGNED_FLOAT

    // OpenData-specific types
    opendata                : "OPENDATA" varname dict ";"

    varword : ["@"] CNAME | "T" ESCAPED_STRING
    varname : varword [("." varword)*]

    typedvalue : varname value

    dict : "[" [pair ";" (pair ";")*] "]"
    pair : varname ":" value

    // not sure about lists, because the sample data only has () aka empty
    list : "(" [value ";" (value ";")*] ")"

    %import common.CNAME
    %import common.ESCAPED_STRING
    %import common.SIGNED_FLOAT
    %import common.SIGNED_INT
    %import common.WS
    %ignore WS
    ''', start='opendata')

class OpenDataTransformer(Transformer):
    def opendata(self, parts):
        parts[1]['__type__'] = 'OpenData'
        parts[1]['__name__'] = parts[0]
        return parts[1]
    def typedvalue(self, parts):
        return {'__type__': parts[0], '__value__': parts[1]}
    def pair(self, parts):
        return tuple(parts)
    def list(self, parts):
        return list(parts)
    def dict(self, parts):
        return dict(parts)
    def ESCAPED_STRING(self, s):
        return s[1:-1]
    def SIGNED_FLOAT(self, i):
        return float(i)
    def SIGNED_INT(self, i):
        return int(i)
    def CNAME(self, s):
        return str(s)
    def varword(self, parts):
        return ''.join(parts)
    def varname(self, parts):
        return '.'.join(parts)

class OpenData:
    '''Class to represent `OpenData` file (e.g. `contents`, `layout`, etc.)'''
    def __init__(self, data):
        '''``Contents`` constructor'''
        if isfile(data):
            data = open(data).read()
        data = data.replace(u'\ufeff','').strip()
        tree = opendata_dict_parser.parse(data)
        self.opendata_dict = OpenDataTransformer().transform(tree)

    def __contains__(self, key):
        '''Implement `in` operator'''
        return key in self.opendata_dict

    def __getitem__(self, key):
        '''Implement the `[]` operator'''
        return self.opendata_dict[key]

    def get_dict(self):
        '''Get a `dict` representation of this `OpenData` object

        Returns:
            A `dict` representation of this `OpenData object
        '''
        return self.opendata_dict
