#!/usr/bin/env python2

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

def printMatch(pattern,line,onlyMatching,path=""):
    if onlyMatching:
        for match in pattern.findall(line):
            out="\033[91m{}\033[00m".format(match)
            if path is "":
                print(out)
            else:
                print("\033[95m{}\033[00m".format(path) + "\033[94m{}\033[00m".format(":") + out)
    else:
        out=""
        ind=0
        for it in pattern.finditer(line):
            out += line[ind:it.start()]
            out += "\033[91m{}\033[00m".format(line[it.start():it.end()])
            ind=it.end()
        out+=line[it.end():(len(line)-1)]
        if path is not "":
            print("\033[95m{}\033[00m".format(path) + "\033[94m{}\033[00m".format(":") + out)
        else:
            print out   
    return

def grep(pattern,destination):
    if os.path.isfile(destination):
        if b'\x00' in open(destination,'r').read():
            errors.append("The file '" + destination + "' is binary.")
        else:
            try:
                with open(destination,'r') as currFile:
                    for line in currFile:
                        if pattern.search(line):
                            yield (destination,line)
            except (OSError,IOError) as error:
                errors.append(str(error))
                pass
    else:
        for content in os.listdir(destination):
            newPath=os.path.join(destination,content)
            for (path,line) in grep(pattern,newPath):
                yield (path,line)

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
            for (path,line) in grep(args.pattern[0],destination):
                printMatch(args.pattern[0],line,args.onlyMatching,path)
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
