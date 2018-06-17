Applying Saturator for dealing with CVEs.

#################################

# requirements

MongoDB: document oriented database (KVS) <br>
global: GNU global source code tagging system <br>
python: devel-libs, pymongo (mongodb-driver) and numpy <br>

install.sh

	  export LC_ALL=C
  	  apt-get install -y mongodb
  	  apt-get install -y global python-pip
  	  apt-get install -y build-essential python-dev
  	  pip install numpy
  	  easy_install numpy
  	  python -m pip install pymongo
  	  easy_install pymongo

# generating data in MongoDB

do.sh

	  chmod 755 *pl
  	  chmod 755 *py
  	  chmod 755 *sh
  	  gtags -v
  	  rm -rf list
  	  ./listup.pl | tee list
  	  rm -rf flist
  	  ./global-t.sh list | tee flist
  	  rm -rf flist2 
  	  ./1.pl flist | tee flist2
  	  rm -rf flist3 
  	  ./cut.pl flist2 | tee flist3
  	  rm -rf flist3-drem 
  	  ./drem.pl flist3 | tee flist3-drem
  	  rm -rf flist4
  	  python global-rx.py flist3-drem | tee flist4
  	  rm -rf flist5
  	  ./1.pl flist4 | tee flist5
  	  python flist2.py flist2
  	  python flist5.py flist5
  	  python ex3.py

<h2>Phase 1: [1] - [7]: global -t と global -rx のコマンド出力を整形</h2>

最終的に生成されるファイル

	1)global -t => flist2
	2)global -rx => flist3

利用するファイル

	1) listup.pl
	2) global-t.sh 
	3) 1.pl 
	4) 1.py
	5) cut.pl 
	6) drem.pl
	7)global-rx.py

<u><b>STEP[1] ./listup.pl > list </u></b><br>
listing up all files ディレクトリ内のファイルを再帰的にすべてリストアップ

	list
	./xen/drivers/passthrough/vtd/dmar.h
	./xen/drivers/passthrough/vtd/dmar.c
	./xen/drivers/passthrough/vtd/extern.h
	./xen/drivers/passthrough/vtd/intremap.c

<u><b>STEP[2] ./global-t.sh list > flist </u></b><br> 
enumrating functions of all files パス付きのファイルリストを元に、gtag (global -t)の出力を全関数について書き出す

	#!/bin/sh
	echo $1
	filename=$1

	while read LINE; do
		global -f ${LINE}
	done < ${filename}

flist:
	libxl_domain_info  372 tools/libxl/libxl.c int libxl_domain_info(libxl_ctx *ctx, libxl_dominfo *info_r,                                                                                            
	libxl_list_cpupool  388 tools/libxl/libxl.c libxl_cpupoolinfo * libxl_list_cpupool(libxl_ctx *ctx\
	, int *nb_pool) 

<u><b>STEP[3] ./1.pl flist > flist2</u></b><br>
read until ")" (right brace) occurs calling 1.py 
一行で右カッコが閉じないものについて、処理する。(1.pyを呼び出す）

	#!/usr/bin/perl -w

	foreach $data (@list)
	{

	    $result=`python 1.py $m[2] $m[0] $m[1]`;
    	print $result;
	}

	close(FILEHANDLE);

<u><b>STEP[4] ./cut.pl flist2 > flist3 </u></b><br>
extracting function name  (cutting path)

flist3:

	libxl_list_domain                                                                      
	libxl_domain_info                                                                        
	libxl_list_cpupool
	libxl_list_vm     

<u><b>STEP[5] ./drem.pl flist3 > flist3-drem </u></b><br>
cutting duplicated function name

<u><b>STEP[6] python global-rx.py flist3-drem > flist4 </u></b><br>

flist3:

	rijndael_set_key 1243 xen/crypto/rijndael.c rijndael_set_key(rijndael_ctx *ctx, const u_char *key\
	, int bits)                                                                                       
	rijndael_decrypt 1260 xen/crypto/rijndael.c rijndael_decrypt(rijndael_ctx *ctx, const u_char *src\
	, u_char *dst)                                                                                    
	rijndael_encrypt 1266 xen/crypto/rijndael.c rijndael_encrypt(rijndael_ctx *ctx, const u_char *src\
	, u_char *dst) 

	# time python global-rx.py flist3-drem > flist4

	real    65m28.102s
	user    21m50.904s
	sys     37m2.386s

<u><b>STEP[7] ./1.pl flist4 > flist5</u></b><br>

do.sh - do all at once (STEP[1] - [7]).

      apt-get install -y global
      gtags -v
      ./listup.pl > list 
      ./global-t.sh list > flist 
      ./1.pl flist > flist2 
      ./cut.pl flist2 > flist3 
      ./drem.pl flist3 > flist3-drem
      python global-rx.py flist3-drem > flist4
      ./1.pl flist4 > flist5

real    48m53.981s
user    33m1.083s
sys     14m31.247s

#############################################

<h2>Phase 2:csv ファイルの生成</h2>

      ./flist_to_csv.pl flist > flist.csv
      ./flist_to_csv.pl flist3 > list-callchain.csv
          
<h2>Phase 3: inserting results of phase 1 into MongoDB / MongoDBへ格納</h2>

<b><u>step [1]: inserting info of callees. </u></b>

bash# time python flist5.py flist5

"extras/mini-os/include/ia64/os.h

106static inline uint64_t <br>
107xchg8(uint64_t* ptr, uint64_t x) <br>

		   { "_id" : ObjectId("57b8060bb3051f288e5dc7d1"), "arguments" : "uint64_t a", "type" : "definition", "function_type" : "", "location" : "extras/mini-os/arch/ia64/efi.c", "linenumber" : "40", "callee" : "uint64_t", "function_name" : "ia64_call_efi_func" }
		   { "_id" : ObjectId("57b8060bb3051f288e5dc7d2"), "arguments" : "uint64_t b", "type" : "definition", "function_type" : "", "location" : "extras/mini-os/arch/ia64/efi.c", "linenumber" : "40", "callee" : "uint64_t", "function_name" : "ia64_call_efi_func" }
		   { "_id" : ObjectId("57b8060bb3051f288e5dc7d3"), "arguments" : "uint64_t c", "type" : "definition", "function_type" : "", "location" : "extras/mini-os/arch/ia64/efi.c", "linenumber" : "40", "callee" : "uint64_t", "function_name" : "ia64_call_efi_func" }
		   { "_id" : ObjectId("57b8060bb3051f288e5dc7d4"), "arguments" : "uint64_t d", "type" : "definition", "function_type" : "", "location" : "extras/mini-os/arch/ia64/efi.c", "linenumber" : "40", "callee" : "uint64_t", "function_name" : "ia64_call_efi_func" }

real    0m57.328s
user    0m30.858s
sys     0m4.454s

<u><b>step [2] : inserting info of function definitions</u></b>

bash# python flist2.py flist2

      { "_id" : ObjectId("57b801fdb3051f4270bfb989"), "function_type" : "void", "arguments" : "unsigned char *m", "linenumber" : "779", "function_name" : "vhash_update", "type" : "definition", "location" : "xen/crypto/vmac.c" }
      { "_id" : ObjectId("57b801fdb3051f4270bfb98a"), "function_type" : "void", "arguments" : "vmac_ctx_t    *ctx", "linenumber" : "779", "function_name" : "vhash_update", "type" : "definition", "location" : "xen/crypto/vmac.c" }

real    0m39.003s<br>
user    0m22.087s<br>
sys     0m2.066s<br>

<h2>Phase 4: extracting callchain</h2>

python ex3.py

> db.ex.find().limit(-1).skip(500).next()                                                         
{
        "_id" : ObjectId("57b93e6eb3051f38d71cf8a1"),
        "caller_ln" : 649,
        "caller" : "get_cluster_offset",
        "location" : "tools/ioemu-qemu-xen/block-qcow2.c",
        "callee_ln" : "649",
        "callee" : "uint64_t"
}

> db.ex.find().limit(-1).skip(1500).next()                                                        
{
        "_id" : ObjectId("57b93ee5b3051f38d71cfc89"),
        "caller_ln" : 619,
        "caller" : "fzap_lookup",
        "location" : "tools/libfsimage/zfs/fsys_zfs.c",
        "callee_ln" : "641",
        "callee" : "uint64_t"
}

<h2>Phase 5: visualizing callchain (using graphviz)</h2>

	  > db.ex.find({"callee":/libxl_list_cpupool/})                                                                        
	  { "_id" : ObjectId("57bb0effb3051f6c18001ed6"), "caller_ln" : 3148, "caller" : "libxl_cpupool_cpuremove_node", "location" : "tools/libxl/libxl.c", "callee_ln" : 3157, "callee" : "libxl_list_cpupool" }
	  { "_id" : ObjectId("57bb0effb3051f6c18001ed7"), "caller_ln" : 212, "caller" : "libxl_cpuid_destroy", "location" : "tools/libxl/libxl.h", "callee_ln" : 418, "callee" : "libxl_list_cpupool" }
	  { "_id" : ObjectId("57bb0effb3051f6c18001ed8"), "caller_ln" : 139, "caller" : "libxl_name_to_cpupoolid", "location" : "tools/libxl/libxl_utils.c", "callee_ln" : 147, "callee" : "libxl_list_cpupool" }
	  { "_id" : ObjectId("57bb0effb3051f6c18001ed9"), "caller_ln" : 5441, "caller" : "main_cpupoollist", "location" : "tools/libxl/xl_cmdimpl.c", "callee_ln" : 5493, "callee" : "libxl_list_cpupool" }

viz.sh

	python viz.py libxl_list_cpupool > tmpdot
	dot -o c.png -Tpng tmpdot
	cp c.png 

<img src="c.png">

<h2>Detecting CVE-2013-4371</h2>

<u>step 1: generating file list.</u>

	   -bash-4.1# ./filelist.pl flist > filelist
	   -bash-4.1# ./drem.pl filelist > filelist-drem
	   -bash-4.1# wc -l filelist
	   97639 filelist
	   -bash-4.1# wc -l filelist-drem
	   2739 filelist-drem

bash# for.sh filelist-drem

	   TESTFILE=$1
	   while read line; do
    	   	 python for.py $line
	   done < $TESTFILE

real    6m20.072s
user    5m8.987s
sys     0m54.946s

	> db.forloop.find()                                                                                                               
	{ "_id" : ObjectId("57ce59eeb3051f085ad12465"), "end" : 753, "linecounter" : 753, "start" : 738, "location" : "xen/crypto/rijndael.c", "line" : "\t\tfor (;;) {", "type" : "forloop" }
	{ "_id" : ObjectId("57ce59eeb3051f085ad12466"), "end" : 775, "linecounter" : 775, "start" : 758, "location" : "xen/crypto/rijndael.c", "line" : "\t\tfor (;;) {", "type" : "forloop" }

	> db.forloop.count()                                                                                                              
	6638

time ./realloc.sh filelist-drem

      { "_id" : ObjectId("57ce611fb3051f48ea5c3712"), "lhs" : "tmp", "location" : "tools/libxl/libxl.c", "linenumber" : 402, "line" : "        tmp = realloc(ptr, (i + 1) * sizeof(libxl_cpupoolinfo));\n", "type" : "realloc-line" }

real    5m57.291s
user    4m56.786s
sys     0m54.215s

<u>step 2: detecting realloc() in forloop.</u>

-bash-4.1# time python realloc-forloop.py

real    0m2.019s
user    0m0.591s
sys     0m0.063s

	tmp:tools/libxl/libxl.c:402:tmp = realloc(ptr, (i + 1) * sizeof(libxl_cpupoolinfo));
	{u'end': 420, u'linecounter': 420, u'start': 398, u'location': u'tools/libxl/libxl.c', u'line': u'    for (i = 0;; i++) {', u'_id': ObjectId('57ce5b35b3051f3fc7402bd8'), u'type': u'forloop'}

<u>step 3: do-it-all</u>

CVE-2013-4371.sh

	export LC_ALL=en_US.UTF-8
	cd forloop
	make clean
	make
	rm -rf parse
	cp forloop/parse .
	cd ..

	time ./filelist.pl flist > filelist
	time ./drem.pl filelist > filelist-drem

	# forloop
	time ./for.sh filelist-drem

	# notes:
	# realloc.sh calls realloc.py. realloc.py drops looptype also.
	# db= connect['sat']
	# db.drop_collection(db.relloc)
	# db.drop_collection(db.looptype)
	time ./realloc.sh filelist-drem

	# parse.yy
	# const string ns = "sat.looptype";
	# builder.append("type", type).append("linenumber", linenumber);  
	time ./realloc-looptype.sh filelist-drem

	# if reallocln > flstart and reallocln < flend:
	time python realloc-forloop.py

real    62m7.052s
user    12m52.504s
sys     1m8.384s
	
	> db.cve_2013_4371.find()                                                                                                                      
	{ "_id" : "tools/libxl/libxl.c", "loop_start" : "398", "realloc_line" : "tmp = realloc(ptr, (i + 1) * sizeof(libxl_cpupoolinfo));", "lhs" : "tmp", "linenumber" : 402, "loop_end" : 420, "line" : "    for (i = 0;; i++) {", "function_name" : "libxl_list_cpupool" }

DETECTED!

	388: libxl_cpupoolinfo * libxl_list_cpupool(libxl_ctx *ctx, int *nb_pool)
	389: {
	390:     libxl_cpupoolinfo *ptr, *tmp;
	391:     int i;
	392:     xc_cpupoolinfo_t *info;
	393:     uint32_t poolid;
	394: 
	395:     ptr = NULL;
	396: 
	397:     poolid = 0;
	398:     for (i = 0;; i++) {
	399:         info = xc_cpupool_getinfo(ctx->xch, poolid);
	400:         if (info == NULL)
	401:             break;
	402:         tmp = realloc(ptr, (i + 1) * sizeof(libxl_cpupoolinfo));
	403:         if (!tmp) {
	404:             LIBXL__LOG_ERRNO(ctx, LIBXL__LOG_ERROR, "allocating cpupool info");
	405:             free(ptr);
	406:             xc_cpupool_infofree(ctx->xch, info);
	407:             return NULL;
	408:         }
	409:         ptr = tmp;
	410:         ptr[i].poolid = info->cpupool_id;
	411:         ptr[i].sched_id = info->sched_id;
	412:         ptr[i].n_dom = info->n_dom;
	413:         if (libxl_cpumap_alloc(ctx, &ptr[i].cpumap)) {
	414:             xc_cpupool_infofree(ctx->xch, info);
	415:             break;
	416:         }
	417:         memcpy(ptr[i].cpumap.map, info->cpumap, ptr[i].cpumap.size);
	418:         poolid = info->cpupool_id + 1;
	419:         xc_cpupool_infofree(ctx->xch, info);
	420:     }
	421: 
	422:     *nb_pool = i;
	423:     return ptr;
	424: }

#detecting CVE-2016-0728

	   # global -t join_session_keyring                                                                                              
	   join_session_keyring    security/keys/process_keys.c    753

	   742: /*
	   743:  * Join the named keyring as the session keyring if possible else attempt to
	   744:  * create a new one of that name and join that.
	   745:  *
	   746:  * If the name is NULL, an empty anonymous keyring will be installed as the
	   747:  * session keyring.
	   748:  *
	   749:  * Named session keyrings are joined with a semaphore held to prevent the
	   750:  * keyrings from going away whilst the attempt is made to going them and also
	   751:  * to prevent a race in creating compatible session keyrings.
	   752:  */
	   753: long join_session_keyring(const char *name)
	   754: {
	   755: 	const struct cred *old;
	   756: 	struct cred *new;
	   757: 	struct key *keyring;
	   758: 	long ret, serial;
	   759: 
	   760: 	new = prepare_creds();
	   761: 	if (!new)
	   762: 		return -ENOMEM;
	   763: 	old = current_cred();
	   764: 
	   765: 	/* if no name is provided, install an anonymous keyring */
	   766: 	if (!name) {
	   767: 		ret = install_session_keyring_to_cred(new, NULL);	
	   768: 		if (ret < 0)
	   769: 			goto error;
	   770: 
	   771: 		serial = new->session_keyring->serial;
	   772: 		ret = commit_creds(new);
	   773: 		if (ret == 0)
	   774: 			ret = serial;
	   775: 		goto okay;
	   776: 	}
	   777: 
	   778: 	/* allow the user to join or create a named keyring */
	   779: 	mutex_lock(&key_session_mutex);
	   780: 
	   781: 	/* look for an existing keyring of this name */
	   782: 	keyring = find_keyring_by_name(name, false);
	   783: 	if (PTR_ERR(keyring) == -ENOKEY) {
	   784: 		/* not found - try and create a new one */
	   785: 		keyring = keyring_alloc(
	   786: 			name, old->uid, old->gid, old,
	   787: 			KEY_POS_ALL | KEY_USR_VIEW | KEY_USR_READ | KEY_USR_LINK,
	   788: 			KEY_ALLOC_IN_QUOTA, NULL);
	   789: 		if (IS_ERR(keyring)) {
	   790: 			ret = PTR_ERR(keyring);
	   791: 			goto error2;
	   792: 		}
	   793: 	} else if (IS_ERR(keyring)) {
	   794: 		ret = PTR_ERR(keyring);
	   795: 		goto error2;
	   796: 	} else if (keyring == new->session_keyring) {
	   797: 		ret = 0;
	   798: 		goto error2;
	   799: 	}
	   800: 
	   801: 	/* we've got a keyring - now to install it */
	   802: 	ret = install_session_keyring_to_cred(new, keyring);
	   803: 	if (ret < 0)
	   804: 		goto error2;
	   805: 
	   806: 	commit_creds(new);
	   807: 	mutex_unlock(&key_session_mutex);
	   808: 
	   809: 	ret = keyring->serial;
	   810: 	key_put(keyring);
	   811: okay:
	   812: 	return ret;
	   813: 
	   814: error2:
	   815: 	mutex_unlock(&key_session_mutex);
	   816: error:
	   817: 	abort_creds(new);
	   818: 	return ret;
	   819: }
