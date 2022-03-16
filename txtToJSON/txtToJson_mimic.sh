#!/bin/bash
for FILE in *.txt; 
do 
	python ../quitar_palabras.py --txt $FILE; 
done

for FILE in *.txt;
do 
	python ../add_entities.py --txt $FILE --json ${FILE%.*}.json; 
done
