import os, flask, json
from fileinput import close

class AvailableEndpoint:
    def __init__(self, dir_path: str, file_path: str, url: str, filename: str):
        self.dir_path = dir_path
        self.file_path = file_path
        self.url = url
        self.filename = filename
        self.__data_callback_name = url + filename

    def data_callback(self) -> flask.Response:
        os.chdir(self.dir_path)

        with open(self.filename, 'r') as file_object:
            json_string = file_object.read()
            json_o = json.loads(json_string) 
            close()       
            return flask.jsonify(json_o)

    def handler_data_callback(self):
        handler = self.data_callback
        handler.__func__.__name__ = self.__data_callback_name

class MockServer:
    app = flask.Flask(__name__)
    available_endpoints = list()

    def run(self):
        self.__load_available_endpoints(True)
        self.__set_main_view()
        self.__set_endpoints()
        self.app.run()

    def __load_available_endpoints(self, is_first_call = False):
        if is_first_call:
            os.chdir('mocks')

        dirs = os.listdir()
        DS_Store_file_name = ".DS_Store"
        contains_DS_Store = dirs.__contains__(DS_Store_file_name)

        if contains_DS_Store:
            dirs.remove(DS_Store_file_name)
        
        dirs_is_not_empty = dirs.__len__() > 0

        if dirs_is_not_empty:
            for fd in dirs:
                try:
                    current_path = os.getcwd()
                    os.chdir(fd)
                    self.__load_available_endpoints()            
                    os.chdir(current_path)

                except:
                    is_json_file = fd.endswith(".json")
                    is_html_file = fd.endswith(".html")
                    
                    folder_path = os.getcwd()
                    file_path =  "{0}/{1}".format(folder_path.split("/mocks")[1], fd)

                    if is_json_file:
                        route_path = file_path.replace(".json", "/")
                        available_endpoint = AvailableEndpoint(
                            dir_path=folder_path,
                            file_path=file_path,
                            url=route_path,
                            filename=fd)
                        
                        self.available_endpoints.append(available_endpoint)

                    elif is_html_file:
                        pass

    def __set_endpoints(self):
        for available_endpoint in self.available_endpoints:
            available_endpoint: AvailableEndpoint
            available_endpoint.handler_data_callback()

            self.app.add_url_rule(
                available_endpoint.url, 
                view_func=available_endpoint.data_callback)

    def __main_view(self):
        return flask.render_template("index.html", available_endpoints=self.available_endpoints)

    def __set_main_view(self):
        self.app.add_url_rule("/", view_func=self.__main_view)
