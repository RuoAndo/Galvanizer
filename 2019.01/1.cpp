#include <string>
#include <cstring>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <fstream>
#include <bitset>

#include <stdio.h>
#include <iostream>

#include <map>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>   

#include "csv.hpp"
using namespace std;

std::map<string, string> n;

int main( int argc, char* argv[] )
{
  int N = atoi(argv[2]);

  // map<string, string> myM;
  
  const string csv_file = std::string(argv[1]); 
  vector<vector<string>> data; 

  Csv objCsv(csv_file);
  if (!objCsv.getCsv(data)) {
     cout << "read ERROR" << endl;
     return 1;
  }

  // irq_bypass_register_producer,87,linux/virt/lib/irqbypass.c
  
  for (int row = 0; row < data.size(); row++) {
      vector<string> rec = data[row];
      n.insert(pair<string, string>(rec[0],rec[1]));
  }

  for (auto itr = n.begin(); itr != n.end(); itr++)
    {
      std::cout << itr->first << "," << itr->second << std::endl;
    }         
  
  return 0;
}
