import os, flask, json
from fileinput import close

class AvailableEndpoint:
    def __init__(self, folder_path: str, file_path: str, url: str, filename: str):
        self.folder_path = folder_path
        self.file_path = file_path
        self.url = url
        self.filename = filename
        self.callback_method_name = url + filename
        

    def get_json_callback(self) -> flask.Response:
        os.chdir(self.folder_path)

        with open(self.filename, 'r') as file_object:
            json_string = file_object.read()
            json_o = json.loads(json_string) 
            close()       
            return flask.jsonify(json_o)

    def set_callback_name(self):
        handler = self.get_json_callback
        handler.__func__.__name__ = self.callback_method_name

class MockServer:
    app = flask.Flask(__name__)
    available_endpoints = list()

    def run(self):
        self.load_available_endpoints(True)
        self.set_paths_in_app()
        self.app.run()

    def load_available_endpoints(self, is_first_call = False):
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
                    self.load_available_endpoints()            
                    os.chdir(current_path)

                except:
                    is_json_file = fd.endswith(".json")
                    is_html_file = fd.endswith(".html")

                    if is_json_file:
                        folder_path = os.getcwd()
                        file_path =  "{0}/{1}".format(folder_path.split("/mocks")[1], fd)
                        route_path = file_path.replace(".json", "/")
                        available_endpoint = AvailableEndpoint(
                            folder_path=folder_path,
                            file_path=file_path,
                            url=route_path,
                            filename=fd)
                        
                        self.available_endpoints.append(available_endpoint)

                    elif is_html_file:
                        pass

    def set_paths_in_app(self):
        for available_endpoint in self.available_endpoints:
            available_endpoint: AvailableEndpoint
            available_endpoint.set_callback_name()

            self.app.add_url_rule(
                available_endpoint.url, 
                view_func=available_endpoint.get_json_callback)
