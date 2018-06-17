from pymongo import MongoClient

import numpy
import numpy as np

connect = MongoClient("127.0.0.1", 27017)
db= connect['sat']
collect = db['realloc']
collect2 = db['forloop']
collect3 = db['looptype']
collect4 = db['cve_2013_4371']

collect5 = db['definition']

ret = collect.find({"type":"realloc"}).batch_size(30)

for doc in ret:
        #print doc['lhs'] + ":" + doc['location']
        fileloc = doc['location']
        reallocln = int(doc['linenumber'])
        reallocline = doc['argument']

        #print fileloc
        
        ret2 = collect2.find({'location':fileloc}).batch_size(30)

        for doc2 in ret2:
            #print doc2
            flstart = int(doc2['start'])
            flend = int(doc2['end'])
            #flln = int(doc2['linenumber'])

            if reallocln > flstart and reallocln < flend:

                #print str(flstart) + "->" + str(reallocln) + "->" + str(flend) + "@" + fileloc

                #ret3 = collect3.find({"location":fileloc, "linenumber":443}).batch_size(30)
                ret3 = collect3.find({"location":fileloc, "linenumber": flstart, "type": "type5"}).batch_size(30)

                #collect3 = db['looptype']
                for doc3 in ret3:
                        print "DETECTED:"
                        print doc['lhs'] + ":" + doc['location'] + ":" + str(doc['linenumber']) + ":" + doc['argument'].rstrip().lstrip() + ":" + doc['line'].strip()
                        rhs = doc['argument'].rstrip().lstrip()
                        print doc2
                        print doc3

                        realloc_fileloc = doc['location']

                        line_number_array = []
                        ret5 = collect5.find({"location" : realloc_fileloc})
                        for doc5 in ret5:
                                if doc5['linenumber'].isdigit() == True:
                                        line_number_array.append(int(doc5['linenumber']))

                        line_number_array_uniq = list(set(line_number_array))
                
                        x = np.sort(line_number_array_uniq).tolist()
                        y = np.searchsorted(x, int(doc["linenumber"]), side='left')
                        print x
                        print "realloc:" + str(doc["linenumber"])
                        print x[y-1]

                        # ok.
                        # realloc:402
                        # 388 (x[y-1])

                        # no.
                        # realloc:251
                        # 497
                        
                        if int(doc["linenumber"]) > x[y-1]:
                                
                                ret6 = collect5.find({"location" : realloc_fileloc, "linenumber" : str(x[y-1])})
                                for doc6 in ret6:
                                        print doc6

                                        try:
                                                collect4.insert({"_id": doc["location"], "lhs": doc['lhs'], "linenumber": doc['linenumber'], "loop_start": str(doc2["start"]), "loop_end" : doc2["end"], "line" : doc2["line"], "realloc_line" : doc['line'].strip(), "function_name" : doc6["function_name"]})
                                        except:
                                                pass
                                                                    
                        print '---------------'
                                        
                        # tmp:forloop/libxl.c:403:(i + 1) * sizeof(libxl_cpupoolinfo))
                        # {u'end': 421, u'linecounter': 421, u'start': 398, u'location': u'forloop/libxl.c',
                        # u'line': u'    for (i = 0;; i++)', u'_id': ObjectId('57d21db4b39e3a28b7c93f0f'), u'type': u'forloop'}
                        # {u'_id': ObjectId('57d2296fe47d54056fc28ac2'), u'type': u'type5', u'location': u'forloop/libxl.c',
                        # u'linenumber': 398}

                        #pymongo.errors.DuplicateKeyError: insertDocument :: caused by :: 11000 E11000 duplicate key error index:
                        #sat.cve.$_id_  dup key: { : "libxl.c" }
                        #try:
                        #        collect4.insert({"_id": doc["location"], "lhs": doc['lhs'], "linenumber": doc['linenumber'], "loop_start": str(doc2["start"]), "loop_end" : doc2["end"], "line" : doc2["line"], "realloc-line" : doc['line'].strip()})
                
                        #except:
                        #        pass
                        #        

                                
#ret3 = collect3.find({"location":"tools/libxl/libxl.c", "type": "type5"}).batch_size(30)
#for doc3 in ret3:
#        print "test"
#        print doc3
