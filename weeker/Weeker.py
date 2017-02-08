import os
import json
import datetime
import calendar
import argparse

section = lambda msg : '\n{:=>80}'.format(' [ {} ]'.format(msg))

class Weeker:
    """
    Converts a "CSV" that is tabbed into list of lists
    """
    csv = None
    data = []
    row_head = None

    stype = []
    month = 0
    month_name = None
    month_abbr = None

    _out_dir = './output'

    def show_args(self, args):
        print
        for key, val in vars(args).iteritems():
            print '{:>6} : {}'.format(key, val) 

    def __init__(self):
        self._args = self.get_args()
        self.show_args(self._args)
 
    def get_args(self):
        pars = argparse.ArgumentParser()

        pars.add_argument('-s', '--save', action='store_true', 
                          help='Save all output to files')
        pars.add_argument('csv', metavar='input_csv',
                          type=argparse.FileType('r'),
                          help='The tabbed CSV file you want converted')

        return pars.parse_args()

    def get_meta(self):
        m = self.row_head[0]
        lm = list(calendar.month_name)
       
        if m not in lm:
            raise RuntimeError('Weird month! ({})'.format(m))

        self.month = lm.index(m)
        self.stype = self.row_head[2:]

        if len(self.stype) != 6:
            raise RuntimeError('Wrong headers! ({})'.format(self.stype))

        self.month_name = calendar.month_name[self.month]
        self.month_abbr = calendar.month_abbr[self.month]
        
        print self.month_name
        print self.month_abbr
        print self.stype

    def time_as_string(self, key, val):
        return '{} {}'.format(key.rjust(7, ' '), str(val).rjust(2, '0'))
    
    def stringify_day(self, day):
        s = []
        
        date = str(day[0]).rjust(2, '0')
        dayw = day[1]

        right = ' {}, {} {}'.format(dayw, self.month_abbr, date)
        right = right.rjust(24, '-')
        s.append(right)

        for idx, val in enumerate(day[2:]):
            s.append(self.time_as_string(self.stype[idx], val))

        return '\n'.join(s)

    def week_to_file(self, fn, week, reverse=True):
        #reverse order of days in week
        if reverse:
            week.reverse()
        
        with open(fn, 'w') as f:
            f.write('```\n')
            for day in week:
                s = self.stringify_day(day)
                f.write(s + '\n')
            f.write('```\n')

    def data_to_files(self):
        weeks = self.data

        for idx, week in enumerate(weeks):
            fn = '{}-{}-{}.txt'.format(self.month, 
                                       self.month_abbr.lower(),
                                       idx)
            file_path = os.path.join(self._out_dir, fn)
            self.week_to_file(file_path, week)
            print 'Saved', file_path

    def partition_data(self):
        weeks = []
        week = []

        for line in self.data:
            day = line[1]
            if day == calendar.day_abbr[calendar.MONDAY]:
                weeks.append(week)
                week = []
            
            week.append(line)

        if len(week) > 0:
            weeks.append(week)
 
        self.data = weeks

    def show_partitions(self):
        for week in self.data:
            print
            for day in week:
                print day
    
    def check_data(self):
        data = self.data
        if len(data) is 0:
            raise RuntimeError('Data is empty')

        # first item of first list should be the month
        month = data[0][0]
        if month not in calendar.month_name:
            raise RuntimeError('Can\'t detect the month')
        
        print 'Month: {}'.format(month)
        print 'Number of days: {}'.format(len(data) - 1)

    def ingestion(self, open_file):
        data = []
        for line in open_file:
            # get rid of newline and intertabs
            toks = line.rstrip().split('\t')

            # needs 9 items in list
            if len(toks) is not 9:
                print 'Discarded ({}). Too short.'.format(toks)
                continue

            # get rid of 2nd item
            toks.pop(1)
            data.append(toks)

        return data

    def show_data(self):
        for d in self.data:
            print d, len(d), type(d)

    def run_it(self):
        args = self._args

        print section('Ingestion')
        print 'Input File: {}'.format(args.csv.name)
        self.data = self.ingestion(args.csv)
        print 'Ingested {} lines'.format(len(self.data))
        args.csv.close()

        print section('Checking')
        self.check_data()
        
        print section('Extracting Metadata')
        self.row_head = self.data.pop(0)
        self.get_meta()
       
        print section('Partitioning')
        self.partition_data()
        self.show_partitions()

        if args.save:
            print section('Saving To File')
            self.data_to_files()


if __name__=='__main__':
    Weeker().run_it()
