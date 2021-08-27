import logging
import matplotlib.pyplot as plt
import matplotlib
from options import Options

log = logging.getLogger('qp')

# For plot style, color and marker symbols refer to the format strings section under:
# https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html

linestylemap = {
    '': '-',
    'solid': '-',
    'dashed': '--',
    'dashdot': '-.',
    'dotted': ':',
}

linecolormap = {
    '': '',
    'blue': 'b',
    'green': 'g',
    'red': 'r',
    'cyan': 'c',
    'magenta': 'm',
    'yellow': 'y',
    'black': 'k',
    'white': 'w'
}

class Plotter:

    def __init__(self, options: Options = None, **kwargs):
        self.options = options
        pass

    def plot(self, lines: [str], delimiter, cols):

        fig, axs = plt.subplots()

        fmt = "{}{}{}".format(
            self.options.get('linemarker'),
            linestylemap[self.options.get('linestyle')],
            linecolormap[self.options.get('linecolor') if len(cols) == 1 else ''],
        )

        labels = self.options.get('labels')

        for c, (x, y, label) in enumerate(cols):
            if not label:
                label = labels[c] if c < len(labels) else str(y[0])
            axs.plot(x, y, fmt, label=label)

        axs.set_xlabel(self.options.get('xlabel'))
        axs.set_ylabel(self.options.get('ylabel'))
        axs.set_title(self.options.get('title'))
        axs.grid(self.options.get('gridlines', default=False))

        fmt = matplotlib.dates.DateFormatter('%Y-%m-%d')
        axs.xaxis.set_major_formatter(fmt)
        plt.xticks(rotation=self.options.get('xticksrotation'))
        plt.legend()

        fig.tight_layout()

    def save_plot(self, outfile):
        frmt = outfile.split('.')[-1].lower()
        frmt_supported = plt.gcf().canvas.get_supported_filetypes().keys()
        if frmt not in frmt_supported:
            if frmt != outfile:
                log.warning(f"Unsupported file format of {frmt}, defaulting to \"png\".")
                log.warning("Supported formats:")
                log.warning("\t{}".format(", ".join(frmt_supported)))
            outfile += '.png'
            frmt = 'png'

        plt.savefig(outfile, format=frmt)
        log.info(f"Wrote {outfile}")
