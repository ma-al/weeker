import os
import json
import datetime
import calendar


class TabbedConvert:
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


    def __init__(self, file_name):
        
        self.csv = os.path.abspath(file_name)
        print 'Input File: {}'.format(self.csv)

        print
        print 'Ingesting...'
        with open(self.csv, 'r') as f:
            for l in f:
                self.clean_line(l)

        print
        print 'Checking...'
        self.check_data()
        
        print
        print 'Extract Meta...'
        self.row_head = self.data.pop(0)
        self.get_meta()
       
        print
        print 'Partitioning...'
        self.partition_data()
        
        print
        print 'Printing...'
        self.data_to_files()

        #self.show_data()
    
    
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
            fn = './{}-{}-{}.txt'.format(
                self.month, self.month_abbr.lower(), idx)
            self.week_to_file(fn, week)
            print 'Saved ({})'.format(fn)


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
        
        for w in weeks:
            print
            for d in w:
                print d
        
        self.data = weeks


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


    def clean_line(self, l):
        # get rid of newline and intertabs
        l = l.rstrip()
        lst = l.split('\t')

        # needs 9 items in list
        if len(lst) is not 9:
            print 'Discarded ({}). Too short.'.format(lst)
            return

        # get rid of 2nd item
        lst.pop(1)
        
        # save it
        self.data.append(lst)


    def show_data(self):
        for d in self.data:
            print d, len(d), type(d)





if __name__=='__main__':

    print
    tc = TabbedConvert('./csv/2017-01.csv')
    #tc.show_data()




