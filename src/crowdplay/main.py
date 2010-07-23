import tornado.httpserver
import tornado.ioloop
import tornado.web

from handlers import MainHandler, QueueHandler

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/queue/(?P<track_id>[\d\w]+)/(?P<vote>[01])", QueueHandler),
])

def start_server(port=8000):
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    start_server()
