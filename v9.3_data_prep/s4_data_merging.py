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

AUTHOR_WRAPS = ['smk_sources', 'version_nums','locations','explored_dates', 
                'all_ratings', 'aliases', 'dates_added', 'all_links']
COFFEE_WRAPS = ['version_nums','smk_sources','locations', 'fandom','author',
                'all_links','coffee_tags']
SERIES_WRAPS = ['version_nums', 'smk_sources', 'locations', 'all_links',
                'dtb_types', 'fandom', 'author', 'categories', 'all_tags',
                'all_ratings']

LOCATION_ORDERING = {'archiveofourown.org': {'abbr': 'ao3', 'rank': 0},
                    'fanfiction.net': {'abbr': 'ffn_net', 'rank': 1},
                    'tumblr.com': {'abbr': 'tum', 'rank': 2},
                    'dreamwidth.org': {'abbr': 'drm', 'rank': 3},
                    'livejournal.com': {'abbr': 'lvj', 'rank': 4},
                    'facebook.com': {'abbr': 'fcb', 'rank': 5},
                    'wattpad.com': {'abbr': 'wat', 'rank': 6},
                    }

DTBTYPE_ORDERING = {'read': 1,
                    'cont_read': 2,
                    'to_read': 3}

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
    container_df = pd.DataFrame(columns=['num_appeared',
                                         'author_name', 'author_stylized', 
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

def coffee_row_merge(df) -> dict:
    """
    Takes a coffee df (df), either text or url, ideally of multiple rows.
    Merges data, as specificed below, into a single row.
    Returns author dict of merged info (dict).
    """

    # Get lists & primary versions
    version_nums = list(set(df['version_num'][df['version_num'].notnull()]))
    primary_version = min(version_nums)

    sources = list(set(df['smk_source'][df['smk_source'].notnull()]))
    primary_source = sorted(sources, key = lambda source: int(source[1]))[0]

    locations = list(set(df['location'][df['location'].notnull()]))
    primary_loc = locations[0]

    links = list(set(df['url'][df['url'].notnull()]))
    primary_link = links[0] if len(links) != 0 else np.nan


    # Get primary str
    work_type = list(set(df['work_type'][df['work_type'].notnull()]))[0]
    title = df.iloc[0]['title'].strip().lower()

    coffee_lens = list(set(df['coffee_length'][df['coffee_length'].notnull()]))
    coffee_len = np.nan if len(coffee_lens) == 0 else coffee_lens[0].lower()

    plot_types = list(set(df['plot_type'][df['plot_type'].notnull()]))
    plot_type = plot_types[0] if len(plot_types) != 0 else np.nan

    pairings = list(set(df['pairing'][df['pairing'].notnull()]))
    pairing = pairings[0] if len(pairings) != 0 else np.nan


    # Get boolean cols
    fil_list = list(set(df['is_filth'][df['is_filth'].notnull()]))
    is_fil = np.any(fil_list) if len(fil_list) != 0 else np.nan

    # Breakup vals -> clean lists
    fandoms = list(set([fan.strip().lower() for fan_list in df['fandom'][df['fandom'].notnull()] 
                        for fan in fan_list.split(',')]))
    authors = list(set([author.strip().lower() for author_list in df['author'][df['author'].notnull()] 
                        for author in author_list.split(',')]))
    tags = list(set([author.strip().lower() for author_list in df['coffee_tags'][df['coffee_tags'].notnull()] 
                        for author in author_list.split(',')]))


    return {'primary_version': primary_version, 
            'version_nums': version_nums,
            'primary_source': primary_source,
            'smk_sources': sources, 
            'primary_location': primary_loc, 
            'locations': locations,
            'work_type': work_type, 
            'fandom': fandoms,
            'title': title, 
            'author': authors, 
            'primary_link': primary_link, 
            'all_links' : links,
            'coffee_length': coffee_len, 
            'plot_type': plot_type,
            'coffee_tags': tags,
            'is_filth': is_fil, 
            'pairing': pairing,
            }


def clean_coffee(coffee_df, outfile_name) -> None:
    """
    Takes a coffee df (df) and outfile name (str).
    Cleans & merges coffee df & write it to CSV.
    Returns nothing.
    """
    # Initialize new container df
    container_df = pd.DataFrame(columns=['num_appeared',
                                         'primary_version', 'version_nums',
                                        'primary_source', 'smk_sources',  
                                        'primary_location', 'locations',
                                        'work_type', 'fandom',
                                        'title', 'author', 
                                        'primary_link', 'all_links',
                                        'coffee_length', 'plot_type',  'coffee_tags',
                                        'is_filth', 'pairing', 
                                        ])
    
    # Section & sort fics
    print('- sectioning')
    sections = section_fics(coffee_df, fic_equal)
    
    print('- sorting')
    sorted_sections = sorted(sections, key=lambda sec: sec.iloc[0]['title']) 

    # Add cleaned rows to container
    for i, sec in enumerate(sorted_sections):
        fic_row = coffee_row_merge(sec)
        fic_row['num_appeared'] = len(sec)
        container_df.loc[len(container_df.index)] = fic_row
        print(f'  - processed {i+1} of {len(sorted_sections)}')

    # Write to CSV
    write_df = wrap_df(container_df, COFFEE_WRAPS)
    write_df.to_csv(outfile_name)
    print(f'- Wrote to {outfile_name}')


def series_row_merge(df) -> dict:
    """
    Takes a series df (df), either text or url, ideally of multiple rows.
    Merges data, as specificed below, into a single row.
    Returns author dict of merged info (dict).
    """
    # Get lists & primary versions
    version_nums = list(set([int(num) for num in df['version_num'][df['version_num'].notnull()]]))
    primary_version = min(version_nums)

    sources = list(set(df['smk_source'][df['smk_source'].notnull()]))
    print(sources)
    primary_source = sorted(sources, key = lambda source: int(source[1]))
    primary_source = primary_source[0] if len(primary_source) != 0 else np.nan

    types = list(set(df['dtb_type'][df['dtb_type'].notnull()]))
    primary_type = sorted(sources, key = lambda source: int(source[1]))
    primary_type = primary_type[0] if len(primary_type) != 0 else np.nan

    all_ratings = list(set(df['series_rating'][df['series_rating'].notnull()]))
    rating = sum(all_ratings)/len(all_ratings) if len(all_ratings) != 0 else np.nan

    cur_chaps = list(set(df['current_chapter'][df['current_chapter'].notnull()]))
    cur_chap = 're' if 're' in cur_chaps else (max(cur_chaps) if len(cur_chaps) != 0 else np.nan)


    # Get primary str
    title = df.iloc[0]['title']
    title = title.strip().lower() if not pd.isnull(title) else np.nan
    

    lens = list(set(df['series_length'][df['series_length'].notnull()]))
    length = np.nan if len(lens) == 0 else lens[0]
    if isinstance(length, str):
        length = length.lower()


    # Get boolean cols
    bold_list = list(set(df['is_bold'][df['is_bold'].notnull()]))
    is_bold = np.any(bold_list) if len(bold_list) != 0 else np.nan

    sub_list = list(set(df['is_subbed'][df['is_subbed'].notnull()]))
    is_sub = np.any(sub_list) if len(sub_list) != 0 else np.nan

    cof_list = list(set(df['is_coffee'][df['is_coffee'].notnull()]))
    is_cof = np.any(cof_list) if len(cof_list) != 0 else np.nan

    comp_list = list(set(df['is_complete'][df['is_complete'].notnull()]))
    is_comp = np.any(comp_list) if len(comp_list) != 0 else np.nan

    bookm_list = list(set(df['is_bookmarked'][df['is_bookmarked'].notnull()]))
    is_bookm = np.any(bookm_list) if len(bookm_list) != 0 else np.nan

    fin_list = list(set(df['is_finished_inputting_info'][df['is_finished_inputting_info'].notnull()]))
    is_finished = np.any(fin_list) if len(fin_list) != 0 else np.nan


    # Breakup vals -> clean lists
    fandoms = list(set([fan.strip().lower() for fan_list in df['fandom'][df['fandom'].notnull()] 
                        for fan in fan_list.split(',')]))
    authors = list(set([author.strip().lower() for author_list in df['author'][df['author'].notnull()] 
                        for author in author_list.split(',')]))
    authors = [auth for auth in authors if auth != '']
    tags = list(set([author.strip().lower() for author_list in df['all_tags'][df['all_tags'].notnull()] 
                        for author in author_list.split(',')]))
    categories = list(set([cat.strip().lower() for cats in df['categories'][df['categories'].notnull()] 
                        for cat in cats.split(',')]))


    # Get sources & locations
    sources = list(set(df['smk_source'][df['smk_source'].notnull()]))
    primary_source = sorted(sources, key = lambda source: int(source[1]))[0]
    
    sorted_links = []
    primary_link = np.nan
    if 'url' in df.columns:
        # Get list of links sorted by LOCATION_ORDERING
        links_list = [links.split(',') for links in df['url'] 
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

    return {'primary_version': primary_version, 
            'version_nums': version_nums, 
            'primary_source': primary_source, 
            'smk_sources': sources,
            'primary_location': primary_location, 
            'locations': locations, 
            'primary_link': primary_link, 
            'all_links': sorted_links,
            'primary_dtbtype': primary_type, 
            'dtb_types': types,
            'title': title, 
            'fandom': fandoms, 
            'author': authors, 
            'length': length, 
            'is_bold': is_bold,
            'is_coffee': is_cof, 
            'is_complete': is_comp,
            'is_subbed': is_sub, 
            'is_bookmarked': is_bookm, 
            'is_full': is_finished,
            'categories': categories, 
            'cur_chapters': cur_chaps,
            'current_chapter': cur_chap, 
            'all_ratings': all_ratings, 
            'rating': rating,
            'all_tags': tags
            }


def fic_equal(row1, row2) -> bool:
    """
    Takes two fic or series rows from a database (df).
    Compares them to determine if they're the same fic.
    Returns a boolean of whether or not they're equal (bool).
    """
    # Get titles boolean
    title1 = row1.iloc[0]['title'].lower().strip()
    title2 = row2.iloc[0]['title'].lower().strip()
    same_title = title1 == title2
    
    # Get authors boolean (strip, lower, not empty)
    authlist1 = [] if pd.isnull(row1.iloc[0]['author']) else row1.iloc[0]['author'].split(',')
    authlist2 = [] if pd.isnull(row2.iloc[0]['author']) else row2.iloc[0]['author'].split(',')
    author1 = set([auth.lower().strip() for auth in authlist1 if auth != ''])
    author2 = set([auth.lower().strip() for auth in authlist2 if auth != ''])
    
    same_author = (author1 == author2) or (not author1 and not author2)
    absent_author = not author1 or not author2

    # Get locations boolean
    same_location = (row1.iloc[0]['location'] == row2.iloc[0]['location']) or \
        pd.isnull(row1.iloc[0]['location']) or pd.isnull(row2.iloc[0]['location'])
    
    # Get fandoms boolean
    same_fandoms = False
    if not pd.isnull(row1.iloc[0]['fandom']) and not pd.isnull(row2.iloc[0]['fandom']):
        fandom1 = [fan.strip() for fan in row1.iloc[0]['fandom'].split(',')]
        fandom2 = [fan.strip() for fan in row2.iloc[0]['fandom'].split(',')]
        same_fandoms = len(set(fandom1) ^ set(fandom2)) == 0
    
    # print(f'same_title: {same_title}, same_fandoms: {same_fandoms}, same_author: {same_author}, absent_author: {absent_author}')
    # print()
    return same_title and same_fandoms and (same_author or (absent_author and same_location))
        

def id_equal(row1, row2) -> bool:
    """
    Takes two fic or series rows from a database (df).
    Compares them to determine if they're the same fic by id.
    Returns a boolean of whether or not they're equal (bool).
    """
    id_name = 'series_id'
    id1 = row1.iloc[0][id_name]
    id2 = row2.iloc[0][id_name]
    return id1 == id2


def section_fics(df, equal_func) -> list:
    """
    Takes a df of fics (df).
    Sections all fics in given df into a list dfs.
    Returns lists of dfs (list of dfs).
    """
    # Initialize first section
    df_list = [df.iloc[[0]].copy()]

    # Check if row matches existing section
    for ind in range(1, len(df)):
        # Progress check
        if ind % 10 == 0:
            print(f'- {ind} of {len(df)}')
       
        # If row matches existing section, add on; else, add new section
        for i in range(len(df_list)):
            attached = False
            fic1 = df.iloc[[ind]]
            fic2 = df_list[i].iloc[[0]]
            if equal_func(fic1, fic2):
                df_list[i].loc[len(df_list[i])] = fic1.to_dict(orient='records')[0]
                attached = True
                break
        if not attached:
            df_list.append(fic1.copy())
    
    return df_list



if __name__ == "__main__":
    # Read in stage 4 file
    series_df = pd.read_csv('clean_data_4/all_versions_series_url.csv', \
                            encoding='utf-8-sig', index_col=0) \
    
    container_df = pd.DataFrame(columns=['num_appeared',
                                        'primary_version', 'version_nums',
                                        'primary_source', 'smk_sources',  
                                        'primary_location', 'locations',
                                        'primary_link', 'all_links',
                                        'primary_dtbtype', 'dtb_types',
                                        'title', 'fandom', 'author', 'length',
                                        'is_bold', 'is_coffee', 'is_complete',
                                        'is_subbed', 'is_bookmarked', 'is_full',
                                        'categories', 'current_chapter', 'all_tags',
                                        'rating', 'all_ratings', 
                                        ])

    # res = series_df[series_df['title'] == 'bait and switch']
    # res = res[['title', 'author', 'fandom', 'location']]
    # res1 = section_fics(res, fic_equal)
    # print(res1)
    

    # Section & sort fics
    print('- sectioning')
    sections = section_fics(series_df, id_equal)
    
    print('- sorting')
    sorted_sections = sorted(sections, key=lambda sec: sec.iloc[0]['series_id']) 

    
    # Add cleaned rows to container
    for i, sec in enumerate(sorted_sections):
        fic_row = series_row_merge(sec)
        fic_row['num_appeared'] = len(sec)
        container_df.loc[len(container_df.index)] = fic_row
        print(f'  - processed {i+1} of {len(sorted_sections)}')

    # Write to CSV
    outfile_name = 'series_url_test.csv'

    write_df = wrap_df(container_df, SERIES_WRAPS)
    write_df.to_csv(outfile_name, encoding='utf-8-sig')
    print(f'- Wrote to {outfile_name}')
    





    # test_df = file_df[file_df['title'] == "a"]
    # res = section_fics(test_df, fic_equal)
    # print(res)
    # # Get & sort keys (author names)
    # sorted_titles = sorted(list(set([title.lower().strip() for title in authors_df['title']])))

    # # For each key, merge info from all associated rows
    # for title in sorted_titles:
    #     title_df = coffee_df[coffee_df['title'] == title]
    #     fic_rows = section_fics(title_df, fic_equal)
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
    

