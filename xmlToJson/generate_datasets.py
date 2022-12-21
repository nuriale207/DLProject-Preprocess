import argparse
import json
import os

from sklearn.model_selection import train_test_split

from XmlFile import XmlFile


def create_arguments():
    parser = argparse.ArgumentParser(
        description='This runnable converts the XML files contained in train test dev folders in the mentioned directory into train, '
                    'test, dev and train_dev JSON divisions needed by the SpERT model.')

    parser.add_argument('--dir', dest='orig_dir', nargs='+',
                        help='Path to the directory that has the XML files inside train test dev folders.')
    parser.add_argument('--dest', dest='dest_dir', nargs='+',
                        help='Path to the directory to save the JSON output.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = create_arguments()
    orig_dir = args.orig_dir[0]
    dest_dir = args.dest_dir[0]

    train_dir=orig_dir+"/train"
    test_dir=orig_dir+"/test"
    dev_dir=orig_dir+"/dev"

    #Train
    trainFile = []
    entityTypes = set()
    relationTypes = set()
    for filename in os.listdir(train_dir):
        f = os.path.join(orig_dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            xml = XmlFile(f, filename)
            jsonInfo = xml.xmlToJson()
            trainFile = trainFile + jsonInfo
            entityTypes.update(xml.getEntityTypes())
            relationTypes.update(xml.getRelationTypes())

    train_json = json.dumps(trainFile)

    # Dev
    devFile = []
    for filename in os.listdir(dev_dir):
        f = os.path.join(orig_dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            xml = XmlFile(f, filename)
            jsonInfo = xml.xmlToJson()
            devFile = devFile + jsonInfo
            entityTypes.update(xml.getEntityTypes())
            relationTypes.update(xml.getRelationTypes())

    dev_json = json.dumps(devFile)

    # Test
    testFile = []
    for filename in os.listdir(test_dir):
        f = os.path.join(orig_dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            xml = XmlFile(f, filename)
            jsonInfo = xml.xmlToJson()
            testFile = testFile + jsonInfo
            entityTypes.update(xml.getEntityTypes())
            relationTypes.update(xml.getRelationTypes())

    test_json = json.dumps(testFile)


    train_dev_json=json.dumps(trainFile+devFile)
    def generate_types_file(entityTypes, relationTypes):
        entities = {}
        relations = {}

        for entity in entityTypes:
            entities[entity] = {"short": entity, "verbose": entity}

        for relation in relationTypes:
            relations[relation] = {"short": relation, "verbose": relation, "symmetric": False}
        types_json = {"entities": entities, "relations": relations}
        return types_json


    types_json = json.dumps(generate_types_file(entityTypes, relationTypes))
    # Using a JSON string
    with open(dest_dir + '/train.json', 'w') as outfile:
        outfile.write(train_json)

    with open(dest_dir + '/test.json', 'w') as outfile:
        outfile.write(test_json)

    with open(dest_dir + '/dev.json', 'w') as outfile:
        outfile.write(dev_json)

    with open(dest_dir + '/train_dev.json', 'w') as outfile:
        outfile.write(train_dev_json)

    with open(dest_dir + '/types.json', 'w') as outfile:
        outfile.write(types_json)