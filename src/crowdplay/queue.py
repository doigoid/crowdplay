import os
import sys
import random
from datetime import datetime

import pymongo
from pymongo import Connection
from pymongo.objectid import ObjectId

import conf
import catalog

conn = Connection(conf.MONGODB_HOST, conf.MONGODB_PORT)
db = conn[conf.MONGODB_DB]
collection = db['playqueue'] 

track_count = catalog.collection.find().count()

def get_playlist_queue():

    playlist_queue = collection.find(sort=[
        ('points', pymongo.DESCENDING),
        ('created', pymongo.ASCENDING),])

    tracks = []
    for q in playlist_queue:
        track = catalog.collection.find_one(
            {'_id':ObjectId(q['track_id'])})
        track['points'] = q['points']
        tracks.append(track)

    return tracks
    

def queue_track(track_id, vote=1):

    vote = int(vote)
    if vote == 0:
        vote = -1
    
    # first verify the track_id isn't fudged
    if not catalog.collection.find_one({'_id':ObjectId(track_id)}):
        return False

    if collection.find_one({'track_id': track_id}):
        collection.update({'track_id': track_id},
                          {'$inc' : { 'points': vote }})
    else:
        collection.insert({'track_id': track_id,
                           'created': datetime.now(),
                           'points': 1})
    return True

def next_song():

    next_song = collection.find(sort=[
        ('points', pymongo.DESCENDING),
        ('created', pymongo.ASCENDING),],
                    limit=1)
    if next_song.count() > 0:
        next_song = next_song[0]
        print os.path.abspath(
            os.path.join(
                conf.MUSIC_DIR,
                str(catalog.collection.find_one(
                    {'_id':ObjectId(next_song['track_id'])})['path'])))
    
        collection.remove({'track_id':next_song['track_id']})
        
    else:
        
        print os.path.abspath(
            os.path.join(
                conf.MUSIC_DIR,
                str(catalog.collection.find().\
                    limit(-1).skip(random.randint(0,track_count)).\
                    next()['path'])))
    
    
