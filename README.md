`qp` (quick plot) is a helper tool intended as a quick and easy way to get some visual
representation of data extracted from log files or otherwise.

The tool takes advantage of the rather powerful [matplotlib](https://matplotlib.org/) library for
python to create graphs. `qp` is an evolution of a similar
[gnuplot wrapper script](https://bitbucket.org/bakkeby/plot/src/master/) that I used in the past.

The tool can be considered as being in alpha state.

The general idea here is that the tool should be intelligent enough to:
   - work out what the data delimiter is
   - to differentiate between time and data columns and
   - to detect which format the time is in

This avoids, for the most part, having the user waste time explaining to the tool how the
data is formatted (or having to reformat the data in a certain way).

example commands:
   - ```qp.py stats.dat```
   - ```qp.py counts.csv -o number.png --title "Embrace for impact"```

### Requirements

   - python 3.x
   - argparse
   - matplotlib

Install the required libraries using:

```sh
$ pip install -r requirements.txt
```

Note that it is generally recommended to use virtual environments to store and load program specific
dependencies like this.
