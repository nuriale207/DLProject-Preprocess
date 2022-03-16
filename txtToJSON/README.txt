1. Data cleaning:

1.1 Vamos a unir todos los ficheros en un solo .txt gigante. cat $(find ./Annotated/ -name "*.txt" | sort ) > todo_txt.txt
1.2 Vamos a eliminar palabras como "Background,results" y de ese estilo. Para ello nos aseguramos que sean palabras que estan pracitcamente solas en su lineaante de ponernos a eliminar. 
el txt sera rescrito, no se crea un fichero nuevo.
$ python quitar_palabras.py --txt ../todo_txt.txt 
1.3 Se ha asumido que algunos titulos de las secciones van al final de cada clase.

2. Data formatting:

2.1 Ahora es necesario crear un .json que contenga la frase y la anotacion de las entidades.
Para ello se ha creado el script add_entities.py, que prepara un .json
$  python add_entities.py -h 
    optional arguments:
  -h, --help            show this help message and exit
  --txt ORIGEN_TXT [ORIGEN_TXT ...]
                        Path no the .txt file with the words.
  --json DEST_JSON [DEST_JSON ...]
                        Path to the JSON output

$ python add_entities.py --txt ../todo_txt.txt --json all_data.json         

2.2 Crear el fichero de tipos, ya que para SpERT sepa que tipos de datos y entidades hay, hay que definirlos, por suerte, podemos emplear el que tenemos.
$ python create_types.py --json ./all_data.json --d dian_types.json  

2.3 Ya que SpERT requiere contener relaciones, aun siendo vacias por cada token, los anadimos del mismo modo
$ python add_empy_relations.py --json ./all_data.json --d all_train_data.json 