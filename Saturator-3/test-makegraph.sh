# test for xen_4_1_2 @ 192.168.11.4
mongo xen_4_1_2 --host 192.168.11.4 < test.js 
mongo xen_4_1_2 --host 192.168.11.4 < test.js > dump
echo "digraph {" > testgraph.dot
echo "layout = "fdp"" >> testgraph.dot
./graphviz-1.pl dump > link1
python 1.py dump xen_4_1_2 > link2
cat link1 >> testgraph.dot
cat link2 >> testgraph.dot
echo "}" >> testgraph.dot
dot -Tpng testgraph.dot -o 1.png 
eog 1.png 

# real0m26.554s
# user0m3.598s
# sys0m0.207s
