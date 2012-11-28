#include current directory dynamically
import os, sys
workspace_dir = os.path.dirname(os.path.abspath(__file__))
if workspace_dir not in sys.path:
    sys.path.append(workspace_dir)


#Import PyMapper
import pymapper
#Import Sub Application Url Patterns defined for each view
from articles import urls as articles
from blog import urls as blog


class index:
    """"
    Index url dispatcher defined in url patterns
    """""
    def GET(self):
        return "Welcome to pymapper"


#Defiine URL Patterns
url_patterns = (
    '/articles', articles.url_patterns,
    '/blog', blog.url_patterns,
    '/', index
)

#Start a pymapper application instance.
app = pymapper.Application(url_patterns)

#To include the pymapper just include the following code
# in your apache conf or nginx.conf
application = app.startWSGI()