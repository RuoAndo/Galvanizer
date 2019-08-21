<pre>
#define N 5
#define WORKER_THREAD_NUM N
#define MAX_QUEUE_NUM N
#define END_MARK_FNAME   "///"
#define END_MARK_FLENGTH 3
</pre>

<pre>
# grep drivers r.csv > r.csv.drivers
# split -l 500000 r.csv.drivers
# mkdir rx-drivers
# mv x* ./rx-drivers/

# time ./traverse2 rx-drivers t.csv
355458457 - done.
355458458 - done.
355458459 - done.

real    12669m29.009s
user    62272m30.844s
sys     196m58.617s

# pwd
/home/flare/Saturator/2019.07
</pre>