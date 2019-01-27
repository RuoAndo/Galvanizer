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

#include "csv.hpp"
using namespace std;

int main( int argc, char* argv[] )
{
  int N = atoi(argv[2]);
  
  const string csv_file = std::string(argv[1]); 
  vector<vector<string>> data; 

  Csv objCsv(csv_file);
  if (!objCsv.getCsv(data)) {
     cout << "read ERROR" << endl;
     return 1;
  }

  for (int row = 0; row < data.size(); row++) {
      vector<string> rec = data[row]; 
  }

  return 0;
}
