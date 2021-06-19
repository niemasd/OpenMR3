#!/usr/bin/env python3
'''
Functions and classes for handling `OpenData` files (e.g. `contents`, `layout`, etc.)
Niema Moshiri 2021
'''
from lark import Lark, Transformer
from os.path import isfile

opendata_dict_parser = Lark(r'''
    ?value : opendata
           | analogchannel
           | analogsignal
           | int16analogarchive
           | lengthproperty
           | motionsignalreal64
           | personboneset
           | pxstream
           | skeletonclip
           | skeletonclipcalibration
           | skeletoncliplandmark
           | skeletonclipsegment
           | stringproperty
           | timerecordmovement
           | videochannel
           | videodata
           | weightproperty
           | varname
           | dict
           | list
           | ESCAPED_STRING
           | SIGNED_INT
           | SIGNED_FLOAT

    // OpenData-specific types
    opendata                : "OPENDATA" varname dict ";"
    analogchannel           : "AnalogChannel" dict
    analogsignal            : "Analog_signal" dict
    int16analogarchive      : "Int16AnalogArchive" dict
    lengthproperty          : "LengthProperty" dict
    motionsignalreal64      : "Motion_signal_real64" dict
    personboneset           : "Person.Bone_set" dict
    pxstream                : "PxStream" ESCAPED_STRING
    skeletonclip            : "Skeleton.Clip" dict
    skeletonclipcalibration : "Skeleton.Clip.Calibration" dict
    skeletoncliplandmark    : "Skeleton.Clip.Landmark" dict
    skeletonclipsegment     : "Skeleton.Clip.Segment" dict
    stringproperty          : "StringProperty" dict
    timerecordmovement      : "TimeRecord.Movement" dict
    videochannel            : "Video.Channel" value
    videodata               : "Video.Data" value
    weightproperty          : "WeightProperty" dict

    varword : ["@"] CNAME | "T" ESCAPED_STRING
    varname : varword [("." varword)*]

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
    def analogchannel(self, parts):
        parts[0]['__type__'] = 'AnalogChannel'
        return parts[0]
    def analogsignal(self, parts):
        parts[0]['__type__'] = 'Analog_signal'
        return parts[0]
    def int16analogarchive(self, parts):
        parts[0]['__type__'] = 'Int16AnalogArchive'
        return parts[0]
    def lengthproperty(self, parts):
        parts[0]['__type__'] = 'LengthProperty'
        return parts[0]
    def motionsignalreal64(self, parts):
        parts[0]['__type__'] = 'Motion_signal_real64'
        return parts[0]
    def personboneset(self, parts):
        parts[0]['__type__'] = 'Person.Bone_set'
        return parts[0]
    def pxstream(self, parts):
        if len(parts) != 1:
            raise ValueError("Invalid PxStream")
        return {'__type__': 'PxStream', 'value': parts[0]}
    def skeletonclip(self, parts):
        parts[0]['__type__'] = 'Skeleton.Clip'
        return parts[0]
    def skeletonclipcalibration(self, parts):
        parts[0]['__type__'] = 'Skeleton.Clip.Calibration'
        return parts[0]
    def skeletoncliplandmark(self, parts):
        parts[0]['__type__'] = 'Skeleton.Clip.Landmark'
        return parts[0]
    def skeletonclipsegment(self, parts):
        parts[0]['__type__'] = 'Skeleton.Clip.Segment'
        return parts[0]
    def stringproperty(self, parts):
        parts[0]['__type__'] = 'StringProperty'
        return parts[0]
    def timerecordmovement(self, parts):
        parts[0]['__type__'] = 'TimeRecord.Movement'
        return parts[0]
    def videochannel(self, parts):
        parts[0]['__type__'] = 'Video.Channel'
        return parts[0]
    def videodata(self, parts):
        parts[0]['__type__'] = 'Video.Data'
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

    def get_dict(self):
        '''Get a `dict` representation of this `OpenData` object

        Returns:
            A `dict` representation of this `OpenData object
        '''
        return self.opendata_dict
