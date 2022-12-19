import argparse
import json
import os

from sklearn.model_selection import train_test_split

from XmlFile import XmlFile


def create_arguments():
    parser = argparse.ArgumentParser(
        description='This runnable converts a XML file into JSON format needed by the SpERT model.')

    parser.add_argument('--file', dest='orig_dir', nargs='+',
                        help='Path to the XML file.')
    parser.add_argument('--dest', dest='dest_dir', nargs='+',
                        help='Path to the directory to save the JSON output.')

    parser.add_argument('--types',action="store_true", default=False,
                        help='Whether to generate or not a file containing the entities and relations of the file.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    def generate_types_file(entityTypes, relationTypes):
        entities = {}
        relations = {}

        for entity in entityTypes:
            entities[entity] = {"short": entity, "verbose": entity}

        for relation in relationTypes:
            relations[relation] = {"short": relation, "verbose": relation, "symmetric": False}
        types_json = {"entities": entities, "relations": relations}
        return types_json


    args = create_arguments()
    orig_file=args.orig_dir[0]
    dest_dir=args.dest_dir[0]
    file_name=orig_file.split("/")[-1].split(".")[0]
    xml=XmlFile(orig_file,file_name)
    jsonInfo = xml.xmlToJson()


    jsonInfo=json.dumps(jsonInfo)

    # Using a JSON string
    with open(dest_dir+'/'+file_name+".json", 'w') as outfile:
        outfile.write(jsonInfo)

    if args.types:

        types_json=json.dumps(generate_types_file(xml.getEntityTypes(),xml.getRelationTypes()))
        # Using a JSON string
        with open(dest_dir+'/'+file_name+"_types.json", 'w') as outfile:
            outfile.write(types_json)