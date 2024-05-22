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

import s4_data_merging


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
    series = AO3.Series(int(id), session)

    return {'title': series.name,
            'fandom': get_series_fandoms(series),
            'author': [user.username for user in series.creators]}

if __name__ == '__main__':
    pass
    # print(dir(AO3.Series))
    # file_df = pd.read_csv('clean_data_4/all_versions_series_url.csv', encoding='utf-8-sig')
    # series_ids = file_df[file_df.index >= 179]['series_id']

    # sess = AO3.Session(os.environ['AO3_USERNAME'], os.environ['AO3_PASSWORD'])
    # AO3.utils.limit_requests()

    # container_df = pd.DataFrame(columns=['series_id', 'title', 'fandom', 'author'])
    
    # for i, id in enumerate(series_ids):
    #     try:
    #         print(id)
    #         series_row = get_fic_info(id, session=sess)
    #         series_row['series_id'] = id
    #         container_df.loc[len(container_df)] = series_row
    #         print(f' - wrote {i+1} of {len(container_df)}')
    #     except:
    #         print('ERROR:', id)
    
    # write_df = s4_data_merging.wrap_df(container_df, ['fandom', 'author'])
    # print(write_df)
    # write_df.to_csv('names1.csv', encoding='utf-8-sig')



