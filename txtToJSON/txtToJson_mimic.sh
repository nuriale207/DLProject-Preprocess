#!/bin/bash
for FILE in *.txt;
do 
	python ../txtToJson.py --txt $FILE --json ${FILE%.*}.json --r reduce;
done
