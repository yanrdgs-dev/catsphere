from bottle import template

class Application():
    def __init__(self):
        self.pages = {
            "index": self.index,
        }
    
    def render(self, page):
        content = self.pages.get(page, self.page_not_found)
        return content()
    
    def index(self):
        return template("app/views/html/index")
    
    def page_not_found(self):
        return template("app/views/html/404")