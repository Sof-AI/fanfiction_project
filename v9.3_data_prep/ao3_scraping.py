"""
Author: Sofia Kobayashi
Date: 06/30/2023
Description: Functions to scrape AO3.
"""
import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

import AO3
import pandas as pd
import json


def get_series_fandoms(series_obj) -> list:
    """
    * helper function, exists bc this will be a common list comprehension 
    Takes a AO3.Series obj.
    Gets the fandoms from all the works in that series.
    Returns list of fandoms (list).
    """
    return list(set([fandom for work in series_obj.work_list 
                     for fandom in work.fandoms]))


def get_fic_info(id, session=None) -> dict:
    """
    Takes an AO3 series id or url (int or str).
    Uses Unoffical AO3 API to get series' name, fandoms, and authors.
    Returns dict with above info (dict).
    """
    # Get series obj
    id = str(id)
    if 'archiveofourown.org' in id:
        id = AO3.utils.workid_from_url(id)
    series = AO3.Series(int(id))

    return {'title': series.name,
            'fandoms': get_series_fandoms(series),
            'authors': [user.username for user in series.creators]}

if __name__ == '__main__':
    # print(dir(AO3.Series))

    sess = AO3.Session(os.environ['AO3_USERNAME'], os.environ['AO3_PASSWORD'])
    res = get_fic_info(1540144, session=sess)
    print(res)


