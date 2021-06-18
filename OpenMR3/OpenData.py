#!/usr/bin/env python3
'''
Functions and classes for handling `OpenData` files (e.g. `contents`, `layout`, etc.)
Niema Moshiri 2021
'''
from lark import Lark, Transformer
from os.path import isfile

opendata_dict_parser = Lark(r'''
    ?value : opendata
           | lengthproperty
           | stringproperty
           | weightproperty
           | varname
           | dict
           | list
           | ESCAPED_STRING
           | SIGNED_INT
           | SIGNED_FLOAT

    // OpenData-specific types
    opendata : "OPENDATA" varname dict ";"
    lengthproperty : "LengthProperty" dict
    stringproperty : "StringProperty" dict
    weightproperty : "WeightProperty" dict

    varword : ["@"] CNAME | "T" ESCAPED_STRING
    varname : varword [("." varword)*] ["PxStream"]

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
    def lengthproperty(self, parts):
        parts[0]['__type'] = 'LengthProperty'
        return parts[0]
    def stringproperty(self, parts):
        parts[0]['__type__'] = 'StringProperty'
        return parts[0]
    def weightproperty(self, parts):
        parts[0]['__type__'] = 'WeightProperty'
        return parts[0]
    def pair(self, parts):
        return tuple(parts)
    def list(self, parts):
        return list(parts)
    def dict(self, parts):
        return dict(parts)
    def ESCAPED_STRING(self, s):
        return s[1:-1]
    def SIGNED_INT(self, i):
        return int(i)
    def CNAME(self, s):
        return str(s)
    def varword(self, parts):
        return ''.join(parts)
    def varname(self, parts):
        if len(parts) != 1:
            raise ValueError("MULTIPLE PARTS!!!")
        return ''.join(parts)
    def opendata(self, parts):
        parts[1]['__type__'] = 'OpenData'
        parts[1]['__name__'] = parts[0]
        return parts[1]

class OpenData:
    '''Class to represent `OpenData` file (e.g. `contents`, `layout`, etc.)'''
    def __init__(self, data):
        '''``Contents`` constructor'''
        if isfile(data):
            data = open(data).read()
        data = data.replace(u'\ufeff','').strip()
        tree = opendata_dict_parser.parse(data)
        self.opendata_dict = OpenDataTransformer().transform(tree)
