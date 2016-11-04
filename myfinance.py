#!/usr/bin/env python3

import sys

from cmdparser import ParseInput

if __name__ == '__main__':
    parse_input = ParseInput()
    ParseInput.usage()
    parse_input.main(sys.argv[1:])
