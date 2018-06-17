# findCaller.py

usage
<pre>
# python findCaller.py xen_test xen/common/radix-tree.c 70
                       [DB name] [file name]            [line number]
</pre>

output
<pre>
# python findCaller.py xen_test xen/common/radix-tree.c 70
[47, 55, 95, 150, 189, 202, 212, 277, 305, 331, 393, 415, 433, 443]

x:[47, 55, 95, 150, 189, 202, 212, 277, 305, 331, 393, 415, 433, 443]
-> 検索しているファイルで、関数が定義されている行番号

ln:70 -> 検索している行番号
y:2
len(x):14
x(y):55 -> 一番近い左隣の行番号

radix_tree_extend:xen/common/radix-tree.c:55 <- 検索した行番号が入っている関数名とファイル名

# python findCaller.py xen_test xen/common/radix-tree.c 105
[47, 55, 95, 150, 189, 202, 212, 277, 305, 331, 393, 415, 433, 443]
x:[47, 55, 95, 150, 189, 202, 212, 277, 305, 331, 393, 415, 433, 443]
ln:105
y:3
len(x):14
x(y):95
radix_tree_insert:xen/common/radix-tree.c:95
</pre>

