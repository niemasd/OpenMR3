#!/usr/bin/env python3
'''
Convert `OpenData` file to JSON
Niema Moshiri 2021
'''
from json import dump as jdump
from OpenMR3 import OpenData
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input OpenData File")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output JSON File")
    args = parser.parse_args()
    if args.input.lower() == 'stdin':
        from sys import stdin
        opendata = OpenData(stdin.read())
    else:
        opendata = OpenData(args.input)
    if args.output.lower() == 'stdout':
        from sys import stdout as out
    else:
        out = open(args.output,'w')
    try:
        jdump(opendata.get_dict(), out)
    except Exception as e:
        print("FAILED TO SERIALIZE TO JSON:\n%s\n" % str(opendata.get_dict())); raise e
    if args.output.lower() == 'stdout':
        print()
    out.close()
