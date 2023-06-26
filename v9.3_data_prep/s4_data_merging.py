"""
Author: Sofia Kobayashi
Date: 06/18/2023
Description: Merging & cleaning data for stage 4 (merging data)!
"""
import pandas as pd
import json
import numpy as np
import re

with open('reference_info/author_aliases.json', 'r') as infile:
    AUTHOR_ALIASES = json.load(infile)

AUTHOR_WRAPS = ['smk_sources', 'version_nums','locations','explored_dates', \
                'all_ratings', 'aliases', 'dates_added', 'all_links']

LOCATION_ORDERING = {'archiveofourown.org': {'abbr': 'ao3', 'rank': 0},
                    'fanfiction.net': {'abbr': 'ffn_net', 'rank': 1},
                    'tumblr.com': {'abbr': 'tum', 'rank': 2},
                    'dreamwidth.org': {'abbr': 'drm', 'rank': 3},
                    'livejournal.com': {'abbr': 'lvj', 'rank': 4},
                    'facebook.com': {'abbr': 'fcb', 'rank': 5},
                    'wattpad.com': {'abbr': 'wat', 'rank': 6},
                    }

### ### HELPER FUNCTIONS ### ###
def wrap_df(df, columns) -> pd.DataFrame:
    """
    * General helper function * 
    Takes any df and a list of column names (list of str).
    Wraps all values of given columns in json.dumps(), to be loaded in later. 
        Doesn't modify original df.
    Returns wrapped df.
    """
    new_df = df.copy()

    for ind in new_df.index:
        for col in columns:
            if not np.any(pd.isnull(df[col])):
                new_df.at[ind, col] = json.dumps(df.at[ind, col])

    return new_df


def unwrap_df(df, columns) -> pd.DataFrame:
    """
    * General helper function * 
    Takes any df and a list of column names (list of str).
    Unwraps all values of given columns in json.loads(). Doesn't modify original df.
    Returns unwrapped df.
    """
    new_df = df.copy()

    for ind in new_df.index:
        for col in columns:
            if not np.any(pd.isnull(df[col])):
                new_df.at[ind, col] = json.loads(df.at[ind, col])

    return new_df

def url_domain(url) -> str:
    """
    * General helper function *
    Takes a url (str).
    Gets url's domain.
    Returns domain (str).
    """
    # Get the letters between // and the next /
    match = re.findall("//.+\.[A-Za-z0-9]+/", url)[0].replace('/','').split('.')
    if match:
        return f'{match[-2]}.{match[-1]}'


### ### AUTHOR METHODS ### ###
def get_author_stylization(url) -> str:
    """
    * Helper function for author_row_merge() *
    Takes an AO3_user url (str).
    Gets stylized author's name from url
    Returns stylized authors name (str).
    """    
    # Get the letters between /users/ and the next /
    if 'archiveofourown.org' in url:
        match = re.findall('/users/[A-Za-z0-9_]+(?:$|/)', url)
        if match: 
            return match[0].replace('/users/', '').replace('/','')
    elif 'fanfiction.net' in url:
        match = re.findall('/u/\d*/[A-Za-z0-9_]+(?:$|/)', url)
        if match: 
            name = match[0].split('/')[-1]
            if '-' not in name:
                return name
    return np.nan


def author_row_merge(df) -> dict:
    """
    Takes an author df (df), either text or url, ideally of multiple rows.
    Merges data, as specificed below, into a single row.
    Returns author dict of merged info (dict).
    """
    # Get name attributes
    author_name = df.iloc[0]['author_name'].lower().strip()
    ratings = [int(num) for num in df['author_rating'] if not pd.isnull(num)]
    avg_rating = round(sum(ratings)/len(ratings), 2) if len(ratings) != 0 else np.nan
    
    cur_alias = np.nan
    for alias in AUTHOR_ALIASES:
        if author_name in AUTHOR_ALIASES[alias]:
            cur_alias = alias
            break


    # Get version & source attrs
    version_nums = list(set(df['version_num'][df['version_num'].notnull()]))
    primary_version = min(version_nums)

    sources = list(set(df['smk_source'][df['smk_source'].notnull()]))
    primary_source = sorted(sources, key = lambda source: int(source[1]))[0]
    

    # Get is_bold & is_subbed attrs
    bold_list = list(set(df['is_bold'][df['is_bold'].notnull()]))
    is_bold = np.any(bold_list) if len(bold_list) != 0 else np.nan

    sub_list = list(set(df['is_subbed'][df['is_subbed'].notnull()]))
    is_sub = np.any(sub_list) if len(sub_list) != 0 else np.nan
    

    # Get dates attrs
    explored_dates = list(set([date.replace('/', '-') for date in df['explored_page_date'] 
                      if not pd.isnull(date)]))
    
    dates_added = np.nan
    if 'ffn_net_date_added' in df.columns:
        dates_added = list(set([date.replace('/', '-') for date in df['ffn_net_date_added'] 
                        if not pd.isnull(date)]))
        

    # Get links & author stylization, if possible
    sorted_links = []
    primary_link = np.nan
    if 'author_links' in df.columns:
        # Get list of links sorted by LOCATION_ORDERING
        links_list = [links.split(',') for links in df['author_links'] 
                              if not pd.isnull(links)]
        all_links = list(set([link.strip() for links in links_list 
                              for link in links if link != '']))
        sorted_links = sorted(all_links, 
                              key = lambda link: LOCATION_ORDERING.get(url_domain(link), {}).get('rank', 7))
        
        primary_link = sorted_links[0]


    # Get locations attrs
    link_locations = [LOCATION_ORDERING.get(url_domain(link), {}).get('abbr', 'oth') 
                      for link in sorted_links]
    df_locations = [loc.strip() for loc in df['location'] if not pd.isnull(loc)]
    locations = list(set(link_locations + df_locations))
    
    if not pd.isnull(primary_link):
        primary_location = LOCATION_ORDERING[url_domain(primary_link)].get('abbr', 'oth')
    elif locations:
        locs = [LOCATION_ORDERING[key]['abbr'] for key in LOCATION_ORDERING]
        primary_location = 'oth'
        for loc in locs:
            if loc in locations:
                primary_location = loc
                break
    else:
        primary_location = np.nan

    # Get author stylization attr
    author_stylized = np.nan
    if 'author_links' in df.columns:
        author_stylized = get_author_stylization(primary_link)
    
    # Store & return author row dict
    return {'primary_version': primary_version, 
            'version_nums': version_nums,
            'primary_source': primary_source,
            'smk_sources': sources, 
            'primary_location': primary_location,
            'locations': locations, 
            'is_bold': is_bold,
            'is_subbed': is_sub,
            'author_name': author_name, 
            'author_rating': avg_rating,
            'all_ratings': ratings,
            'explored_dates': explored_dates,
            'aliases': cur_alias,
            'dates_added': dates_added,
            'primary_link': primary_link,
            'all_links': sorted_links,
            'author_stylized': author_stylized,
            }

def clean_authors(authors_df, outfile_name) -> str:
    """
    * Main function for authors dtbs *
    Takes text or url author df (df) and the outfile name (str).
    On the author's name, merges & cleans info from all associated rows.
    Returns the outfile name (str).
    """
    # Initialize new container df
    container_df = pd.DataFrame(columns=['author_name', 'author_stylized', 
                                         'aliases', 'num_appeared', 
                                        'primary_version', 'version_nums', 
                                        'primary_source', 'smk_sources', 
                                        'primary_location', 'locations',
                                        'is_bold', 'is_subbed', 
                                        'author_rating', 'all_ratings', 
                                        'explored_dates', 'dates_added',
                                        'primary_link', 'all_links'])
    
    # Get & sort keys (author names)
    sorted_names = sorted(list(set([name.lower() for name in authors_df['author_name']])))

    # For each key, merge info from all associated rows
    for name in sorted_names:
        name_df = authors_df[authors_df['author_name'] == name]
        author_row = author_row_merge(name_df)
        author_row['num_appeared'] = len(name_df)
        container_df.loc[len(container_df.index)] = author_row

    # Write merge author df to outfile
    final_df = wrap_df(container_df, AUTHOR_WRAPS)
    final_df.to_csv(f"{outfile_name}", encoding='utf-8-sig')

    return outfile_name



def is_equal(row1, row2) -> bool:
    """
    Takes two fic or series rows from a database (df).
    Compares them to determine if they're the same fic.
    Returns a boolean of whether or not they're equal (bool).
    """
    same_title = row1.iloc[0]['title'] == row2.iloc[0]['title']
    
    author1 = row1.iloc[0]['author']
    author2 = row2.iloc[0]['author']
    same_author = author1 == author2
    absent_author = pd.isnull(author1) or pd.isnull(author2)
    same_location = (row1.iloc[0]['location'] == row2.iloc[0]['location']) or \
        pd.isnull(row1.iloc[0]['location']) or pd.isnull(row2.iloc[0]['location'])

    fandom1 = [fan.strip() for fan in row1.iloc[0]['fandom'].split(',')]
    fandom2 = [fan.strip() for fan in row2.iloc[0]['fandom'].split(',')]
    same_fandoms = len(set(fandom1) ^ set(fandom2)) == 0
    
    return same_title and same_fandoms and (same_author or (absent_author and same_location))
    

def section_fics(df) -> list:
    """
    Takes a df of fics (df).
    Sections all fics in given df into a list dfs.
    Returns lists of dfs (list of dfs).
    """
    df_list = [df.iloc[[0]].copy()]
    for ind in range(1, len(df)):
        for i in range(len(df_list)):
            attached = False
            fic1 = df.iloc[[ind]]
            fic2 = df_list[i].iloc[[0]]
            if is_equal(fic1, fic2):
                df_list[i].loc[len(df_list[i])] = fic1.to_dict(orient='records')[0]
                attached = True
                break
        if not attached:
            df_list.append(fic1)
    
    return df_list



if __name__ == "__main__":
    file_df = pd.read_csv('clean_data_4/all_versions_coffee.csv', \
                            encoding='utf-8-sig', index_col=0)
    

    # Initialize new container df
    coffee_df = pd.DataFrame(columns=['primary_version', 'version_nums',
                                      'primary_source', 'smk_sources',  
                                      'primary_location', 'locations',
                                      'work_type', 'fandom',
                                      'title', 'author', 
                                      'primary_link', 'all_links'
                                      'coffee_length', 'plot_type',  'coffee_tags',
                                      'is_filth', 'pairing',
                                      ])
    

    test_df = file_df[file_df['title'] == "a"]
    res = section_fics(test_df)
    print(res)
    # # Get & sort keys (author names)
    # sorted_titles = sorted(list(set([title.lower().strip() for title in authors_df['title']])))

    # # For each key, merge info from all associated rows
    # for title in sorted_titles:
    #     title_df = coffee_df[coffee_df['title'] == title]
    #     fic_rows = section_fics(title_df)
    #     author_row = 
    #     author_row['num_appeared'] = len(name_df)
    #     container_df.loc[len(container_df.index)] = author_row



    # # Write merge author df to outfile
    # final_df = wrap_df(container_df, AUTHOR_WRAPS)
    # final_df.to_csv(f"{outfile_name}", encoding='utf-8-sig')


    
    # print(sorted_titles)

    # AUTHOR MERGE TEST
    # small_df = authors_df[authors_df['author_name'] == 'cywscross']
    # res = author_row_merge(small_df)
    # for key in res:
    #     print(f'{key}  ---  {res[key]}')
    

