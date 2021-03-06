#if __linux__ && defined(__INTEL_COMPILER)
#define __sync_fetch_and_add(ptr,addend) _InterlockedExchangeAdd(const_cast<void*>(reinterpret_cast<volatile void*>(ptr)), addend)
#endif
#include <string>
#include <cstring>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <fstream>
#include <bitset>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>   

#include "tbb/concurrent_hash_map.h"
#include "tbb/blocked_range.h"
#include "tbb/parallel_for.h"
#include "tbb/tick_count.h"
#include "tbb/task_scheduler_init.h"
#include "tbb/concurrent_vector.h"
//  #include "tbb/tbb_allocator.hz"
#include "utility.h"

#include "csv.hpp"

using namespace tbb;
using namespace std;

/*
struct HashCompare {
  static size_t hash( string x ) {
    return (string)x;
  }
  static bool equal( string x, string y ) {
    return x==y;
  }
};
*/

typedef concurrent_hash_map<string, std::vector<int>> CharTable;
static CharTable table;   

std::vector<string> timestamp;

std::vector<std::string> split_string_2(std::string str, char del) {
  int first = 0;
  int last = str.find_first_of(del);

  std::vector<std::string> result;

  while (first < str.size()) {
    std::string subStr(str, first, last - first);

    result.push_back(subStr);

    first = last + 1;
    last = str.find_first_of(del, first);

    if (last == std::string::npos) {
      last = str.size();
    }
  }

  return result;
}

int main( int argc, char* argv[] ) {

  int counter = 0;
  int N = atoi(argv[2]);  

  struct in_addr inaddr;
  char *some_addr;
  
    try {
        tbb::tick_count mainStartTime = tbb::tick_count::now();
        srand(2);

        utility::thread_number_range threads(tbb::task_scheduler_init::default_num_threads,0);
        // Data = new MyString[N];

	const string csv_file = std::string(argv[1]); 
	vector<vector<string>> data; 
	
	try {
	  Csv objCsv(csv_file);
	  if (!objCsv.getCsv(data)) {
	    cout << "read ERROR" << endl;
	    return 1;
	  }

	  for (unsigned int row = 0; row < data.size(); row++) {
	    vector<string> rec = data[row]; 
	    std::string path = rec[2];

	    //  BLK_MAX_CDB,724,linux/block/scsi_ioctl.c
	    //  replaceAll(path, "/", "__");

	    std::replace(path.begin(), path.end(), '/', '|');
	    
	    cout << path << endl;
	    	    
	    CharTable::accessor a;
	    // string timestamp_string to_string(timestamp
	    table.insert(a, path);
	    a->second.push_back(stoi(rec[1]));

	    /*
	    for(size_t c = tms.find_first_of("\""); c != string::npos; c = c = tms.find_first_of("\"")){
	      tms.erase(c,1);
	    }

	    for(size_t c = tms.find_first_of("/"); c != string::npos; c = c = tms.find_first_of("/")){
	      tms.erase(c,1);
	    }

	    for(size_t c = tms.find_first_of("."); c != string::npos; c = c = tms.find_first_of(".")){
	      tms.erase(c,1);
	    }

	    for(size_t c = tms.find_first_of(" "); c != string::npos; c = c = tms.find_first_of(" ")){
	      tms.erase(c,1);
	    }

	    for(size_t c = tms.find_first_of(":"); c != string::npos; c = c = tms.find_first_of(":")){
	      tms.erase(c,1);
	    }
	    */

	    // timestamp.push_back(tms);
	  }
	}
	catch (...) {
	  cout << "EXCEPTION!" << endl;
	  return 1;
	}

	/*
	std::remove("reduced-timestamp");
	ofstream outputfile("reduced-timestamp");
	
	for(auto itr = timestamp.begin(); itr != timestamp.end(); ++itr) {
	  outputfile  << *itr << std::endl;
	}
      
	outputfile.close();
	*/	  

	for( CharTable::iterator i=table.begin(); i!=table.end(); ++i )
	  {
	    for(auto itr = i->second.begin(); itr != i->second.end(); ++itr) {
	 	    cout << i->first << "," <<  *itr << endl;
	    }
	  }

        utility::report_elapsed_time((tbb::tick_count::now() - mainStartTime).seconds());
       
        return 0;
	
    } catch(std::exception& e) {
        std::cerr<<"error occurred. error text is :\"" <<e.what()<<"\"\n";
    }
}
