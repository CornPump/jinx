from helpers import files,smath
import pytest


@pytest.mark.parametrize("orig, dest, t_res", [
    (13335, 10, 1333500000),
    (42, 5, 42000),
    (987654322, 3, 987),
])
def test_straighten_digits(orig, dest, t_res):
    res = smath.straighten_digits(orig,dest)
    assert res == t_res


def test_convert_utc_to_date():
    utc = 1693856726
    tres = '2023-09-04'
    res = files.convert_utc_to_date(utc)
    assert tres == res


def test_convert_date_to_utc():
    utc = 1693785600
    date = files.convert_utc_to_date(utc)
    res = int(files.convert_date_to_utc(date))
    assert res == utc

