import argparse
import json
import re


def create_arguments():
    parser = argparse.ArgumentParser(
        description='Limpiar el texto de palabras inutiles.')

    parser.add_argument('--txt', dest='origen_txt', nargs='+',
                        help='Path no the .txt file with useless words.')
    args = parser.parse_args()
    return args



def clean_text(origen):
    with open(origen,"r+") as f:
        new_f = f.readlines()
        f.seek(0)
        print(new_f)
        for line in new_f:
            print(line)
            if len(line.split()) > 3:
                f.write(line)
        f.truncate()
           

if __name__ == '__main__':
    args = create_arguments()
    clean_text(args.origen_txt[0])
