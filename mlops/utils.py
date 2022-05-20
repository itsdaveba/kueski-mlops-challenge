import json

def save_dict(d, filepath):
    with open(filepath, 'w') as fp:
        json.dump(d, fp=fp, indent=2)

def load_dict(filepath):
    with open(filepath, 'r') as fp:
        d = json.load(fp)
    return d