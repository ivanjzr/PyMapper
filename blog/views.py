
class index:
    """"
    Sub Application Index url dispatcher defined in url patterns
    """""
    def GET(self):
        return "Blog Index"



class section:
    """"
    Sub Application Blog url dispatcher defined in url patterns
    """""
    def GET(self):
        return "Blog Section"