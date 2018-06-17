#include <stdio.h>
#include <stdlib.h>

char tmp_string[1024];

void init_tmp_string(char *tmp_sting)
{
  int i;
  for(i=0; i<1024; i++)
    {
      tmp_string[i] = 1;
    }

}

int main() {
  int i;

  init_tmp_string(tmp_string);

  for(i=0; i<1024; i++)
    {
      printf("%d ", tmp_string[i]);
    }

}
