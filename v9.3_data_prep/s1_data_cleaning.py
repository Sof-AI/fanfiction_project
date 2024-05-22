"""
Author: Sofia Kobayashi
Date: 05/12/2023
Description : Converting stage 0 data -> clean, consistent CSVs.
* data cleaning & condensation stages: 0 (collection) & 1 (structure)
"""
import pandas as pd
import numpy as np
import json

import bs4 as bs
import urllib.request
import requests

import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

### CONSTANTS & ERRORS ###
with open('reference_info/fandom_aliases.json', 'r') as infile:
    FANDOM_NAMES = json.load(infile)

class UnknownFandomException(Exception):
    pass

### HELPER FUNCTIONS ###
def get_clean_fandom_name(unclean_fandom_name) -> str:
    """
    * Helper function for clean_fandom_names() and fandom_report() * 
    Takes an uncleaned fandom name (str).
    Checks if it's a clean name or fandom alias. 
    Returns clean fandom name (str) if one found, else returns None.
    """
    unclean_fandom_name = unclean_fandom_name.lower().strip()

    # Return fandom name if it's recognized & clean
    if unclean_fandom_name in FANDOM_NAMES.keys():
        return unclean_fandom_name

    # Else, search for an alias 
    for fandom in FANDOM_NAMES:
        if unclean_fandom_name in FANDOM_NAMES[fandom]:
            return fandom
    

def add_category(fic_dict, df, ser_fic_type='fic') -> str:
    """
    * Helper function for add_all_categories() * 
    Takes fic_dict: {category, fandom, title} (dic) and fic_df (df).
    Tries to merge categories from fic_dict into df on fic title, if possible.
    Returns a success/failure code (str). 
    """
    # define column names
    col_title = f'{ser_fic_type}_title'
    col_fandom = f'{ser_fic_type}_fandom'
    col_category = f'{ser_fic_type}_category'

    DEBUG = 0
    if fic_dict['title'] == 'basic instincts':
        DEBUG = 0

    # try to match category
    num_title_matches = 0
    for ind in df.index:
        # get title
        title = df.at[ind, col_title]
        if not isinstance(title, str):
            continue
        title = title.strip().lower()
        
        # check title
        if title == fic_dict['title'].strip():
            num_title_matches += 1

            # get fandoms
            fandoms = df.at[ind, col_fandom]
            if not isinstance(fandoms, str):
                continue
            fandoms = set([fan.strip() for fan in fandoms.strip().split(',')])
           
            # check fandoms
            if fandoms == fic_dict['fandom']:
                # insert the category/ies
                cur_cat = df.at[ind, col_category]
                if not pd.isnull(cur_cat):
                    new_cat = set(cur_cat.split(','))
                    new_cat.update(fic_dict['category'])
                    new_cat = new_cat
                else:
                    new_cat = fic_dict['category']
                
                # insert category into ffn_dtb
                df.at[ind,col_category] = (',').join(list(new_cat))
                return 'success - category added'
    
    # if no matches (on title), insert category-fic row into ffn_dtb
    if num_title_matches == 0:
        df.loc[len(df.index)] = {col_title: fic_dict['title'],
                                 col_fandom: (',').join(list(fic_dict['fandom'])),
                                 col_category: (',').join(list(fic_dict['category'])),
                                 'smk_source': f'6_category',
                                 'dtb_type': 'read',}
        return 'success - no matches, so added fic'

    return 'failed - no match found'
        
    
def make_cat_fic_dicts(cat_df, ser_fic_type='fic'):
    """
    * Helper function for add_all_categories() * 
    Takes category_df (category, series, title) (df).
    Reads in category_df -> a list of fic_dicts {category, fandom, title}.
    Returns a list of fic dicts (list of dicts).
    """
    col_category = f'{ser_fic_type}_category'
    col_fandom = f'{ser_fic_type}_fandom'
    col_title = f'{ser_fic_type}_title'

    # assemble & add all fics from category_df
    categories = []
    for ind in cat_df.index:
        # get category row
        cat_row = cat_df.iloc[[ind]]

        # get relevant data from row
        cat = set(cat_row[col_category])
        fandom = set([fan.strip() for fan in list(cat_row[col_fandom])[0].split(',')])
        title = list(cat_row[col_title])[0].strip().lower()

        # assemble fic_dict
        fic_dict = {'category': cat,
                    'fandom': fandom,
                    'title': title,}
        
        categories.append(fic_dict)

    return categories



### MAIN FUNCTIONS ###
def clean_fandom_names(dtb, fandom_col_name, verbose=False, blank_okay=False, old=False) -> str:
    """
    * Main function * 
    Takes a database (DF) and name of the fandom column (str)
    Reads the fandoms in the given dtb -> changes all fandom names to be
        consistent to the ones in FANDOM_NAMES.
    Returns status update.
    """
    changed_count = 0
    all_clean = {}
    for ind in dtb.index:
        # Get & clean fandom string
        fandom_str = dtb.at[ind, fandom_col_name]

        if pd.isnull(fandom_str) and blank_okay:
            all_clean[ind] = ""
            continue        

        if old:
            fandom_list = fandom_str.replace("*", "").replace(" x ", ",").split(",")
        else:
            fandom_list = json.loads(fandom_str)

        # Get the clean fandom for each fandom in fic
        clean_fandoms = []
        for old_fandom in fandom_list:
            if old_fandom == "":
                continue
            clean_fandom = get_clean_fandom_name(old_fandom)
            if not clean_fandom:
                raise UnknownFandomException(f'{old_fandom} for a recognized fandom or fandom alias!')
            else:
                clean_fandoms.append(clean_fandom)
    
        # Insert clean fandoms
        print(clean_fandom)
        clean_fandoms = list(set(clean_fandoms))
        if old:
            dtb.at[ind, fandom_col_name] = ",".join(clean_fandoms)
        else:
            dtb.at[ind, fandom_col_name] = json.dumps(clean_fandoms)

    return f"Fandoms all clean, {changed_count} changed!"


def fandom_report(dtb, fic_col, verbose=False, old=False) -> int:
    """
    * Main function * 
    Takes a database (DF), name of the fandom column (str), and verbose 
        switch (boolen).
    Checks all fandoms in given column & prints a report on state of that fandom
        col (errors/blanks, number of datapoints, known/unknown, uniqueness).
    Returns success/failure status (str).
    """
    known_fandoms = []
    unknown_fandoms = []
    clean_fandoms = []
    error_ind = set()
    num_rows = len(dtb)
    
    # for each fandom row
    for ind in dtb.index:
        fandom_str = dtb.loc[ind].loc[fic_col]
        
        # if fandom cell empty
        if pd.isnull(fandom_str):
            error_ind.add(ind)
            continue
        
        # clean fandom string
        if old:
            fandom_list = fandom_str.replace('*','') \
                            .replace(' x ',',') \
                            .split(',')
        else:
            fandom_list = json.loads(fandom_str)

        
        # for each fandom in fic
        for old_fandom in fandom_list:
            if old_fandom == "":
                continue
            
            # get clean fandom
            if old_fandom in FANDOM_NAMES.keys():
                clean_fandoms.append(old_fandom)
                clean_fandom = old_fandom
            else:
                clean_fandom = get_clean_fandom_name(old_fandom)
            
            # if no clean fandom found
            if not clean_fandom:
                unknown_fandoms.append((ind, old_fandom))
            else:
                known_fandoms.append(clean_fandom)
    
    # print report
    unknown_fandom_names = []
    if unknown_fandoms:
        unknown_fandom_names = list(zip(*unknown_fandoms))[1]
    
    num_unclean = len(set(known_fandoms))-len(set(clean_fandoms))
    if verbose:
        print(f'- --- FANDOM REPORT --- -')
        print(f'- # rows/fandoms:           {num_rows}')
        print(f'- # errors (row num):       {len(error_ind)}')
        [print('  ', err) for err in error_ind]
        print(f'- # unique known fandoms:   {len(set(known_fandoms))} (total), \
            {len(set(clean_fandoms))} (clean), {num_unclean} (unclean)')
        print(f'- # unique unknown fandoms: {len(set(unknown_fandom_names))}')
        [print('  ', fname) for fname in set(unknown_fandom_names)]

    if len(error_ind) == 0 and len(set(unknown_fandom_names)) == 0:
        if num_unclean == 0:
            return f"Ideal - all fandoms known & clean!"
        return f"Good - all fandoms known, but {num_unclean} unclean"
    return f"Bad - {len(error_ind)} errors and {len(set(unknown_fandom_names))} unknown fandoms"


def add_all_categories(category_df, fic_df, ser_fic_type='fic') -> list:
    """
    * Main function * 
    Takes category df & fic df.
    Modified inplace fic_df by adding categories from df where possible.
    Returns list of unmatched fic_dicts.
    """
    # create fic_dicts
    fic_dicts = make_cat_fic_dicts(category_df, ser_fic_type)
    unmatched = []

    # try to match all categories
    for fic in fic_dicts:
        # print(fic)
        status = add_category(fic, fic_df, ser_fic_type)
        # print(status)
        # print()
        if 'failed' in status:
            unmatched.append(fic)
    
    return unmatched
    

def get_my_bookmarks():
    """
    * Main function *
    Takes nothing.
    Grabs bookmarked series, works, and users from my AO3 account using an 
        authenicated session.
    Returns list of bookmarked series, works, and users (list of lists).
    """
    # Aet AO3 login html
    source = urllib.request.urlopen("https://archiveofourown.org/users/login").read()
    soup = bs.BeautifulSoup(source,'lxml')

    # Get ao3 authenticity token
    authenticity_token = soup.find("input", {"name": 'authenticity_token'})["value"]

    # Define payload
    payload = {'user[login]': os.environ['AO3_USERNAME'],
                'user[password]': os.environ['AO3_PASSWORD'],
                'authenticity_token': authenticity_token}

    # Initialize bookmark containers
    all_bm_works = []
    all_bm_series = []
    all_bm_users =[]

    # Define requests session
    with requests.Session() as sess:
        # Post payload
        post = sess.post("https://archiveofourown.org/users/login", params=payload, allow_redirects=False)
        if not post.status_code == 302:
                print("DID NOT WORK")
        
        # Get links from each page
        total_pages = 60
        for i in range(1, total_pages):
            print(f'Starting page {i} of {total_pages}')
            # Get html from protected url with authenticated session
            url = f'https://archiveofourown.org/users/{os.environ["AO3_USERNAME"]}/bookmarks?page='+str(i)
            p1 = sess.get(url)
            soup1 = bs.BeautifulSoup(p1.text,'lxml')
        
            # Grab desired info
            bookmarks = soup1.find("ol", {"class": "bookmark index group"})
            for bookm in bookmarks.find_all("li", {"class": ["bookmark", "index", "group"]}):
                if bookm.h4 is not None:
                    user_block = bookm.find_all('div',{'class': ['own','user','module','group']})[1]
                    date = user_block.find('p', {'class':'datetime'}).text
                    tags = [tag.text for tag in user_block.find_all('li')]
                    try:
                        notes = user_block.find_all('p')[1].text
                    except:
                        notes = ""
                    for a in bookm.h4.find_all("a"):
                        if a.attrs["href"].startswith("/works"):
                            workname = str(a.string)
                            url = f'https://archiveofourown.org{a["href"]}'

                            temp = [workname, url, date, tags, notes]

                            if 'works' in a["href"]:
                                all_bm_works.append(temp)
                            elif 'series' in a["href"]:
                                all_bm_series.append(temp)
                            else:
                                all_bm_users.append(temp)

    return [all_bm_series, all_bm_works, all_bm_users]

        


if __name__ == '__main__':
    pass
    # series_df = pd.read_csv('series_url_test.csv')
    # fandom_report(series_df, 'fandom',True)
    # res = clean_fandom_names(series_df, "fandom", verbose=True, blank_okay=False, old=False)
    # print(res)
    # series_df.to_csv('test1.csv')

    # bookmarks_list = get_my_bookmarks()
    # bookmarks_df = pd.DataFrame(bookmarks_list, columns=['series', 'works', 'users'])\
    #     .to_csv('my_bookmarks.csv')