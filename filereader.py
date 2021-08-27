#!/usr/bin/env python3
# coding=UTF8

from options import Options

class FileReader:

    def __init__(self, options: Options = None, **kwargs):
        pass

    def read_file_as_lines(self, filename):
        lines = []
        with open(filename, 'r') as f:
            lines = f.read().splitlines()

        return lines
