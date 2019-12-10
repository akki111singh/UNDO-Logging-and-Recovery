#!/bin/bash
argc="$#"
if [ $argc -eq 1 ]
then
	python3 20171210_2.py $1 
elif [ $argc -eq 2 ]
then
		python3 20171210_1.py $1 $2
else
	echo "Error: Enter filename and x as argument for UNDO Logging and only Filename for Undo recovery "
fi
