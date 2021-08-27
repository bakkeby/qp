import argparse
import random
import sys

show_more_args = '--more' in sys.argv

tips = [
    'Tip: Did you know that you can customise your default settings in qp.cfg?',
    'Warning! Plotting to outplot the plot of fellow plotters will only result in counterplot.',
    'Tip: Did you know that this script supports input from standard in? You can just pipe data to it.'
]

class Arguments:

    @staticmethod
    def parser(description):
        parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=random.choice(tips)
        )
        return parser

    @staticmethod
    def param_setup(parser, show_more_args=True):

        parser.add_argument(
            "--more",
            default=False,
            dest='show_more_args',
            help=argparse.SUPPRESS if show_more_args else "show advanced options",
            action="store_true"
        )

        parser.add_argument(
            "--debug",
            default=False,
            dest='debug',
            help="enable debug logging" if show_more_args else argparse.SUPPRESS,
            action="store_true"
        )

        parser.add_argument(
            "-tf", "--timeformat",
            default=None,
            dest='timeformat',
            metavar="<format>",
            help="specify the time format being used in the input file" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "-t", "--title",
            default=None,
            dest='title',
            metavar="<title>",
            help="specify the title of the generated graph" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "-ls", "--linestyle",
            default=None,
            choices=['solid', 'dashed', 'dashdot', 'dotted'],
            dest='linestyle',
            metavar='<style>',
            help="the line style used for the graph, one of solid (default), dashed, dashdot or dotted" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "-lc", "--linecolor",
            default=None,
            choices=['', 'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white'],
            dest='linecolor',
            metavar='<color>',
            help="the line color used for single column graphs, one of blue, green, red, cyan, magenta, yellow, black or white" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "-lm", "--linemarker",
            default=None,
            choices=['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_'],
            dest='linemarker',
            metavar='<marker>',
            help="the line marker used for the graph, one of: . , o v ^ < > 1 2 3 4 8 s p P * h H + x X D d | _" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "-l", "--label",
            default=None,
            dest='labels',
            metavar='<label>',
            help="the label(s) used for the legend" if show_more_args else argparse.SUPPRESS,
            action="append",
        )

        parser.add_argument(
            "-o", "--output",
            default=None,
            dest='outfile',
            metavar="<filename>",
            help="name of the output file to store the plotted graph (defaults to <input>.png)" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "-d", "--delimiter",
            default=None,
            dest='delimiter',
            metavar="<sep>",
            help="the delimiter that separates columns in the input file, if not specified the script will attempt to deduce it based on the file contents" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "--xlabel",
            default=None,
            dest='xlabel',
            metavar="<string>",
            help="set the x-label (defaults to not being set)" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "--ylabel",
            default=None,
            dest='ylabel',
            metavar="<string>",
            help="set the y-label (defaults to not being set)" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "--grid",
            default=None,
            dest='gridlines',
            help="include gridlines in the graph" if show_more_args else argparse.SUPPRESS,
            action='store_true'
        )

        parser.add_argument(
            "--xticksrotation",
            default=None,
            type=int,
            dest='xticksrotation',
            help="rotation of date listings in the graph (defaults to 45)" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "-c", "--config",
            default=None,
            type=str,
            dest='cfg_file',
            metavar="<file>",
            help="specify the configuration file to use, defaults to qp.cfg" if show_more_args else argparse.SUPPRESS,
        )

        parser.add_argument(
            "remaining_args",
            nargs='*',
            help=argparse.SUPPRESS
        )
