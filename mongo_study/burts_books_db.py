import os.path
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.locale
import pymongo

from tornado.options import define,options

define("port",default=8000,help="run on the given port",type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r"/",MainHandler),
            (r"/recommended/",RecommendedHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            ui_modules={"Book":BookModule},
            debug=True,
        )
        conn = pymongo.Connection("localhost",27017)
        self.db = conn["bookstopre"]
        tornado.web.Application.__init__(self,handlers,**settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",page_title="Burt's Books | Home",header_text="WelCome to Burt's Books!",)


class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.books
        books = coll.find()
        self.render("recommended.html",page_title="Burt's Books | Recommended Reading",
                     header_text="Recommended Reading",books = books)

class BookModule(tornado.web.UIModule):
    def render(self,book):
        return self.render_string(
            "modules/book.html",
            book=book,
        )
    def css_files(self):
        return "/static/css/recommended.css"

    def javascipt_file(self):
        return "/static/js/recommended.js"


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

