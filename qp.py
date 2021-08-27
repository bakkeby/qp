#!/usr/bin/env python3
# coding=UTF8
# APPTAG|python|qp.py|A plot helper to generate quick graphs from data files
# Copyright (c) 2021, Stein Gunnar Bakkeby, all rights reserved.

import logging
import sys

from filereader import FileReader
from options import Options
from args import Arguments
from intuition import Intuition
from plotter import Plotter

def main():
    """
This is a helper tool intended as a quick and easy way to get some visual representation of
data extracted from log files or otherwise.

The general idea here is that the tool should be intelligent enough to:
   - work out what the data delimiter is
   - to differentiate between time and data columns and
   - to detect which format the time is in

This avoids, for the most part, having the user waste time explaining to the tool how the
data is formatted (or having to reformat the data in a certain way).

example commands:
   - qp.py stats.dat
   - qp.py counts.csv -o number.png --title "Embrace for impact"
"""
    options = Options(parser=Arguments.parser(main.__doc__))
    options.load_params(Arguments)
    options.parse_args()
    cfg_file = options.get('cfg_file', default=str.replace(__file__, '.py', '.cfg'))
    options.load_config(cfg_file)

    log = logging.getLogger('qp')
    log.handlers = []
    handler = logging.StreamHandler(sys.stderr)
    frmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(frmt)
    log.addHandler(handler)
    if options.get('debug', default=False):
        log.setLevel(logging.DEBUG)

    fileReader = FileReader(options)
    intuition = Intuition(options)
    plotter = Plotter(options)

    outfile = options.get('outfile')
    extargs = options.get('remaining_args')
    filename = None
    lines = None

    if not sys.stdin.isatty():
        log.debug('Standard in detected')
        lines = [line.rstrip('\n') for line in sys.stdin.readlines()]
        outfile = "qp.png"
    elif extargs:
        filename = extargs[0]
        log.info(f"Reading file {filename}")
        lines = fileReader.read_file_as_lines(filename)

    if not lines:
        options.print_help()
        exit(0)

    if not outfile:
        outfile = filename + '.png'

    delimiter = options.get('delimiter')
    if not delimiter:
        delimiter = intuition.deduce_delimiter_from_lines(lines)
    cols = intuition.deduce_plot_columns_from_lines(lines, delimiter)
    plotter.plot(lines, delimiter, cols)
    plotter.save_plot(outfile)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt):
        print("\nExiting...\n")
