#include <cassert>
#include <string>
#include <map>
#include <vector>
#include <iostream>
#include <iomanip>
#include <algorithm>

using namespace std;

class sat_ctx {
public:
  sat_ctx(int r) { assert(r > 0 && r < 10); radix = r; }

  inline int getradix(void) { return radix; } 

  void test(char *string, int current_line_number) 
  { 
    std::string string_2 = std::string(string);  
    //printf("test: %s %d \n", string, current_line_number);  
    values[string_2] = current_line_number;
  } 

  void list();

private:
  int radix;
  std::map<std::string, int> values;

};




