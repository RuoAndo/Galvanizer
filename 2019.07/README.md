<pre>
 2011  grep drivers r.csv > r.csv.drivers
  2016  split -l 500000 r.csv.drivers
   2018  mkdir rx-drivers
    2019  mv x* ./rx-drivers/

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