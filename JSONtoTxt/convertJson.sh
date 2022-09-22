#!/bin/bash
for FILE in ../EjemplosAnalisisMimic/*.json;
do
	python jsonToTxt.py --file ../EjemplosAnalisisMimic/$FILE --dest ../EjemplosAnalisisMimic/;
done