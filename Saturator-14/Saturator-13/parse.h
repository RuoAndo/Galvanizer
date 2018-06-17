static int counter = 0;
static char function_name[256];

struct symbol {               /* a word */
  struct ref *reflist;
  char *name;
};

struct ref {
  struct ref *next;
  char *filename;
  int flags;
  int lineno;
};

void test()
{
  printf("test %d \n", counter);
}

