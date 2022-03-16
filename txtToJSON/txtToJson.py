import argparse
import json as jsonss
import re


def create_arguments():
    parser = argparse.ArgumentParser(
        description='Turns a txt into json needed by the SpERT model..')

    parser.add_argument('--txt', dest='orig_txt', nargs='+',
                        help='Path no the .txt file with the words.')
    parser.add_argument('--json', dest='dest_json', nargs='+',
                        help='Path to the JSON output')
    parser.add_argument('--r', dest='reduce',
                        help='If applied the file will be divided in 12 word sentences')
    args = parser.parse_args()
    return args



def add_info(origen,destination,reduce):
    json = {}
    entitie = {}
    json_all = []
    with open(origen) as file:
        for line in file:
            entites = []
            entitie = {}
            json = {}
            # Por cada linea del texto
            words = remove_html_tags(line)
            if(reduce!=None):
                tokens=words.split()
                i_prev=0
                i=12
                json = {}
                while (i<len(tokens)):
                    json = {}
                    line_tokens=tokens[i_prev:i]
                    json['tokens']=line_tokens
                    i_prev=i
                    i+=12
                    line=""
                    line=line.join(line_tokens)
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
                    json_all.append(json)
            else:
                json['tokens'] = words.split()

                if re.search(r'(<[a-z]*>)',line):
                    # Si existe almenos una anotacion.
                    for idx_word,word in enumerate(line.split()):
                        # Recorremos las palabras de la frase.
                        if re.search(r'(<[a-z][a-z][a-z]>)',word):
                            # Si la palabra contiene un tag.
                            entitie = {}
                            c = re.compile(r'(<[a-z][a-z][a-z]>)')
                            tag = c.findall(word)[0][1:-1] # Asi obtenemos el nombre de la tag.
                            n_words = count_words(idx_word,tag,line.split()) # Sabemos la longitud.
                            if n_words != None:
                                entitie['start'] = idx_word
                                entitie['end'] = n_words
                                entitie['type'] = tag
                                entites.append(entitie)
                                json['entities'] = entites
                else:
                    json['entities'] = []
                json_all.append(json)

    with open(destination, 'w') as outfile:
        jsonss.dump(json_all, outfile)
        

                
def count_words(idx_word,tag,words):
    aux = idx_word
    for i in range(idx_word,len(words)):
        print(tag)
        if "</"+tag+">" in words[i]: # Para que elimine la ocurrencia.
            return aux+1
        else:
            aux = aux+1
    print("No se ha encontrado lo cerrado, da fallo.")
                
           
def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


if __name__ == '__main__':
    args = create_arguments()
    add_info(args.origen_txt[0],args.dest_json[0],args.reduce[0])
