#Dependency on types to determine instance types
import types

def generate_mappings(tup_data, arr_map, n_url_path=''):
    """"
    This function stores url path & url dispatcher in an array.
    Will examine if there is another tuple defined and will go
    recursive until no other tuples are found.
    """""
    for u, inst in zip(tup_data, tup_data):
        n_path = n_url_path + u
        if isinstance(inst, tuple):
            n_t = iter(inst)
            generate_mappings(n_t, arr_map, n_path)
        arr_map.append((n_path,inst))


class url_mapper:
    """"
    Url mapper resolver: will store generated mappings
    from tuple. Also it has a match_with method that
    contains the dispatcher if there is a match with url/the path_info
    """""
    def __init__(self, tuple_data):
        self.stored_mappings = []
        _iter_tuple = iter(tuple_data)
        generate_mappings(_iter_tuple, self.stored_mappings)
    def match_with(self, path_info):
        for url, dispatcher in self.stored_mappings:
            if isinstance(dispatcher, types.ClassType):
                if url == path_info:
                    return dispatcher
        return False


def ResponseHandler(request, tup_data):
    """"
    Response handler will pass tuple containing url path & dispatcher
    Will get a match callback function from the main url mapper
    and will display the result if there is a match
    """""
    path_info = request.path_info
    _url_mapper = url_mapper(tup_data)
    #get the callback if there is a match from the url mapper
    callback = _url_mapper.match_with(path_info)

    #You can set the response output in any format, it can be
    #a list, a tuple, dictionary or wathever you want.
    response = {}
    if callback:
        #For the callback I specified the GET method to hold
        #data for the content & headers
        response['content'] = callback().GET()
        response['headers'] = "class headers"
        response['status_code'] = "200 OK"
        return response

    response['content'] = "not found"
    response['headers'] = "class headers"
    response['status_code'] = "200 OK"
    return response


class RequestHandler:
    """"
    Request handler will be handling
    environ variables as well as sending &
    receiving POST/GET data
    """""
    def __init__(self, environ):
        self.environ = environ
        #For the moment we just need the path_info variable
        #But we can also add class attributes from path info as we want
        self.path_info = self.environ.get('PATH_INFO')


class Application:
    """"
    Main caller will display
    data from the wsgi response
    """""
    def __init__(self, urls):
        self.urls = urls
    def startWSGI(self):
        try:
            return self.WSGIHandler(self.urls)
        except Exception as e:
            return str(e)
    class WSGIHandler:
        def __init__(self, urls):
            self.urls = urls
        #Main Wsgi Caller
        def __call__(self, environ, start_response):
            try:
                #Request handler will send envion Variables to response
                requestHandler = RequestHandler(environ)
                #Response handler will be retrieving data
                #according to url match
                response = ResponseHandler(requestHandler, self.urls)
                #Properly display content, status & headers.
                output = response['content']
                status = "200 OK"
                response_headers = [('Content-type', 'text/plain')]
                start_response(status, response_headers)
                return [output]
            #Return exception
            except Exception as e:
                output = str(e)
                status = "200 OK"
                response_headers = [('Content-type', 'text/plain')]
                start_response(status, response_headers)
                return [output]
