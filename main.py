import yaml
from swagger_ui import api_doc
from flask import Flask, redirect
from os import listdir

app = Flask(__name__)

api_doc(app, config_path='./doc/build.yaml', url_prefix='/doc', title='API doc')


PATH = './doc'


def get_paths(directory):

    paths_declaration_files = listdir(directory)
    paths_and_methods = {}

    for path_file in paths_declaration_files:
        with open(directory + '/' + path_file) as path_file_text:
            serialized_path_declaration = yaml.safe_load(path_file_text)
            path_url = list(
                serialized_path_declaration
            )[0]
            serialized_methods_declaration = serialized_path_declaration[path_url]
            if path_url in paths_and_methods:
                for method in serialized_methods_declaration:
                    paths_and_methods[path_url][method] = serialized_methods_declaration[method]
            else:
                paths_and_methods[path_url] = serialized_methods_declaration

    return paths_and_methods


def get_components(directory):
    components_declaration_files = listdir(directory)
    components = {}

    for component_file in components_declaration_files:
        with open(directory + '/' + component_file) as component_file_text:
            serialized_component_declaration = yaml.safe_load(component_file_text)

            components.update(serialized_component_declaration )

    return {'schemas': components}


def get_security_schemes(file_path):
    with open(file_path) as security_schemes_file:
        return yaml.safe_load(security_schemes_file)


def build_doc():
    path = './doc'
    doc_structure = listdir(path)
    if 'frame.yaml' not in doc_structure:
        raise Exception('frame.yaml file does not exist!')
    if 'paths' not in doc_structure:
        raise Exception('paths directory does not exist!')
    # append other exception

    paths_and_methods = get_paths(path + '/paths')
    components = get_components(path + '/components/schemas')
    security_schemes = get_security_schemes(path + '/components/securitySchemas.yaml')

    with open(path + '/frame.yaml') as frame_text:
        serialized_frame = yaml.safe_load(frame_text)

        serialized_frame['paths'] = paths_and_methods
        serialized_frame['components'] = components
        serialized_frame['components']['securitySchemes'] = security_schemes

        with open(path + '/build.yaml', 'w') as build_file:
            build_file.write(yaml.dump(serialized_frame))


@app.route('/')
def main():
    build_doc()
    return redirect("/doc", code=302)


if __name__ == '__main__':
    app.run(debug=True)
    # build_doc()
