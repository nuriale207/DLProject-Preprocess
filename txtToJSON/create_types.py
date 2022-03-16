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


def create_types(origen_json, destination):
    entities_types = {}
    relations_type = {}
    with open(origen_json) as f:
        json_txt = json.load(f)

        for idx, json_l in enumerate(json_txt):
            print(json_l)
            if "entities" in json_l.keys():
                for entities in json_l["entities"]:
                    descripcion = {}
                    if entities["type"] not in entities_types.keys():
                        print(entities["type"])
                        descripcion = {
                            "short": entities["type"], "verbose": entities["type"]}
                        entities_types[entities["type"]] = descripcion
                    
            if "relations" in json_l.keys():
                for relations in json_l["relations"]:

                    descripcion = {}
                    if relations["type"] not in relations_type.keys():
                        descripcion = {
                            "short": entities["type"], "verbose": entities["type"], "symmetric": False}
                        relations_type[relations["type"]]=descripcion

    json_total = {"entities":entities_types,"relations":relations_type}
    with open(destination, 'w') as outfile:
            json.dump(json_total, outfile)
if __name__ == '__main__':
    args = create_arguments()
    create_types(args.origen_json[0], args.destination[0])
