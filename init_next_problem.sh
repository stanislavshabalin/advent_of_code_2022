mkdir -p ./code
touch ./code/__init__.py

LAST_PROBLEM_FILENAME=$(
	find ./code -maxdepth 1 -name "*.py" -print \
		| grep -v "__init__" \
		| sort \
		| tail -n1
)

if test -z $LAST_PROBLEM_FILENAME; then
	LAST_PROBLEM=0
else
	LAST_PROBLEM=$(basename $LAST_PROBLEM_FILENAME | cut -d '_' -f 1)
fi

NEXT_PROBLEM=$(printf "%02d" $((LAST_PROBLEM + 1)))

touch ./code/"$NEXT_PROBLEM"_1.txt
touch ./code/"$NEXT_PROBLEM"_2.txt

cat code_template.py | sed s/"%%"/"$NEXT_PROBLEM"/g > ./code/"$NEXT_PROBLEM"_1.py
# each problem consists of two parts
cp ./code/"$NEXT_PROBLEM"_1.py ./code/"$NEXT_PROBLEM"_2.py
