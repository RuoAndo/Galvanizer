#include <iostream>
#include <string>
#include <boost/spirit/include/qi.hpp>

namespace qi = boost::spirit::qi;

int main()
{

  std::string s("123 456");
  std::string::iterator first = s.begin(), last = s.end();
  bool success = qi::parse(
    first,
    last,
    qi::int_
  );
  
  if (success) { std::cout << "OK" << std::endl; }

  return 0;
}
