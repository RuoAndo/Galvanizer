# enumerating poiner invocation

entering souce code directory.
<pre>
# cd xen-4.1.2/
</pre>

listing up files.
<pre>
# ./listup.pl | tee list
xen/common/sched_credit2.c
xen/common/sched_credit2.c
</pre>

parsing list.
<pre>
# ./parse.sh list > tmp
*prv,310,xen/common/sched_credit2.c
*prv,354,xen/common/sched_credit2.c
</pre>

searching caller.
<pre>
# python search.py xen_test xen/common/sched_credit2.c 1553
[280, 285, 295, 301, 307, 351, 396, 406, 442, 471, 482, 586, 627, 674, 707, 730, 770, 798, 808, 822, 832, 863, 871, 897, 916, 969, 1005, 1121, 1155, 1194, 1352, 1362, 1378, 1434, 1461, 1480, 1495, 1506, 1548, 1589, 1721, 1735, 1772, 1825, 1842, 1855, 1921, 1935, 1977, 1989, 2012, 2059]
x:[280, 285, 295, 301, 307, 351, 396, 406, 442, 471, 482, 586, 627, 674, 707, 730, 770, 798, 808, 822, 832, 863, 871, 897, 916, 969, 1005, 1121, 1155, 1194, 1352, 1362, 1378, 1434, 1461, 1480, 1495, 1506, 1548, 1589, 1721, 1735, 1772, 1825, 1842, 1855, 1921, 1935, 1977, 1989, 2012, 2059]
ln:1553
y:39
len(x):52
x(y):1589
runq_candidate:xen/common/sched_credit2.c:1548
</pre>

searching caller 2.

python 2.py tmp xen_test > tmp2

input: tmp
<pre>
*height,62,xen/common/radix-tree.c
*node,98,xen/common/radix-tree.c
*offset,129,xen/common/radix-tree.c
</pre>

output: tmp2
<pre>
*height,62,radix_tree_extend:xen/common/radix-tree.c:55
*node,98,radix_tree_insert:xen/common/radix-tree.c:95
*offset,129,radix_tree_insert:xen/common/radix-tree.c:95
</pre>

searching caller 3.
python 3.py tmp xen_test > tmp2
output: tmp2
<pre>
*height,62,radix_tree_extend,xen/common/radix-tree.c,55,4,1
*node,98,radix_tree_insert,xen/common/radix-tree.c,95,6,1
*offset,129,radix_tree_insert,xen/common/radix-tree.c,95,6,1
</pre>

<pre>
# time python 3.py tmp xen_test > tmp2

real    159m37.013s
user    94m4.120s
sys     523m28.156s
</pre>

# spliting file into functions.

<pre>
# python definition.py xen_test list
</pre>

input: list
<pre>
xen/common/wait.c
xen/common/xmalloc_tlsf.c
xen/common/Makefile
</pre>

output: files
<pre>
# ls
fn-float64_arcsin
fn-pt_is_iomul
fn-zio_checksum_t
fn-float64_arctan
fn-pt_libpci_fixup
fn-zio_checksum_verify
</pre>

rename.
<pre>
# python rename.py list
</pre>

counting up.
<pre>
# python count.py list2 > tmp-count
</pre>

input: list2
<pre>
Crypto_SHA1Full
Crypto_SHA1Full_buf
Crypto_symcrypto_decrypt
Crypto_symcrypto_encrypt
</pre>

output:
<pre>
BSG_Pack_private,3,12,21,1
BSG_Unpack,2,0,1,0
BSG_Unpack_private,0,0,0,0
BSG_static_selfcheck,0,1,4,0
</pre>

