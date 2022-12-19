import argparse
import json as jsonss
import os
import re
import pandas as pd

def create_arguments():
    parser = argparse.ArgumentParser(
        description='Turns a csv data lake into json needed by the SpERT model..')

    parser.add_argument('--csv', dest='orig_txt', nargs='+',
                        help='Path no the .csv file with the words.')
    parser.add_argument('--json', dest='dest_json', nargs='+',
                        help='Path to the JSON output')
    parser.add_argument('--id', dest='id', nargs='+',
                        help='Name of the document id column')
    parser.add_argument('--text', dest='text', nargs='+',
                        help='Name of the text column')
    # parser.add_argument('--r', dest='reduce',
    #                     help='If applied the file will be divided in 12 word sentences')
    args = parser.parse_args()
    return args

def convert_csv(path, id_col, text_col,destination):
    df=pd.read_csv(path)
    print(df)
    texts=df[text_col]
    ids=df[id_col]
    if not os.path.exists(destination):
        os.makedirs(destination)
    add_info(texts,ids,destination)


def add_info(texts,ids,destination):

    i=0
    for text in texts:
        json = {}
        entitie = {}
        json_all = []
        lines=text.split(".")
        for line in lines:
            entites = []
            entitie = {}
            json = {}
            # Por cada linea del texto
            words = remove_html_tags(line)

            json['tokens'] = words.split()

            if re.search(r'(<[a-z]*>)', line):
                # Si existe almenos una anotacion.
                for idx_word, word in enumerate(line.split()):
                    # Recorremos las palabras de la frase.
                    if re.search(r'(<[a-z][a-z][a-z]>)', word):
                        # Si la palabra contiene un tag.
                        entitie = {}
                        c = re.compile(r'(<[a-z][a-z][a-z]>)')
                        tag = c.findall(word)[0][1:-1]  # Asi obtenemos el nombre de la tag.
                        n_words = count_words(idx_word, tag, line.split())  # Sabemos la longitud.
                        if n_words != None:
                            entitie['start'] = idx_word
                            entitie['end'] = n_words
                            entitie['type'] = tag
                            entites.append(entitie)
                            json['entities'] = entites
            else:
                json['entities'] = []
                json['relations']=[]
            json_all.append(json)

        file_name="/"+ids[i]+".json"
        with open(destination+file_name, 'w') as outfile:
            jsonss.dump(json_all, outfile)
        i+=1

def count_words(idx_word, tag, words):
    aux = idx_word
    for i in range(idx_word, len(words)):
        print(tag)
        if "</" + tag + ">" in words[i]:  # Para que elimine la ocurrencia.
            return aux + 1
        else:
            aux = aux + 1
    print("No se ha encontrado lo cerrado, da fallo.")


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


if __name__ == '__main__':
    args = create_arguments()
    convert_csv(args.orig_txt[0], args.id[0], args.text[0], args.dest_json[0] )
