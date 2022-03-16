import argparse
import json
import os
from sklearn.model_selection import train_test_split



def create_arguments():
    parser = argparse.ArgumentParser(
        description='This runnable extracts the text, entities and relations of the given JSON file.')

    parser.add_argument('--file', dest='orig_file', nargs='+',
                        help='Path to the file to convert.')
    parser.add_argument('--dest_dir', dest='dest_dir', nargs='+',
                        help='Path to the directory to save the txt files.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = create_arguments()
    orig_dir=args.orig_file[0]
    dest_dir=args.dest_dir[0]

    # Opening JSON file
    f = open(orig_dir)

    # returns JSON object as
    # a dictionary
    fileJson = json.load(f)

    allTokens=[]
    allTokensEntities=" "

    allRelations=""
    for file in fileJson:
        tokens=file["tokens"]

        entities=file["entities"]

        relations=file["relations"]

        tokens_entities=[[] for _ in tokens]
        i=0
        for entity in entities:
            start=entity["start"]
            end=entity["end"]
            name = entity["type"]
            for j in range(start,end):
                tokens_entities[j].append(name)


            # tokens.insert(start+i,beginTag)
            # tokens.insert(end+1+i,endTag)
            i+=1
        tokens_entities_string=""
        i=0
        for token in tokens:
            tokens_entities_string+=token+": "+" ,".join(tokens_entities[i])+"\n"
            i+=1

        i=0
        relationsSt=""
        for relation in relations:
            start = relation["head"]
            end = relation["tail"]
            name = relation["type"]
            entity1=entities[start]["type"]
            entity2=entities[end]["type"]

            start1 = entities[start]["start"]
            end1 = entities[start]["end"]

            start2 = entities[end]["start"]
            end2 = entities[end]["end"]

            relationsSt+= entity1+" "+name+" "+entity2+"\t"
            relationsSt+= tokens[start1]+" "+tokens[end1]+" "+name+" "+ tokens[start2]+" "+tokens[end2]+"\n"
            i += 1
        allTokens.extend(tokens)
        allTokensEntities+=tokens_entities_string
        allRelations+=relationsSt

    print(allTokensEntities)
    # print(allTokens)
    text=" "
    text=text.join(allTokens)
    name=orig_dir.split("/")[-1]
    name=name.split(".")[0]
    file = open(dest_dir + str(name) + "_tokens_entities.txt", 'a')
    file.write(allTokensEntities)
    file.close()

    file2 = open(dest_dir + str(name) + "_tokens.txt", 'a')
    file2.write(" ".join(allTokens))
    file2.close()

    file3 = open(dest_dir + str(name) + "_relations.txt", 'a')
    file3.write(allRelations)
    file3.close()
