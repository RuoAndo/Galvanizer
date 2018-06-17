python ex-list.py xen414 libxl_list_cpupool 6 > tmp
python 1.py tmp > tmp2
./drem.pl tmp2 > tmp2-drem
dot -Tpng tmp2-drem -o tmp2.png
eog tmp2.png
#rm -rf tmp2-drem
