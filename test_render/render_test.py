import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options
define("port",default=8001,help="run on the given port",type=int)

class BookHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('book.html',title="Home Page",header="Books that are great",books=["Learning Python","Programming Collective Intelligence","Restful Web Services"])


application = tornado.web.Application(handlers=[
    (r'/book',BookHandler)],
    template_path=os.path.join(os.path.dirname(__file__),"templates")
)
          

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start() 
