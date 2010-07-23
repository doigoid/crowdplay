import os
import sys

import pymongo
from pymongo import Connection

import conf

from mutagen.easyid3 import EasyID3 as ID3
from mutagen.flac import FLAC
from mutagen import File as OGG

conn = Connection(conf.MONGODB_HOST, conf.MONGODB_PORT)
db = conn[conf.MONGODB_DB]
collection = db['catalog']

# Recursively scans a directory for music files
def music_files(root, abs_root=None):
    if abs_root is None:
        abs_root = root
    for f in os.listdir(root):
        fullpath = os.path.join(root,f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in music_files(fullpath, abs_root):
                # recurse into subdir
                yield x
        else:
            if fullpath[-4:] in ('.mp3','.ogg','flac'):
                yield fullpath[len(abs_root)+1:] 

def music_metadata(file):
    types = {'.mp3':ID3, '.ogg':OGG, 'flac':FLAC}
    try:
        metadata = types[file[-4:]](file)
        data = {}
        for k,v in metadata.iteritems():
            if len(v) > 0:
                data[k] = v[0].strip()
        return data
    except KeyError, e:
        print file[-4:] + ' file extension is not supported.'
    except IOError, e:
        print 'Trouple opening file: ' + file
    except Exception, e:
        print 'No metadata found for ' + file
    return {}

def update_music_catalog(dir=conf.MUSIC_DIR):
    
    tracks = music_files(dir)
    for path in tracks:
        if collection.find_one({'path':path}) is None:
            track = music_metadata(os.path.join(dir,path))
            if track:
                collection.insert({
                    'path':   path,
                    'artist': track.get('artist'),
                    'title':  track.get('title'),
                    'album':  track.get('album'),
                    'date':   track.get('date'),
                    'genre':  track.get('genre'),
                    })

_CACHE = {}

def get_artist_list():
    if 'artist_list' not in _CACHE:
        _CACHE['artist_list'] = {}
        tracks = collection.find(sort=[('artist',pymongo.ASCENDING)])
        for track in tracks:
            if track['artist'] not in _CACHE['artist_list']: 
                _CACHE['artist_list'][track['artist']] = 1
            else:
                _CACHE['artist_list'][track['artist']] += 1
    return _CACHE['artist_list']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        update_music_catalog(sys.argv[1])
    else:
        update_music_catalog()
                


    
