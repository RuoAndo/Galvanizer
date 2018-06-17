# enumerating and visualizing callgraph

CVE-2013-4371
https://wiki.xenproject.org/wiki/Cpupools_Howto

<pre>
 bash# python ex-list.py xen414 libxl_list_cpupool > tmp
 bash# cd viz

 2079  python 1.py tmp > tmp2
 2080  dot -Tpng tmp2 -o tmp2.png
 2081  eog tmp2.png
</pre>

<img src="tmp2.png">

CVE-2016-2775
https://kb.isc.org/article/AA-01393/74/CVE-2016-2775%3A-A-query-name-which-is-too-long-can-cause-a-segmentation-fault-in-lwresd.html

<pre>
 bash# python ex-list.py bind999b1 isc_buffer_allocate > tmp /
</pre>

<img src="loop.png">

LIMIT = 3

<img src="bind-CVE-2106-2775-limit-3.png">

LIMIT = 7

<img src="bind-CVE-2106-2775-limit-7.jpg">


