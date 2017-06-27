# coding:utf-8

from thread import Threads
import sys

def main():

    argvs = sys.argv
    argc = len(argvs)

    if argc >= 2:
        inputname = ""
        outname = ""
        url = ""

        i = 1
        while i < argc:
            if argvs[i] == "-i":
                inputname = argvs[i + 1]
                i = i + 1
            elif argvs[i] == "-o":
                outname = argvs[i + 1]
                i = i + 1
            elif argvs[i] == "-url":
                url = argvs[i + 1]
                i = i + 1
            
            i = i + 1

        if inputname == "":
            print("Please input InputFilename fullpath with -i and whitespace")
            exit()
        if outname == "":
            print("Please input OutFilename fullpath with -o and whitespace")
            exit()
        if url == "":
            print("Please input URL with -url and whitespace")
            exit()

        thread = Threads()

        thread.download(inputname, url)
        thread.DatToHTML(inputname, outname)
    else:
        print("Not Args")
        exit()

if __name__ == '__main__':
    main()