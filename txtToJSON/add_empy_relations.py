import argparse
import json
import re


def create_arguments():
    parser = argparse.ArgumentParser(
        description='Print confussion matrix between to JSON files.')

    parser.add_argument('--json', dest='origen_json', nargs='+',
                        help='Path no the .json file')

    parser.add_argument('--d', dest='destination', nargs='+',
                        help='Path to created JSON')


    args = parser.parse_args()
    return args


def add_empty_relations(origen_json, destination):

    with open(origen_json) as f:
        json_txt = json.load(f)

        for idx, json_l in enumerate(json_txt):
            if "relations" not in json_l.keys():
                json_txt[idx]["relations"] = []
            if "entities" not in json_l.keys():
                json_txt[idx]["entities"] = []

    with open(destination, 'w') as outfile:
        json.dump(json_txt, outfile)


if __name__ == '__main__':
    args = create_arguments()
    add_empty_relations(args.origen_json[0], args.destination[0])
