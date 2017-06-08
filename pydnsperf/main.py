#!/usr/bin/env python2.7

import argparse
from dns import work_loop
from options import Options, set_options, prepare_args
import os
from sys import argv


def main():
    parser = argparse.ArgumentParser()
    prepare_args(parser)
    args = parser.parse_args()
    set_options(Options(args))
    print(args)

    if os.geteuid() != 0:
        print("Error: {0} requires root privileges.".format(argv[0]))
        exit()

    print("Starting up")
    work_loop()


if __name__ == '__main__':
    main()
