# Fix Plex Posters and Artwork from IMDb

## How to Use
```linux
./fixPlexPostersAndArt.py Movie\ Title\ to\ Fix
```

This python script was written to fix an issue I was having with my plex server running on debian linux.

For whatever reason, all my posters and artwork for every single movie and tv show that I had in my plex library just vanished. 
I tried to get help on the plex forums, to no avail.

I decided to try to find the missing artwork myself. After some searching, I was able to find all images for the posters and artwork 
in the Metadata directory. There was also a few directories for agents and Info.xml files, which I decided to parse. 

Next, I found the tables in the plex database schema that needed to be updated in order to point to the correct images.

This script is the resulting product. It restored all my posters and artwork from IMDB. I'm still not sure what happened. 
However, if you are having the same issue, feel free to use the script!


To fix the entire plex database, simply run the script: fixPlexPostersAndArt.py

To search for specific media to fix, run the script with a search parameter: fixPlexPostersAndArt.py deadpool\ 2

- Remember to change the dbFile variable in the script to your plex database path and file name
- Remember to change the mdPath variable in the script to your plex metadata path and file name
