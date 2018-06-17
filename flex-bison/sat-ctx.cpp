#include <stdio.h>
#include "sat-ctx.hh"

struct list_action {
  void operator()(const std::pair<std::string, int> &it)
  {
    std::cout << it.first << " = " << it.second << std::endl;
  }
} ;

void sat_ctx::list()
{
  std::for_each(values.begin(), values.end(), list_action());
}

