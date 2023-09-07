import binance
import pytest
import random
import datetime
from helpers import files


@pytest.mark.parametrize("coin,limit, t_res", [
    ('BTC', 10, 10),
    ('ETH', 1900, 1000),
    ('bad', 5, 5),
    ('BTC', -1, 5),])
def test_get_price_data_by_limit(coin,limit, t_res):
    r = binance.get_price_data_by_limit(coin, limit)
    if isinstance(r, list):
        rlen = len([x for x in r])
        assert rlen == t_res


def generate_random_dates(num):
    BINANCE_MAX = 500
    random_dates = []
    for i in range(num):
        year = random.randint(2017, 2023)
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        delta = random.randint(1, 1300)
        succeed = False
        while not succeed:
            try:
                start_date = datetime.datetime(year, month, day)
                if start_date > datetime.datetime.now():
                    start_date = datetime.datetime.now() - datetime.timedelta(days=-1)
                succeed = True
            except:
                day -= 1
                delta -= 1
        end_date = start_date + datetime.timedelta(days=delta)
        if end_date > datetime.datetime.now():
            end_date = datetime.datetime.now()
            delta = (end_date - start_date).days
        if delta > BINANCE_MAX:
            delta = BINANCE_MAX
        else:
            delta += 1
        random_dates.append((start_date,end_date,delta))
    return random_dates


@pytest.mark.parametrize("start_date,end_date, t_res", generate_random_dates(4))
def test_get_price_data_by_segment(start_date,end_date, t_res):
    start_date = int(files.covert_date_to_utc(str(start_date.date())))
    end_date = int(files.covert_date_to_utc(str(end_date.date())))
    r = binance.get_price_data_by_segment('BTC',start_date,end_date)
    if isinstance(r, list):
        rlen = len([x for x in r])
        assert rlen == t_res