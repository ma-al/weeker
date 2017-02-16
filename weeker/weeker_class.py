"""
Weeker module.

Main class converts a tabbed CSV into week-separated representation, with the
option to output to plain-text files.
"""

import os
import calendar
import argparse


class Weeker(object):
    """
    Main Weeker class.

    Converts a tabbed CSV into a list of lists. The lists are organised
    according to weeks, with each week being from Monday to Sunday.
    """

    _out_dir = './output'
    sect = lambda self, msg: '\n{:=>80}'.format(' [ {} ]'.format(msg))

    def __init__(self):
        """Initialize class via parsed program arguments."""
        self._month = 0
        self._etype = []
        self._data = []
        self._row_head = None

        self.parse_arguments()
        print
        for key, val in vars(self._args).iteritems():
            print '{:>6} : {}'.format(key, val)

    def parse_arguments(self):
        """Get and parse the program arguments."""
        pars = argparse.ArgumentParser()
        pars.add_argument(
            '-s',
            '--save',
            action='store_true',
            help='Save all output to files')
        pars.add_argument(
            'csv',
            metavar='input_csv',
            type=argparse.FileType('r'),
            help='The tabbed CSV file you want converted')

        self._args = pars.parse_args()

    def get_meta(self):
        """Extract metadata from the read file."""
        month = self._row_head[0]
        month_lst = list(calendar.month_name)

        if month not in month_lst:
            raise RuntimeError('Weird month! ({})'.format(month))

        self._month = month_lst.index(month)
        self._etype = self._row_head[2:]

        if len(self._etype) != 6:
            raise RuntimeError('Wrong headers! ({})'.format(self._etype))

        print calendar.month_name[self._month]
        print calendar.month_abbr[self._month]
        print self._etype

    def stringify_day(self, day):
        """
        Format the given day.

        E.g., Changes ['01', 'Wed', '06:32 AM', '12:00 PM', '08:35 PM'] into
        ---------- Wed, Feb 01
        Sunrise 06:32 AM
           Noon 12:00 PM
         Sunset 08:35 PM

        :param list day: Day data as a list of strings
        :return: Formatted newline-separated string
        :rtype: str
        """
        time = lambda t: t.rjust(8, '0').upper()
        event = lambda e: e.rjust(7, ' ')
        fmt = lambda e, t: event(e) + ' ' + time(t)

        out = [fmt(self._etype[i], v) for i, v in enumerate(day[2:])]

        date = str(day[0]).rjust(2, '0')
        dayw = day[1]
        abbr = calendar.month_abbr[self._month]
        separator = ' {}, {} {}'.format(dayw, abbr, date).rjust(24, '-')

        out.insert(0, separator)
        return '\n'.join(out)

    def week_to_file(self, fpath, week, reverse=True):
        """
        Write a whole week of data into a file.

        :param str fpath: File path to save to
        :param list week: List of day data for the week
        :param bool reverse: True if you want to reverse the order of days
        """
        if reverse:
            # reverse order of days in week
            week.reverse()

        with open(fpath, 'w') as open_file:
            open_file.write('```\n')
            for day in week:
                day_str = self.stringify_day(day)
                open_file.write(day_str + '\n')
            open_file.write('```\n')

    def data_to_files(self):
        """Write all data to week-separated files."""
        weeks = self._data
        month = self._month
        mabbr = calendar.month_abbr[self._month].lower()

        for idx, week in enumerate(weeks):
            fname = '{}-{}-{}.txt'.format(month, mabbr, idx)
            fpath = os.path.join(self._out_dir, fname)
            self.week_to_file(fpath, week)
            print 'Saved', fpath

    def partition_data(self):
        """Reorganise the raw data into individual weeks."""
        weeks = []
        week = []

        for line in self._data:
            day = line[1]
            if day == calendar.day_abbr[calendar.MONDAY]:
                weeks.append(week)
                week = []

            week.append(line)

        if len(week) > 0:
            weeks.append(week)

        self._data = weeks

    def show_partitions(self):
        """Output to console the partitioned data."""
        for week in self._data:
            print
            for day in week:
                print day

    def check_data(self):
        """Basic sanity check of the data."""
        data = self._data
        if len(data) is 0:
            raise RuntimeError('Data is empty')

        # first item of first list should be the month
        month = data[0][0]
        if month not in calendar.month_name:
            raise RuntimeError('Can\'t detect the month')

        print 'Month: {}'.format(month)
        print 'Number of days: {}'.format(len(data) - 1)

    def ingestion(self, open_file):
        """Read raw data from the tabbed CSV."""
        self._data = []
        for line in open_file:
            # get rid of newline and intertabs
            toks = line.rstrip().split('\t')

            # needs 9 items in list
            if len(toks) is not 9:
                print 'Discarded ({}). Too short.'.format(toks)
                continue

            # get rid of 2nd item
            toks.pop(1)
            self._data.append(toks)

    def show_data(self):
        """Output to console the ."""
        for data in self._data:
            print data, len(data), type(data)

    def run_it(self):
        """Do an complete run."""
        args = self._args

        print self.sect('Ingestion')
        self.ingestion(args.csv)
        print 'Input File: {}'.format(args.csv.name)
        print 'Ingested {} lines'.format(len(self._data))
        args.csv.close()

        print self.sect('Checking')
        self.check_data()

        print self.sect('Extracting Metadata')
        self._row_head = self._data.pop(0)
        self.get_meta()

        print self.sect('Partitioning')
        self.partition_data()
        self.show_partitions()

        if not args.save:
            return

        print self.sect('Saving To File')
        self.data_to_files()


if __name__ == '__main__':
    Weeker().run_it()
