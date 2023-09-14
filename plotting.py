import datetime
import binance
import os
import random
import json
from finbert import OUTPUT_FILE_NAME
from helpers import files


class Plot:

    def __init__(self, start: int = 0, end: int = 0, price: bool = True, comments: bool = True,
                 llm: bool = False, comment_dir: str = '', coin: str = ''):
        self.start = start
        self.end = end
        self.price = price
        self.comments = comments
        self.llm = llm
        self.comment_dir = comment_dir
        self.coin = coin

    def __str__(self):
        return (f"{{'start': {self.start}, 'end': {self.end}, "
                f"'price': {self.price}, 'comments': {self.comments}, "
                f"'llm': {self.llm}, 'comment_dir': '{self.comment_dir}', "
                f"'coin': '{self.coin}'}}")

    def params(self):
        return {'start': self.start, 'end': self.end, 'price': self.price,
                'comments': self.comments, 'llm': self.llm,
                'comment_dir': self.comment_dir, 'start': self.coin}

    # start_date,end_date = ins.create_range()
    def create_range(self):
        files_lst = os.listdir(self.comment_dir)
        if OUTPUT_FILE_NAME in files_lst:
            files_lst.remove(OUTPUT_FILE_NAME)

        first_file_date = files.fetch_date_from_comment_file(files_lst[0])
        start_date = end_date = files.convert_str_date_to_datetime(first_file_date)

        for file in files_lst:
            this_file_str_date = files.fetch_date_from_comment_file(file)
            this_file_date = files.convert_str_date_to_datetime(this_file_str_date)

            if this_file_date < start_date:
                start_date = this_file_date
            if this_file_date > end_date:
                end_date = this_file_date

        return start_date, end_date

    def collect_data(self):
        data = {'timestamp': [], 'open': [], 'high': [],
                'low': [], 'close': [], 'volume': [], 'llm': [], }

        # all comments data files
        files_lst_tmp = os.listdir(self.comment_dir)

        # remove sentiment data file
        if OUTPUT_FILE_NAME in files_lst_tmp:
            files_lst_tmp.remove(OUTPUT_FILE_NAME)

        date_range_flag = self.start and self.end

        # if we have start and end utc aka range params, use data files from the range only
        if date_range_flag:
            start_date = files.convert_str_date_to_datetime(files.convert_utc_to_date(self.start))
            end_date = files.convert_str_date_to_datetime(files.convert_utc_to_date(self.end))

        else:
            start_date, end_date = self.create_range()

        # remove out-of-range files
        file_lst = files_lst_tmp
        for file in files_lst_tmp:
            file_date_str = files.fetch_date_from_comment_file(file)
            file_date = files.convert_str_date_to_datetime(file_date_str)

            # don't work on out-of-range files
            if date_range_flag and file_date > end_date or file_date < start_date:
                file_lst.remove(file)

        # step gather binance price data
        if self.price:

            start_utc = int(files.convert_date_to_utc(str(start_date.date())))
            end_utc = int(files.convert_date_to_utc(str(end_date.date())))
            delta = (end_date.date() - start_date.date()).days
            raw_price_data = []


            if delta <= binance.BINANCE_GET_PRICE_DATA_BY_SEGMENT_MAX_OUTPUT:
                raw_price_data = binance.get_price_data_by_segment(self.coin,start_utc,end_utc)

            else:
                start_date_dynamic,end_date_dynamic = start_date,None
                first_flag = True
                loops = int(delta/binance.BINANCE_GET_PRICE_DATA_BY_SEGMENT_MAX_OUTPUT) + 1
                for i in range(1, loops+1):
                    if first_flag:
                        first_flag = False
                    else:
                        start_date_dynamic = end_date_dynamic + datetime.timedelta(days=1)
                    if i != loops:
                        end_date_dynamic = start_date_dynamic + datetime.timedelta \
                            (days=(binance.BINANCE_GET_PRICE_DATA_BY_SEGMENT_MAX_OUTPUT - 1))
                    else:
                        end_date_dynamic = end_date

                    raw_price_data += binance.get_price_data_by_segment(self.coin,
                                                            files.convert_date_date_to_utc(start_date_dynamic),
                                                            files.convert_date_date_to_utc(end_date_dynamic))

            """
            data = {'timestamp': [], 'open': [], 'high': [],
                'low': [], 'close': [], 'volume': [], 'llm': [], }
            """
            for val in raw_price_data:
                utc = val[binance.BINANCE_UIKLINES.date.value]
                str_date = files.convert_utc_to_date(utc)
                data['timestamp'].append(files.convert_str_date_to_datetime(str_date))

                data['open'].append(float(val[binance.BINANCE_UIKLINES.open.value]))
                data['high'].append(float(val[binance.BINANCE_UIKLINES.high.value]))
                data['low'].append(float(val[binance.BINANCE_UIKLINES.low.value]))
                data['close'].append(float(val[binance.BINANCE_UIKLINES.close.value]))

            # step llm fetch all comments and grade on daily basis
            if self.llm:
                path = os.path.join(self.comment_dir,OUTPUT_FILE_NAME)
                with open(path, 'r') as f:
                    lst = json.load(f)

                for dic in lst:

                    # Check data is in the range
                    date_str_tmp = files.fetch_date_from_comment_file(dic['file'])
                    date_str = files.convert_str_date_to_datetime(date_str_tmp)
                    if start_date <= date_str <= end_date:

                        data['volume'].append(dic['num_comments'])
                        data['llm'].append(round(dic['sentiment_score'], 2))

            # if llm = False create random sentiment analysis
            else:
                data['volume'].append(random.randint(20, 2000))
                data['llm'].append(round(random.uniform(-1, 1), 2))

        return data





