#!/usr/bin/python

import os
import sys
import sqlite3
import requests
import xml.etree.ElementTree
from   shutil import copyfile


# Change to your plex database path and file name
dbFile = '/mnt/media/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db'

# Change to your plex metadata path and file name
mdPath = '/mnt/media/Plex Media Server/Metadata/'



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# Downloads a file from the Internet
# param[in] url  - URL of file to download
# param[in] path - Directory to save the file to
#
def downloadFile(url, path):
  if not os.path.isdir(path):
    os.makedirs(path)

  filename = path + url.split('/')[-1]

  r = requests.get(url)
  f = open(filename, 'wb')
  for chunk in r.iter_content(chunk_size=512*1024):
    if chunk:
      f.write(chunk)
  f.close()

  return

db = sqlite3.connect(dbFile)
cur = db.cursor()

# Ensure there are library sections in the database
selectLibrarySectionIds  = '''SELECT id FROM library_sections'''
cur.execute(selectLibrarySectionIds)

rows = cur.fetchall()

if len(rows) == 0:
  print "Error: No library sections found"
  sys.exit(1)

# Check for search passed in search parameters
if len(sys.argv) != 2:
  searchParam = False
else:
  searchParam = True

if searchParam:
  selectPosterSql  = '''SELECT id, title, user_thumb_URL, user_art_url, user_fields, hash, metadata_type FROM metadata_items WHERE title LIKE ? AND library_section_id IN (SELECT id FROM library_sections)'''
  cur.execute(selectPosterSql, ('%'+sys.argv[1]+'%',))
else:
  selectPosterSql  = '''SELECT id, title, user_thumb_URL, user_art_url, user_fields, hash, metadata_type FROM metadata_items WHERE library_section_id IN (SELECT id FROM library_sections)'''
  cur.execute(selectPosterSql)

rows = cur.fetchall()

if len(rows) == 0:
  print 'Error: No media found to fix'
  sys.exit(1)

# Setup various types and agents
mdTypes  = ['', 'Movies/', 'TV Shows/']
mdAgents = ['', 'Contents/com.plexapp.agents.imdb/', 'Contents/com.plexapp.agents.thetvdb/']

# Keep track of porgress
missingAgents   = {}
missingInfoXmls = {}
expCount = 0
actCount = 0

# Parse database query results
for row in rows:
  mdId = row[0]

  mdTitle = row[1]
  if not mdTitle:
    continue

  mdType = row[6]
  if not mdType or mdType < 0 or mdType > len(mdTypes):
    continue

  mdHash = row[5]
  if not mdHash:
    continue

  expCount += 1

  mdParentDir  = mdPath + mdTypes[mdType] + mdHash[0] + '/'
  if not os.path.isdir(mdParentDir):
    continue

  mdDir = mdParentDir + row[5][1:] + '.bundle/'
  if not os.path.isdir(mdDir):
    continue

  mdAgentDir = mdDir + mdAgents[mdType]
  if not os.path.isdir(mdAgentDir):
    missingAgents[mdTitle] = mdAgentDir
    continue

  mdInfoXml = mdAgentDir + 'Info.xml'
  if not os.path.exists(mdInfoXml):
    missingInfoXmls[mdTitle] = mdInfoXml
    continue

  mdUploadsDir   = mdDir + 'Uploads/'
  mdUserThumbUrl = row[2]
  mdUserArtUrl   = row[3]
  mdUserFields   = row[4]

  if 'lockedFields=' not in mdUserFields:
    mdUserFields='lockedFields=9'
  else:
    if '9' not in mdUserFields:
      mdUserFields=mdUserFields+'|9' # FIXME need split userFields by '|' and sort in ascending order before saving to db *************

  print 'Title | Type:',           mdTitle, '|' , mdType, ':'
  # TODO: make this a -v option *********************************************************************************
  print ' - Directories:'
  print '   - Parent Directory:   ', mdParentDir
  print '    - Hash Directory:    ', mdDir
  print '     - Agent Directory:  ', mdAgentDir
  print '      - Info.xml:        ', mdInfoXml
  print '     - Uploads Directory:', mdUploadsDir
  # TODO: make this a -v option *********************************************************************************

  actCount += 1
  
  # ---------------------------------------------------------------------------
  # Parse Info.xml
  root = xml.etree.ElementTree.parse(mdInfoXml).getroot()

  for child in root:
    if child.tag == 'posters':
      posters = child
    if child.tag == 'art':
      artwork = child

  if len(posters) > 0:
    posterUrl = posters[0].get('url')
    if posterUrl:
      print ' - Poster:'
      poster = posterUrl.split('/')[-1]

      # Check user_thumb_url in database
      print '  - Checking database for poster:'
      dbUploadPosterPath = 'upload://posters/' + poster
      if mdUserThumbUrl == dbUploadPosterPath:
        print '    - Poster already updated in database; nothing to do'
      else:
        print '    - Updating poster in database...'
        # Update record with correct user_thumb_url
        updatePosterSql  = '''UPDATE metadata_items SET user_thumb_url=?, user_fields=? WHERE id=?'''

        cur.execute(updatePosterSql, (dbUploadPosterPath, mdUserFields, mdId))
        db.commit()

      # Check poster file exists
      print '  - Checking Uploads dir for poster:'
      if not os.path.exists(mdUploadsDir + 'posters/' + poster):
        print '    - Downloading poster: ', posterUrl
        downloadFile(posterUrl, mdUploadsDir + 'posters/')
      else:
        print '    - Poster already exists; nothing to do'

  if len(artwork) > 0:
    artUrl = artwork[0].get('url')
    if artUrl:
      print ' - Art:'
      art = artUrl.split('/')[-1]

      # Check user_art_url in database
      print '  - Checking database for art:'
      dbUploadArtPath = 'upload://art/' + art
      if mdUserArtUrl == dbUploadArtPath:
        print '    - Art already updated in database; nothing to do'
      else:
        print '    - Updating art in database...'
        # Update record with correct user_art_url
        updateArtSql  = '''UPDATE metadata_items SET user_art_url=?, user_fields=? WHERE id=?'''

        cur.execute(updateArtSql, (dbUploadArtPath, mdUserFields, mdId))
        db.commit()

      # Check art file exists
      print '  - Checking Uploads dir for art:'
      if not os.path.exists(mdUploadsDir + 'art/' + art):
        print '    - Downloading art: ', artUrl
        downloadFile(artUrl, mdUploadsDir + 'art/')
      else:
        print '    - Art already exists; nothing to do'

db.close()
  
print '\n---------------------------\n'

print 'Successfully parsed %d of %d' % (actCount, expCount)
if len(missingAgents) > 0:
  print '- Missing agents:', missingAgents
if len(missingInfoXmls) > 0:
  print '- Missing Info.xml files:', missingInfoXmls

print '\n'

