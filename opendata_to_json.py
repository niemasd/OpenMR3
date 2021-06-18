#!/usr/bin/env python3
'''
Convert `OpenData` file to JSON
Niema Moshiri 2021
'''
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
    # TODO CONVERT TO JSON
