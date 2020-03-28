# Fix Plex Posters and Artwork from IMDb

### How to Use
```
./fixPlexPostersAndArt.py Movie\ Title\ to\ Fix
```

To fix the entire plex database, simply run the script without parameters:
```
fixPlexPostersAndArt.py
```

### Example
```
root@plexserver:/mnt/media/new_movies# ~/scripts/fixPlexPostersAndArt.py Bad\ Boys
Title | Type: Bad Boys for Life | 1 :
 - Directories:
   - Parent Directory:    /mnt/media/Plex Media Server/Metadata/Movies/5/
    - Hash Directory:     /mnt/media/Plex Media Server/Metadata/Movies/5/b03bf02a1dd7de68074c45e76f0f92e24d432c9.bundle/
     - Agent Directory:   /mnt/media/Plex Media Server/Metadata/Movies/5/b03bf02a1dd7de68074c45e76f0f92e24d432c9.bundle/Contents/com.plexapp.agents.imdb/
      - Info.xml:         /mnt/media/Plex Media Server/Metadata/Movies/5/b03bf02a1dd7de68074c45e76f0f92e24d432c9.bundle/Contents/com.plexapp.agents.imdb/Info.xml
     - Uploads Directory: /mnt/media/Plex Media Server/Metadata/Movies/5/b03bf02a1dd7de68074c45e76f0f92e24d432c9.bundle/Uploads/
 - Poster:
  - Checking database for poster:
    - Updating poster in database...
  - Checking Uploads dir for poster:
    - Downloading poster:  http://image.tmdb.org/t/p/original/y95lQLnuNKdPAzw9F9Ab8kJ80c3.jpg
 - Art:
  - Checking database for art:
    - Updating art in database...
  - Checking Uploads dir for art:
    - Downloading art:  http://image.tmdb.org/t/p/original/4WnIfKWV962xYjV1dGxDXi0onvK.jpg

---------------------------

Successfully parsed 1 of 1
```

### Important
- Remember to change the dbFile variable in the script to your plex database path and file name
- Remember to change the mdPath variable in the script to your plex metadata path and file name

### Back Story
This python script was written to fix an issue I was having with my plex server running on debian linux.

For whatever reason, all my posters and artwork for every single movie and tv show that I had in my plex library just vanished. 
I tried to get help on the plex forums, to no avail.

I decided to try to find the missing artwork myself. After some searching, I was able to find all images for the posters and artwork 
in the Metadata directory. There was also a few directories for agents and Info.xml files, which I decided to parse. 

Next, I found the tables in the plex database schema that needed to be updated in order to point to the correct images.

This script is the resulting product. It restored all my posters and artwork from IMDB. I'm still not sure what happened. 
However, if you are having the same issue, feel free to use the script!
