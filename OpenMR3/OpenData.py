#!/usr/bin/env python3
'''
Functions and classes for handling `OpenData` files (e.g. `contents`, `layout`, etc.)
Niema Moshiri 2021
'''
from lark import Lark
from os.path import isfile

opendata_dict_parser = Lark(r'''
    ?value : opendata
           | varname
           | dict
           | list
           | ESCAPED_STRING
           | SIGNED_INT
           | SIGNED_FLOAT

    opendata : "OPENDATA" varname dict ";"

    varword : ["@"] CNAME | "T" ESCAPED_STRING
    varname : varword [("." varword)*] ["PxStream"]

    dict : "[" [pair ";" (pair ";")*] "]"
    pair : varname ":" [varname] value

    // not sure about lists, because the sample data only has () aka empty
    list : "(" [value ";" (value ";")*] ")"

    %import common.CNAME
    %import common.ESCAPED_STRING
    %import common.SIGNED_FLOAT
    %import common.SIGNED_INT
    %import common.WS
    %ignore WS
    ''', start='opendata')

class OpenData:
    '''Class to represent `OpenData` file (e.g. `contents`, `layout`, etc.)'''
    def __init__(self, data):
        '''``Contents`` constructor'''
        if isfile(data):
            data = open(data).read()
        data = data.replace(u'\ufeff','').strip()
        #print(data)
        self.tree = opendata_dict_parser.parse(data)
        print(self.tree)
