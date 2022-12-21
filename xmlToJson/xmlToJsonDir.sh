#!/bin/bash
echo $1
for FILE in $1/*.xml;
do
	echo ${FILE};
	python3 xmlToJson.py --file $FILE --dest $2
done