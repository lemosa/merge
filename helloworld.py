import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.web

from tornado.options import define,options
define("port",default=8000,help="run on the port",type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting','hello')
        self.write(greeting + " Hello, world")
    def write_error(self,status_code,**kwargs):
        self.write("Gosh darnit,user! You cause a %d error." % status_code)

application = tornado.web.Application([
    (r"/", IndexHandler),
])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
