import json


def write_json(data, input_path):
    with open(input_path, 'w') as f:
        json.dump(data, f, indent=4)


def read_file(input_path):
    with open(input_path, 'r') as f:
        return f.read()
