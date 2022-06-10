import os, flask, json
from fileinput import close

class MockServer:
    app = flask.Flask(__name__)

    def run(self):
        self.set_mock_path()

        print("\n ---------- AVAILABLE ENDPOINTS ---------- \n")
        self.get_path()
        print("\n ------------------------------------------\n")

        self.app.run()

    def set_mock_path(self):
        os.chdir('mocks')
 
    def get_path(self):
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
                    self.get_path()            
                    os.chdir(current_path)

                except:
                    is_json_file = fd.endswith(".json")
                    is_html_file = fd.endswith(".html")

                    if is_json_file:
                        folder_path = os.getcwd()
                        file_path =  "{0}/{1}".format(folder_path.split("/mocks")[1], fd)
                        route_path = file_path.replace(".json", "/")
                        print(route_path)
                        callback = lambda : self.get_json_callback(folder_path, fd)
                        callback.__name__ = route_path + fd
                        self.app.add_url_rule(route_path, view_func=callback)

                    elif is_html_file:
                        pass

    def get_json_callback(self, fullpath, filename) -> flask.Response:
        os.chdir(fullpath)
        print(fullpath)
        print(filename)

        with open(filename, 'r') as file_object:
            json_string = file_object.read()
            json_o = json.loads(json_string) 
            close()       
            return flask.jsonify(json_o)
