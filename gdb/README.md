<pre>
# grep CL_GENERATED *c -rin 
clause.c:3554:  Stats[CL_GENERATED]++;
geometry.c:203:  Stats[CL_GENERATED]++;
linkur.c:1030:        Stats[CL_GENERATED]++;
misc.c:1187:  fprintf(fp, "clauses generated        %7ld\n", Stats[CL_GENERATED]);
misc.c:1270:  fprintf(fp, "clauses generated        %7ld\n", Stats[CL_GENERATED]);
misc.c:1827:  gen = Stats[CL_GENERATED];
misc.c:2425:  fprintf(fp, "generated %ld\n", Stats[CL_GENERATED]);
paramod.c:233:      Stats[CL_GENERATED]++;
paramod.c:396:      Stats[CL_GENERATED]++;
process.c:290:    Stats[CL_GENERATED]++;
resolve.c:283:  Stats[CL_GENERATED]++;
resolve.c:1317:     Stats[CL_GENERATED]++;
resolve.c:1441:    Stats[CL_GENERATED]++;

# grep CL_GENERATED *c -rin > tmp
# python 1.py tmp
b geometry.c:203
b linkur.c:1030
b misc.c:1187
b misc.c:1270
b misc.c:1827
b misc.c:2425
b paramod.c:233
b paramod.c:396
b process.c:290
b resolve.c:283
b resolve.c:1317
b resolve.c:1441

# python 1.py tmp > tmp2

# gdb /home/flare/otter-3.3f/bin/otter 
GNU gdb (Ubuntu 8.1-0ubuntu3) 8.1.0.20180409-git
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from /home/flare/otter-3.3f/bin/otter...done.
(gdb) source tmp2
Breakpoint 1 at 0x25a36: file geometry.c, line 203.
Breakpoint 2 at 0x22497: file linkur.c, line 1030.
Breakpoint 3 at 0x1c7fc: file misc.c, line 1187.
Breakpoint 4 at 0x1cdfa: file misc.c, line 1270.
Breakpoint 5 at 0x1ea66: file misc.c, line 1827.
Breakpoint 6 at 0x202ac: file misc.c, line 2425.
Breakpoint 7 at 0x4d779: file paramod.c, line 233.
Breakpoint 8 at 0x4e0d6: file paramod.c, line 396.
Breakpoint 9 at 0x14efd: file process.c, line 290.
Breakpoint 10 at 0x8f8c: file resolve.c, line 283.
Breakpoint 11 at 0xc98e: file resolve.c, line 1317.
Breakpoint 12 at 0xd121: file resolve.c, line 1441.
</pre>