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

typedef concurrent_hash_map<string, std::vector<int>> global_rx_lineNumber;
static global_rx_lineNumber table_rx_lineNumber;

typedef concurrent_hash_map<string, std::vector<string>> global_rx_funcName;
static global_rx_funcName table_rx_funcName;

typedef concurrent_hash_map<string, std::vector<int>> global_tx_lineNumber;
static global_tx_lineNumber table_tx_lineNumber;

typedef concurrent_hash_map<string, std::vector<string>> global_tx_funcName;
static global_tx_funcName table_tx_funcName;   

std::vector<string> timestamp;

int main( int argc, char* argv[] ) {

  int counter = 0;
  // int N = atoi(argv[2]);  

  struct in_addr inaddr;
  char *some_addr;
  
    try {
        tbb::tick_count mainStartTime = tbb::tick_count::now();
        srand(2);

        utility::thread_number_range threads(tbb::task_scheduler_init::default_num_threads,0);
        // Data = new MyString[N];

	const string csv_file = std::string(argv[1]); 
	vector<vector<string>> data_rx; 
	
	try {
	  Csv objCsv(csv_file);
	  if (!objCsv.getCsv(data_rx)) {
	    cout << "read ERROR" << endl;
	    return 1;
	  }

	  for (unsigned int row = 0; row < data_rx.size(); row++) {
	    vector<string> rec_rx = data_rx[row]; 
	    std::string path = rec_rx[2];

	    //  BLK_MAX_CDB,724,linux/block/scsi_ioctl.c
	    //  replaceAll(path, "/", "__");

	    // std::replace(path.begin(), path.end(), '/', '|');
	    	    
	    global_rx_lineNumber::accessor rx_lineNumber;
	    table_rx_lineNumber.insert(rx_lineNumber, path);
	    rx_lineNumber->second.push_back(stoi(rec_rx[1]));

	    global_rx_funcName::accessor rx_funcName;
	    table_rx_funcName.insert(rx_funcName, path);
	    rx_funcName->second.push_back(rec_rx[0]);

	  }
	}
	catch (...) {
	  cout << "EXCEPTION!" << endl;
	  return 1;
	}
	
        // utility::report_elapsed_time((tbb::tick_count::now() - mainStartTime).seconds());

	/*** parsing global-tx ***/

	const string csv_file_2 = std::string(argv[2]); 
	vector<vector<string>> data_2; 
	
	try {
	  Csv objCsv2(csv_file_2);
	  if (!objCsv2.getCsv(data_2)) {
	    cout << "read ERROR" << endl;
	    return 1;
	  }

	  for (unsigned int row = 0; row < data_2.size(); row++) {
	    vector<string> rec_tx = data_2[row]; 
	    std::string path_tx = rec_tx[2];

	    //  scsi_request,9,linux/include/scsi/scsi_request.h	  
	    // std::replace(path_tx.begin(), path_tx.end(), '/', '|');
	    	    	    
	    global_tx_lineNumber::accessor tx_lineNumber;
	    table_tx_lineNumber.insert(tx_lineNumber, path_tx);
	    tx_lineNumber->second.push_back(stoi(rec_tx[1]));	    

	    global_tx_funcName::accessor tx_funcName;
	    table_tx_funcName.insert(tx_funcName, path_tx);
	    tx_funcName->second.push_back(rec_tx[0]);	    
	  }
	}
	catch (...) {
	  cout << "EXCEPTION!" << endl;
	  return 1;
	}

	int counter = 0;

	cout << table_rx_funcName.size() << endl;
	cout << table_rx_lineNumber.size() << endl;

	global_rx_funcName::iterator j=table_rx_funcName.begin();
	for( global_rx_lineNumber::iterator i=table_rx_lineNumber.begin(); i!=table_rx_lineNumber.end(); ++i )
	  {

	    auto itr2 = j->second.begin();
	    
	    for(auto itr = i->second.begin(); itr != i->second.end(); ++itr) {
	      
	      // cout << "[rx]," << i->first << "," <<  *itr << "," << *itr2 << endl;
	      
	      global_tx_funcName::iterator k=table_tx_funcName.begin();
	      for( global_tx_lineNumber::iterator l=table_tx_lineNumber.begin(); l!=table_tx_lineNumber.end(); ++l )
		{
	      
		  if(i->first == l->first)
		    {
		      cout << "[rx]," << i->first << "," <<  *itr << "," << *itr2 << endl;
		      cout << "[HIT]" << "[tx]," << l->first << "," << endl;

		      for(auto itr3 = l->second.begin(); itr3 != l->second.end(); ++itr3)
			{
			  cout << *itr3 << ",";
			}     
		      cout << endl;
			
		      int back = std::lower_bound(l->second.begin() + 1, l->second.end() - 1, *itr) - l->second.begin();
		      int front = back - 1;
		      cout << front << "," << l->second[front] << "," << k->second[front] << endl;

		      cout << endl;											     
		    }
		  
		  k++;
		} // for( global_tx_lineNumber::iterator l=table_tx_lineNumber.begin(); l!=table_tx_lineNumber.end(); ++l )

	      itr2++;
	    } // for(auto itr = i->second.begin(); itr != i->second.end(); ++itr) {

	    j++;

	  } // for( global_rx_lineNumber::iterator i=table_rx_lineNumber.begin(); i!=table_rx_lineNumber.end(); ++i )
	    
	      
	      /*
	      global_tx_funcName::iterator k=table_tx_funcName.begin();
	      for( global_tx_lineNumber::iterator l=table_tx_lineNumber.begin(); l!=table_tx_lineNumber.end(); ++l )
		{
		  
		  if(i->first == l->first)
		    {
		      cout << "[HIT]" << "[tx]," << l->first << "," << endl;

		      for(auto itr3 = l->second.begin(); itr3 != l->second.end(); ++itr3)
			{
			  cout << *itr3 << ",";
			}     
		      cout << endl;
			
		      int back = std::lower_bound(l->second.begin() + 1, l->second.end() - 1, *itr) - l->second.begin();
		      int front = back -1;
		      cout << front << "," << l->second[front] << "," << k->second[front] << endl;

		      cout << endl;											     
		    }
			
		}
	      */
	      		  
	// utility::report_elapsed_time((tbb::tick_count::now() - mainStartTime).seconds());
	// return 0;

    } catch(std::exception& e) {
        std::cerr<<"error occurred. error text is :\"" <<e.what()<<"\"\n";
    }
}
