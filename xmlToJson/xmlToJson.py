import argparse
import json
import os

from sklearn.model_selection import train_test_split

from XmlFile import XmlFile


def create_arguments():
    parser = argparse.ArgumentParser(
        description='This runnable converts the XML files in the mentioned directory into train, '
                    'test, dev and train_dev divisions needed by the SpERT model.')

    parser.add_argument('--dir', dest='orig_dir', nargs='+',
                        help='Path to the directory that has the XML files.')
    parser.add_argument('--dest', dest='dest_dir', nargs='+',
                        help='Path to the directory to save the JSON output.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = create_arguments()
    orig_dir=args.orig_dir[0]
    dest_dir=args.dest_dir[0]
    jsonFile=[]
    entityTypes=set()
    relationTypes=set()
    for filename in os.listdir(orig_dir):
        f = os.path.join(orig_dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            xml=XmlFile(f,filename)
            jsonInfo=xml.xmlToJson()
            jsonFile=jsonFile+jsonInfo
            entityTypes.update(xml.getEntityTypes())
            relationTypes.update(xml.getRelationTypes())
        full=json.dumps(jsonFile)

    with open(dest_dir+'/'+filename+'.json', 'w') as outfile:
         outfile.write(full)

    train,test=train_test_split(jsonFile,test_size=0.15,train_size=0.85)
    train,dev=train_test_split(train,test_size=0.176,train_size=0.823)

    jsonFile2=json.dumps(jsonFile)
    train_json=json.dumps(train)
    test_json=json.dumps(test)
    dev_json=json.dumps(dev)
    train_dev_json=json.dumps(train+dev)

    print(entityTypes)
    print(relationTypes)
    def generate_types_file(entityTypes, relationTypes):
        entities={}
        relations={}

        for entity in entityTypes:
            entities[entity]={"short": entity, "verbose": entity}

        for relation in relationTypes:
            relations[relation]= {"short": relation, "verbose": relation, "symmetric": False}
        types_json={"entities":entities, "relations":relations}
        return types_json

    types_json=json.dumps(generate_types_file(entityTypes,relationTypes))
    # Using a JSON string
    with open(dest_dir+'/e3c_train.json', 'w') as outfile:
        outfile.write(train_json)

    with open(dest_dir+'/e3c_test.json', 'w') as outfile:
        outfile.write(test_json)

    with open(dest_dir+'/e3c_dev.json', 'w') as outfile:
        outfile.write(dev_json)

    with open(dest_dir+'/e3c_train_dev.json', 'w') as outfile:
        outfile.write(train_dev_json)


    with open(dest_dir+'/e3c_types.json', 'w') as outfile:
        outfile.write(types_json)
