import os
import tornado.web

import catalog
import queue

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        artists = catalog.get_artist_list()
        playqueue = queue.get_playlist_queue()
        tracks = catalog.collection.find(sort=[('artist',1)])
        self.render('templates/index.html',
                    artists=artists, tracks=tracks, queue=playqueue)
   
class QueueHandler(tornado.web.RequestHandler):
    def get(self, track_id, vote):
        if queue.queue_track(track_id, vote):
            self.redirect('/')
        else:
            raise tornado.web.HTTPError(404)

                
