#!/usr/bin/env python3
"""
Unit and regression test for the follicle_diameters package.
"""

# Import package, test suite, and other packages as needed

import unittest
import sys
import hashlib
import logging
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from follicle_diameters.dataproc import parse_cmdline
from follicle_diameters.dataproc import read_files
from follicle_diameters.dataproc import clean
from follicle_diameters.dataproc import main
import pandas as pd

# __author__ = 'ikopyeva'

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)


class Test_parse_cmdline(unittest.TestCase):
    def testOneRealFile(self):
        test_input = ['-f', 'data/BMB.csv']
        foo = parse_cmdline(test_input)
        self.assertTrue(parse_cmdline(test_input)[0]['file'] == ['data/BMB.csv'])

    def testTwoRealFileOneFlag(self):
        test_input = ['-f', 'data/BMB.csv', 'data/RGD.csv']
        foo = parse_cmdline(test_input)
        ret = parse_cmdline(test_input)[0]['file']
        self.assertTrue('data/BMB.csv' in ret and 'data/RGD.csv' in ret)

    def testTwoRealFileTwoFlags(self):
        test_input = ['-f', 'data/BMB.csv', '-f', 'data/RGD.csv']
        foo = parse_cmdline(test_input)
        ret = parse_cmdline(test_input)[0]['file']
        self.assertTrue('data/BMB.csv' in ret and 'data/RGD.csv' in ret)

    def testThreeRealFileTwoFlags(self):
        test_input = ['-f', 'data/BMB.csv', 'data/RGD.csv', '-f', 'data/HBP.csv']
        foo = parse_cmdline(test_input)
        ret = parse_cmdline(test_input)[0]['file']
        self.assertTrue('data/BMB.csv' in ret and 'data/RGD.csv' in ret and 'data/HBP.csv')

    def testBadFile(self):
        test_input = ['-f', '/foo/bar.csv']
        self.assertTrue(parse_cmdline(test_input)[1] == 2)

    def testOneBadOneGood(self):
        test_input = ['-f', 'data/BMB.csv', '/foo/bar.csv']
        self.assertTrue(parse_cmdline(test_input)[1] == 2)

    def testOutputGood(self):
        test_input = ['-f', 'data/BMB.csv', '-o', 'foo.png']
        ret = parse_cmdline(test_input)
        path = Path("foo.png").resolve()
        self.assertTrue(ret[0]['output'] == path)

    def testOutputGoodDiffDir(self):
        test_input = ['-f', 'data/BMB.csv', '-o', '/foo.png']
        ret = parse_cmdline(test_input)
        path = Path("/foo.png").resolve()
        self.assertTrue(ret[0]['output'] == path)

    def testBadFlag(self):
        test_input = ['-z']
        with self.assertRaises(SystemExit) as cm:
            parse_cmdline(test_input)

        self.assertEqual(cm.exception.code, 2)

    def testNoArgs(self):
        test_input = []
        with self.assertRaises(SystemExit) as cm:
            parse_cmdline(test_input)

        self.assertEqual(cm.exception.code, 2)



class Test_read_files(unittest.TestCase):

    def testOneFile(self):
        test_input = ['data/BMB.csv']
        data = read_files(test_input)
        self.assertTrue(type(data['BMB']) == pd.DataFrame)

    def testSameDirFile(self):
        test_input = ['BMB.csv']
        data = read_files(test_input)
        self.assertTrue(type(data['BMB']) == pd.DataFrame)

    def testTwoFile(self):
        test_input = ['data/BMB.csv', 'data/RGD.csv']
        data = read_files(test_input)
        self.assertTrue(type(data['BMB']) == pd.DataFrame and type(data['RGD']) == pd.DataFrame)


class Test_clean(unittest.TestCase):

    def testOneNanRow(self):
        test_input = ['data/BMB.csv']
        data = read_files(test_input)
        clean_data = read_files(['data/BMB_clean.csv'])
        ret = clean(data['BMB'])
        self.assertTrue(ret.equals(clean_data['BMB_clean']))

    def testNoNanRow(self):
        test_input = ['data/HBP.csv']
        data = read_files(test_input)
        clean_data = read_files(['data/HBP_clean.csv'])
        ret = clean(data['HBP'])
        self.assertTrue(ret.equals(clean_data['HBP_clean']))


class Test_main(unittest.TestCase):

    def testGoodOutput(self):
        test_input = ['-f', 'data/BMB.csv', '-o', 'data/BMB.png']
        main(test_input)
        actual = hash('data/BMB.png')
        expected = hash('data/BMB_clean.png')
        self.assertTrue(expected == actual)


def hash(file):
    BUF_SIZE = 1000  # lets read stuff in 64kb chunks!
    sha1 = hashlib.sha1()
    with open('data/BMB.png', 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return(sha1.hexdigest())

# Utility functions

# From http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
@contextmanager
def capture_stdout(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out


if __name__ == '__main__':
    unittest.main()
