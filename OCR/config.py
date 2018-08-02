#! /usr/bin/env python3

import yaml

def get(key=None):
    with open("config.yaml", 'r') as stream:
        try:
            if key is None:
                return yaml.load(stream)
            else:
                return yaml.load(stream)[key]           
        except yaml.YAMLError as exc:
            print(exc)
            return None
        
if __name__ == "__main__":
    from sys import argv
    try:
        print(get(argv[1]))
    except IndexError:
        print(get())