from unittest import TestCase
from cStringIO import StringIO
import pytest
import sys

from weeker.weeker_class import Weeker

class Trapper(list):

    _out = None
    _err = None
    _buf = None

    def __enter__(self):
        # save system pipes and create new buffer
        self._out = sys.stdout
        self._err = sys.stderr

        sys.stdout = self._buf = StringIO()
        sys.stderr = self._buf
        return self

    def __exit__(self, *args):
        # Reinstate system pipes and tidy up
        self.extend(self._buf.getvalue().splitlines())
        del self._buf
        sys.stdout = self._out
        sys.stderr = self._err

    def report(self):
        for l in self:
            print l

class TestWeeker(TestCase):
    
    def test_weeker(self):
        print

        # store the command-line arguments
        store = list(sys.argv)
        
        del sys.argv[1:]
        sys.argv.extend(['tests/data/example.csv'])        
        print sys.argv

        with Trapper() as trap:
            Weeker().run_it()

        trap.report()

        checks = ['Ingested 29 lines',
                  'Number of days: 28',
                  '\'Sunrise\', \'Noon\', \'Sunset\'',
                  '\'12\', \'Sun\', \'6:46 am\'',
                  '\'28\', \'Tue\', \'7:03 am\'']
        found = [c for c in checks for t in trap if c in t]

        assert set(found) == set(checks)

        # restore program args
        sys.argv = list(store)
