import argparse

import json



def create_arguments():
    parser = argparse.ArgumentParser(
        description='Print confussion matrix between to JSON files.')

    parser.add_argument('--json', dest='origen_json', nargs='+',
                        help='Path no the .json file')

    parser.add_argument('--d', dest='destination', nargs='+',
                        help='Path to created JSON')
    args = parser.parse_args()
    return args




def create_types(origen_json):
    entities_types = {}
    relations_type = {}
    with open(origen_json) as f:
        json_txt = json.load(f)
        for jsons in json_txt:
            if len(jsons["tokens"]) < 5:
                print("Hay uno muy corto")
 





if __name__ == '__main__':
    args = create_arguments()
    create_types(args.origen_json[0])
