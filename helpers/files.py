import json
import os
import datetime

# number of digits date.date package expects for UTC figures
DATETIME_UTC_INT_DIGITS = 10


# Creates a new directory with name, if already exists does nothing
def create_directory(name,dir):
    new_dir = os.path.join(dir,name.lower())
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    return new_dir


def covert_utc_to_date(utc):
    utc = int((str(utc))[:DATETIME_UTC_INT_DIGITS])
    tmp = datetime.datetime.utcfromtimestamp(int(utc))
    date = tmp.strftime('%Y-%m-%d')
    return date


def covert_date_to_utc(date):
    tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
    utc = str(int(tmp.replace(tzinfo=datetime.timezone.utc).timestamp()))
    return utc


def convert_str_date_to_datetime(str_date):
    lst = str_date.split('-')
    dd = datetime.datetime(int(lst[0]), int(lst[1]), int(lst[2]))
    return dd


def create_file_name(post,dir,utc):
    f = post + '_' + covert_utc_to_date(utc) + '.json'
    f = os.path.join(dir,f)
    return f


def save_comments_to_file(file_name,comments):
    print(f"Dumping comments to file {os.path.basename(file_name)}")
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(comments, file, ensure_ascii=False, indent=4)