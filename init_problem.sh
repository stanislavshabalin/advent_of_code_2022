touch ./code/$1.txt
cat code_template.py | sed s/"%%"/"$1"/g > ./code/$1.py
