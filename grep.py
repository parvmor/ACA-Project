#!/usr/bin/python2

import os
import re
import sys
import argparse

errors=[]

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-r','--recursive',action='store_true',help="recurse into directories and follow symbolic links if necessary")
#implementing of symbolic links will be done later
    parser.add_argument('-o','--onlyMatching',action='store_true',help="print only the matched parts of a matching line")
    parser.add_argument('-i','--ignoreCase',action='store_true',help="perform case-insensitive matching")
    parser.add_argument('pattern',nargs=1,help="Pattern to be searched")
    parser.add_argument('destinations',nargs='*',help="File/s or Directorie/s to be searched")
    args=parser.parse_args()
    return args

def printMatch(pattern,line,onlyMatching):
    if onlyMatching:
        for match in pattern.findall(line):
            print("\033[91m{}\033[00m".format(match))
    else:
        out=""
        ind=0
        for it in pattern.finditer(line):
            out += line[ind:it.start()]
            out += "\033[91m{}\033[00m".format(line[it.start():it.end()])
            ind=it.end()
        out+=line[it.end():(len(line)-1)]
        print out   
    return

def grep(pattern,destination):
    if os.path.isfile(destination):
        try:
            with open(destination,'r') as currFile:
                for line in currFile:
                    if pattern.search(line):
                        yield line
        except (OSError,IOError) as error:
            errors.append(str(error))
            pass
    else:
        for content in os.listdir(destination):
            newPath=os.path.join(destination,content)
            for line in grep(pattern,newPath):
                yield line

def grep_util(args):
    if args.ignoreCase:
        args.pattern[0]=re.compile(args.pattern[0],re.IGNORECASE)
    else:
        args.pattern[0]=re.compile(args.pattern[0])
    for destination in args.destinations:
        if not os.path.exists(destination):
            errors.append("File/Directory '" + destination + "' does not exists.")            
        elif (not args.recursive) and (os.path.isdir(destination)):
            errors.append("The given path '" + destination + "' is a directory. Please use recursive flag.")
        else:
            for line in grep(args.pattern[0],destination):
                printMatch(args.pattern[0],line,args.onlyMatching)
    if not sys.stdin.isatty():
        for line in sys.stdin:
            if args.pattern[0].search(line):
                printMatch(args.pattern[0],line,args.onlyMatching)
    return


def main():
    args=parse_args()
    grep_util(args)
    for error in errors:
        print '\x1b[0;37;41m' + 'ERROR:' + '\x1b[0m' + ' ' + error
    return

if __name__ == '__main__':
    main()
