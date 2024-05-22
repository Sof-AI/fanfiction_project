### Clean Data versions
- clean_data_1: Get raw data from v1-8 documents, lists, and sheet into a spreadsheet/csv format
    - `versionNum_workType_dataType_origin.csv` (ex. `v3_fic_text_categories.csv`)
- clean_data_2: Combine clean_data_1 on version number & type (author_text, fic_url, etc.)
    - `versionNum_workType_dataType.csv` (ex. `v3_fic_text.csv`)
- clean_data_3: Combine clean_data_2 on type w/ all additional cols (smk_source, version, location, etc.)
    - `all_versions_workType_dataType.csv` (ex. `all_versions_fic_text.csv`)
- clean_data_4: Clean clean_data_3, make column names and values consistant across all sheets, all empty cells = data not found (not negative)
    - same naming format as above
-  clean_data_5: De-dup clean_data_4, use python script to format all columns into consistant, script-readable forms
    - `workType_dataType.csv` (ex. `fic_text.csv`)
- clean_data_6: Merge clean_data_5 on work type (aka merge & de-dup the text & url versions of each work type, fill in any missing urls, add primary keys
    - `workType.csv` (ex. `fic.csv`)

- See [FFN Connections diagram](https://www.figma.com/file/BM3RU54zSJn7AzbcFr3WKb/FFNv9-Navigation-Chart?type=whiteboard&node-id=0-1&t=ci0O17LZqOHYLOAM-0) to see end goal for clean_data_6, under 'FFN v9.3 No-SQL UML'





