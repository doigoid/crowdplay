import os

# path to the root music directory  
MUSIC_DIR = os.path.join(
    os.path.dirname(__file__),
    '..', '..', 'links', 'music')
# path to the root directory of icecast's playlist.txt file resides
ICES_PLAYLIST = os.path.join(
    os.path.dirname(__file__),
    '..', '..', 'links', 'ices2', 'playlist.txt')

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'crowdplay'
