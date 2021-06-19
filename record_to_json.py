#!/usr/bin/env python3
'''
Convert `Record` folder to JSON
Niema Moshiri 2021
'''
from json import dump as jdump
from OpenMR3 import Record
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=str, help="Input Record Folder")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output JSON File")
    args = parser.parse_args()
    record = Record(args.input)
    if args.output.lower() == 'stdout':
        from sys import stdout as out
    else:
        out = open(args.output,'w')
    jdump(record.get_dict(), out)
    if args.output.lower() == 'stdout':
        print()
    out.close()
