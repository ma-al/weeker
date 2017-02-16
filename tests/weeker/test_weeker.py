from unittest import TestCase
import pytest
import sys

from weeker.weeker_class import Weeker


class TestWeeker(TestCase):
    
    def test_weeker(self):
        print

        # store the command-line arguments
        store = list(sys.argv)
        
        del sys.argv[1:]
        sys.argv.extend(['tests/data/example.csv'])
        
        print sys.argv
        Weeker().run_it()

        # restore program args
        sys.argv = list(store)
