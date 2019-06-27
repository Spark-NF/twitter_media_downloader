# coding: utf-8

import argparse
from datetime import datetime
import pytest
from ..src.args import parseDate, parseArgs


def test_parseDate_invalid():
    with pytest.raises(argparse.ArgumentTypeError, match="Not a valid date: 'test'.") as e:
        assert parseDate('test')

def test_parseDate_valid():
    assert parseDate('2019-06-27 13:20') == datetime(2019, 6, 27, 13, 20, 0, 0)
    assert parseDate('2019-06-27') == datetime(2019, 6, 27, 0, 0, 0, 0)

def test_parseArgs():
    args = ['-o', 'out', '-f', '[%date%] %filename%.%ext%', '-s', 'large', '-u', 'Twitter']
    parsed = parseArgs(args)
    assert parsed.userid == 'Twitter'
    assert parsed.o_userid == True
    assert parsed.output == 'out'
    assert parsed.format == '[%date%] %filename%.%ext%'
    assert parsed.image_size == 'large'
