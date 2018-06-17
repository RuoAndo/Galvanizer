#python definition.py list-definition-$currentdir4 $currentdir4
#python callchain.py list-callchain-$currentdir4 $currentdir4
#python ex.py $currentdir4

python dropdb.py linux405
python createdb.py linux405
python create_definition.py linux405
python create_callchain.py linux405
python definition.py list-callchain-linux405 linux405
python callchain.py list-callchain-linux405 linux405
python ex.py linux49

