### v8: The Idea Update (first reckoning w/ web scraping)
## Summary
- Ultimately, this project is given a file of URLs, then returns an array of ArchiveFic objects (one object to every AO3 URL given)
- Files:
- main.py is where this url file -> array of ArchiveFic objects is run
- Fic.py is where ArchiveFic is defined, has THREE main dictionaries with all fic data: metaInfo{}, tags{}, and stats{}
- GreaterMethods.py is where all the three methods that return one of the three main ArchiveFic dictionaries are defined
- helperMethods.py defines misc help methods to be used anywhere
- getMetaInfoMethods.py is where all the methods to get each individual piece of data for metaInfo{} (ex. Title, fandoms, etc.) are defined
- other two getMethods.py are pretty much the same
- urls.txt is the text file that contains all the URLs to be turned into an array of ArchiveFic objects

## Updating ‘update’ System
- Put TXT file of urls into ‘update’ folder, rename it to ‘input.txt’
- run ‘update.py’ - this will parsed AO3 urls in ‘input.txt’, get their data, saved it to ‘output.csv’ or ‘runoff.txt’
- Get output from ‘output.csv’


## TO DO
- Finish all methods
- Test connections file
- Grab all data from my favorites list

## Testing Stuff
- https://archiveofourown.org/works/13273611/chapters/30371190
- https://archiveofourown.org/works/20564600
- https://archiveofourown.org/works/12292116/chapters/27943080
- https://archiveofourown.org/works/32361358/chapters/80227150
- https://archiveofourown.org/works/36143854
- https://www.fanfiction.net/s/13789183/1/The-Self-Made-Man

C## ool Things to Remember
- csv Writer 
