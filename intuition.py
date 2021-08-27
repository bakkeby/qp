import re
import logging
import matplotlib
from datetime import datetime
from options import Options

time_re = re.compile("^[0-9/:. -]{5,}$")
numb_re = re.compile("^[0-9.]+$")

log = logging.getLogger('qp')

class Intuition:

    def __init__(self, options: Options = None, **kwargs):
        self.options = options

    def deduce_delimiter_from_lines(self, lines):

        del_idx = 0
        delim_col_count = []
        delimiters = ['|', ',', ';', '=', ' ', ' ']

        has_header = False
        # TODO check for header
        if len(lines) > 1:
            has_header = (sum(c.isdigit() for c in lines[0]) < sum(c.isdigit() for c in lines[1]) and
                          sum(c.isalpha() for c in lines[0]) > sum(c.isalpha() for c in lines[1]))
            if (has_header):
                lines = lines[1:]

        for del_idx in range(len(delimiters)):
            delim_col_count.append([])
            delimiter = delimiters[del_idx]

            for line in lines:
                columns = line.split(delimiter)

                num_numb_col = 0
                num_time_col = 0
                num_othr_col = 0

                for col in columns:
                    if numb_re.match(col):
                        num_numb_col += 1
                    elif time_re.match(col):
                        num_time_col += 1
                    else:
                        num_othr_col += 1

                num_list = [num_numb_col, num_time_col, num_othr_col]

                if num_list not in delim_col_count[del_idx]:
                    delim_col_count[del_idx].append(num_list)

            del_idx += 1

        max_numb = 0
        delimiter = ' '

        for del_idx in range(len(delimiters)):
            num_lists = delim_col_count[del_idx]
            if len(num_lists) != 1:
                continue

            numb, time, othr = num_lists[0]

            if numb + time > max_numb:
                max_numb = numb + time
                delimiter = delimiters[del_idx]

        return delimiter

    def deduce_plot_columns_from_lines(self, lines, delimiter):

        rows = []
        for line in lines:
            if (line.isspace()):
                continue
            rows.append(line.split(delimiter))

        # Select the first time column found for the x column
        time_cols = []
        time_vals = []
        numb_cols = []
        numb_vals = []
        head_cols = []

        has_header = False
        header = []

        if len(rows) > 1:
            has_header = (sum(c.isdigit() for c in rows[0]) < sum(c.isdigit() for c in rows[1]) and
                          sum(c.isalpha() for c in rows[0]) > sum(c.isalpha() for c in rows[1]))
            if (has_header):
                header = rows[0]
                rows = rows[1:]

        # The number of columns is determined by the first row
        num_cols = len(rows[0])
        uneven_cols_warning_logged = False
        for c in range(num_cols):

            time_rows_matched = 0
            numb_rows_matched = 0
            col_unique_values = []
            col_all_values = []
            timefmt = self.options.get('timeformat')
            for row in rows:
                if c >= len(row):
                    if not uneven_cols_warning_logged:
                        log.warning('Uneven number of columns detected for line: ' + delimiter.join(row))
                        uneven_cols_warning_logged = True
                    continue

                col = row[c]

                if numb_re.match(col):
                    numb_rows_matched += 1
                    if col not in col_unique_values:
                        col_unique_values.append(col)
                    col_all_values.append(float(col))
                elif time_re.match(col):
                    time_rows_matched += 1
                    if not timefmt:
                        timefmt = self.deduce_input_time_format_from_time(col)
                        if not timefmt:
                            continue
                    # print(f"trying to parse '{col}' with timefmt of {timefmt}")
                    time = datetime.strptime(col, timefmt)
                    if time.year == 1900:
                        time = time.replace(year=datetime.now().year)
                    col_all_values.append(matplotlib.dates.date2num(time))

            if time_rows_matched == len(rows):
                time_cols.append(c)
                time_vals.append(col_all_values)
            # If the column contains numbers then expect at least 10% variation in the numbers listed
            # I.e. ignore columns having the same value
            elif numb_rows_matched == len(rows) and len(col_unique_values) > len(rows) * 10 / 100:
                numb_cols.append(c)
                numb_vals.append(col_all_values)
                if has_header:
                    head_cols.append(header[c])

        plot_columns = []
        if len(time_cols) > 0:
            for i in range(len(numb_cols)):
                plot_columns.append((time_vals[0], numb_vals[i], head_cols[i] if i < len(head_cols) else None))
        elif len(numb_cols) == 1:
            plot_columns.append((range(len(numb_cols)), numb_cols[0], head_cols[0] if len(head_cols) else None))
        else:
            for i in range(1, len(numb_cols)):
                plot_columns.append((numb_vals[0], numb_vals[i], head_cols[i] if i < len(head_cols) else None))

        return plot_columns

    def deduce_input_time_format_from_time(self, time):

        timefmt = self.options.get('timeformat', default=None)
        if (timefmt):
            try:
                datetime.strptime(time, timefmt)
                log.debug(f"time format, using passed timeformat of {timefmt}")
                return timefmt
            except ValueError:
                timefmt = None

        time_formats = {
            '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$': '%Y-%m-%d %H:%M:%S',
            '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}$': '%Y-%m-%d %H:%M',
            '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}$': '%Y-%m-%d %H',
            '^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}$': '%Y-%m-%d_%H',
            '^[0-9]{4}-[0-9]{2}-[0-9]{2}$': '%Y-%m-%d',
            '^[0-9]{4}-[0-9]{2}$': '%Y-%m',
            '^[0-9]{2}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}': '%m/%d/%y %H:%M:%S',
            '^[0-9]{2}/[0-9]{2}-[0-9]{2}:[0-9]{2}:[0-9]{2}[.][0-9]{3}$': '%m/%d-%H:%M:%S.%f',
            '^[0-9]{2}/[0-9]{2}-[0-9]{2}:[0-9]{2}:[0-9]{2}$': '%m/%d-%H:%M:%S',
            '^[0-9]{2}/[0-9]{2}-[0-9]{2}:[0-9]{2}$': '%m/%d-%H:%M',
            '^[0-9]{2}/[0-9]{2}-[0-9]{2}$': '%m/%d-%H',
            '^[0-9]{2}/[0-9]{2}$': '%m/%d',
            '^[0-9]{2}:[0-9]{2}:[0-9]{2}$': '%H:%M:%S',
            '^[0-9]{2}:[0-9]{2}$': '%H:%M',
            '^[0-9]{8}_[0-9]{2}$': '%Y%m%d_%',
        }

        for regexp in time_formats:
            tfmt_re = re.compile(regexp)
            if tfmt_re.match(time):
                timefmt = time_formats[regexp]
                break
        log.debug(f"time format, using deduced timeformat of {timefmt}")
        return timefmt
