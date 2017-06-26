# coding:utf-8

from thread import Threads
import sys

def main():

    argvs = sys.argv
    argc = len(argvs)

    thread = Threads()

    filename = thread.ReturnFileName()

    if argc >= 2:
        url = argvs[1]
        thread.download(filename, url)
        thread.DatToHTML(filename)
    else:
        print("Not Args")
        exit()

if __name__ == '__main__':
    main()