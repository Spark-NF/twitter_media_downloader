# coding: utf-8

import argparse
from datetime import datetime
import pytest
from ..src.args import parse_date, parse_args, parse_file_arg


def test_parse_date_invalid():
    with pytest.raises(argparse.ArgumentTypeError, match="Not a valid date: 'test'."):
        assert parse_date('test')


def test_parse_date_valid():
    assert parse_date('2019-06-27 13:20') == datetime(2019, 6, 27, 13, 20, 0, 0)
    assert parse_date('2019-06-27') == datetime(2019, 6, 27, 0, 0, 0, 0)


def test_parse_args():
    args = ['-o', 'out', '-f', '[%date%] %filename%.%ext%', '-s', 'large', '-u', 'Twitter']
    parsed = parse_args(args)
    assert parsed.userid == ['Twitter']
    assert parsed.o_userid is True
    assert parsed.output == 'out'
    assert parsed.format == '[%date%] %filename%.%ext%'
    assert parsed.image_size == 'large'


def test_parse_file_arg_basic():
    parsed = parse_file_arg('Twitter')
    assert parsed == ['Twitter']
