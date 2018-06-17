/*
 properties:

  BSON_APPEND_UTF8 (doc, "property", "local_decl");
  BSON_APPEND_UTF8 (doc, "property", "forloop");
  BSON_APPEND_UTF8 (doc, "property", "function");

[1] local variable declaration.

 391    int i;
  { "_id" : ObjectId("573f0c010dd43c070c4017e1"), "property" : "local_decl", "file_name" : "./tools/libxl/libxl.c", "decls" : "i", "line_number" : 391 }

[2] forloop.

  > db.xen_4_1_0_func.find({"property":"forloop", "file_name":"./tools/libxl/libxl.c"})
{ "_id" : ObjectId("5735e8cb0dd43c7a5c365a99"), "property" : "forloop", "file_name" : "./tools/libxl/libxl.c", "conditions" : "i = 0; i < ret; i++\n", "line_number" : 365 }
  { "_id" : ObjectId("5735e8cb0dd43c7a5c365a9b"), "property" : "forloop", "file_name" : "./tools/libxl/libxl.c", "conditions" : "i = 0;; i++\n", "line_number" : 398 }

[3] function declaration (name).

  > db.xen_4_1_0_func.find({"property":"function", "file_name":"./tools/libxl/libxl.c"})
{ "_id" : ObjectId("5735e8cb0dd43c7a5c365a91"), "property" : "function", "function_name" : "\nint libxl_ctx_init", "file_name" : "./tools/libxl/libxl.c", "arguments" : "libxl_ctx *ctx, int version, xentoollog_logger *lg", "line_number" : 44 }


*/

%{
#include <stdio.h>
#include <stdlib.h>

#include <bson.h>
#include <mongoc.h>

#include "parse.h"

char tmp_string[1024];
char tmp_string_2[1024];
char cond_string[1024];
char local_variable_string[1024];

static int block_flag = 0;
static int func_flag = 0;

static int current_line_number = 0;

extern int yyparse();
extern FILE* yyin;

/* mongo setting */
char dbname[256];
char colname[256];
char ipaddress[256];
char filename[256];

mongoc_client_t *client;
mongoc_collection_t *collection;
mongoc_cursor_t *cursor;
bson_error_t error;
bson_oid_t oid;
bson_t *doc;

void yyerror(const char* s);
%}
%union {
    int ival;
    char* string;
}
%defines
%locations

%token SPACES
%token STRING
%token DECL
%token NUMBER

%type <ival> NUMBER
%type <string> STRING
%type <string> DECL

%code requires {
  char *p; 
}

%%

input
: input line
    | line
;

line
:
| string_list
| decl
| decl_name
| arg
| local
| forloop1
| forloop2
| cond1
| cond2
| cond3
| cond4
| realloc
;

/* realloc: use-after-free */

/*
   402        tmp = realloc(ptr, (i + 1) * sizeof(libxl_cpupoolinfo));
*/

/*
realloc: 'realloc' '(' string_list ')' { 
  track_line_number();
  print_line_number();
  printf("realloc detected %s \n", tmp_string);
}
*/


decl: decl_name arg {
  track_line_number();

  /*
  print_line_number();
  printf("decl %s \n", tmp_string_2);
  printf("argments: %s \n", tmp_string);
  */

  insert_function_name(tmp_string_2, tmp_string);

  init_tmp_string(tmp_string);
  init_tmp_string(tmp_string_2);

 }

arg: '(' string_list ')' {
  // print_line_number();
  // printf("arg %s\n", tmp_string);
  // init_tmp_string();
}

local: 'int' string_list ';' {
  print_line_number();
  init_local_variable_string();
  printf("local %s \n", tmp_string);
  sprintf(local_variable_string, "%s", tmp_string);
  track_line_number();
  insert_local_variable(local_variable_string);

 }

string_list : STRING {
  // init_tmp_string();
  sprintf(tmp_string, "%s", $1);
 }
|
string_list STRING {
  sprintf(tmp_string, "%s %s", tmp_string, $2);
  // print_line_number();
  // printf("string list %s \n", tmp_string);
}
|
string_list '*' STRING {
  sprintf(tmp_string, "%s *%s", tmp_string, $3);
  // print_line_number();
  // printf("string list %s \n", tmp_string);
  // printf("string list %s \n", tmp_string);
}
|
string_list '&' STRING {
  sprintf(tmp_string, "%s &%s", tmp_string, $3);
  // print_line_number();
  // printf("string list %s \n", tmp_string);
  // printf("string list %s \n", tmp_string);
}
|
string_list ',' STRING {
  sprintf(tmp_string, "%s, %s", tmp_string, $3);
  // print_line_number();
  // printf("string list %s \n", tmp_string);
  // printf("string list %s \n", tmp_string);
}
|
string_list ',' SPACES STRING {
  sprintf(tmp_string, "%s, %s", tmp_string, $4);
  // print_line_number();
  // printf("string list %s \n", tmp_string);
}

decl_name : DECL {
  // init_tmp_string_2();
  sprintf(tmp_string_2, "%s", $1);
  //printf("decl list %s \n", tmp_string_2);
}
|
decl_name STRING {
  sprintf(tmp_string_2, "%s %s", tmp_string_2, $2);
  //printf("decl list 2 \n");
}
|
decl_name "\n" STRING {
  // printf("decl list 3 \n");
  sprintf(tmp_string_2, "%s %s", tmp_string_2, $3);
}

// loop representation "as usual"
forloop1: cond1 cond2 cond3 {
  print_line_number();
  track_line_number();
  printf("forloop type 1. conditions: %s \n", cond_string);
  insert_loop(cond_string);
  init_cond_string();
}

cond1: 'for' '(' STRING '=' NUMBER ';' {
  print_line_number();
  sprintf(cond_string, "%s = %d; ", $3, $5);
  printf("cond1 %s = %d \n", $3, $5);
 }
cond2: STRING '<' STRING ';' {
  print_line_number();
  sprintf(cond_string, "%s%s < %s; ", cond_string, $1, $3);
  printf("cond2 %s < %s \n", $1, $3);
 }
cond3: STRING '++' ')' {
  print_line_number();
  sprintf(cond_string, "%s%s++\n", cond_string, $1);
  printf("cond3 %s++ \n", $1);
 }

// loop repsentation for "CVE-2013-4371"
// { "_id" : ObjectId("573f0c010dd43c070c4017e2"), "property" : "forloop", "file_name" : "./tools/libxl/libxl.c", "conditions" : "i = 0;; i++\n", "line_number" : 398 }

/*
388 libxl_cpupoolinfo * libxl_list_cpupool(libxl_ctx *ctx, int *nb_pool)
389 {
390    libxl_cpupoolinfo *ptr, *tmp;
391    int i;
392    xc_cpupoolinfo_t *info;
393    uint32_t poolid;
394
395    ptr = NULL;
396
397    poolid = 0;
398    for (i = 0;; i++) {
399        info = xc_cpupool_getinfo(ctx->xch, poolid);
400        if (info == NULL)
401            break;
402        tmp = realloc(ptr, (i + 1) * sizeof(libxl_cpupoolinfo));
403        if (!tmp) {
404            LIBXL__LOG_ERRNO(ctx, LIBXL__LOG_ERROR, "allocating cpupool info");
405            free(ptr);
406            xc_cpupool_infofree(ctx->xch, info);
407            return NULL;
408        }
409        ptr = tmp;
410        ptr[i].poolid = info->cpupool_id;
411        ptr[i].sched_id = info->sched_id;
412        ptr[i].n_dom = info->n_dom;
413        if (libxl_cpumap_alloc(ctx, &ptr[i].cpumap)) {
414            xc_cpupool_infofree(ctx->xch, info);
415            break;
416        }
417        memcpy(ptr[i].cpumap.map, info->cpumap, ptr[i].cpumap.size);
418        poolid = info->cpupool_id + 1;
419        xc_cpupool_infofree(ctx->xch, info);
420    }
421
422    *nb_pool = i;
423    return ptr;
424 }
*/

forloop2: cond4 cond3 {
  print_line_number();
  track_line_number();
  printf("forloop type 2 (without boundary). conditions: %s \n", cond_string);
  insert_loop(cond_string);
  init_cond_string();
}

cond4: 'for' '(' STRING '=' NUMBER ';'';' {
  print_line_number();
  sprintf(cond_string, "%s = %d;; ", $3, $5);
  printf("cond4 %s = %d \n", $3, $5);
 }

%%

void track_line_number()
{
  extern int yylineno;
  current_line_number = yylineno;
}

void print_line_number()
{
  extern int yylineno;
  printf("%d:", yylineno);
}

void init_tmp_string(char *tmp_string)
{
  int i;
  for(i=0; i<1024; i++)
    {
      tmp_string[i] = 0;
    }
}

/*
void init_tmp_string_2()
{
  int i;
  for(i=0; i<1024; i++)
    {
      tmp_string_2[i] = 0;
    }
}
*/

void init_cond_string()
{
  int i;
  for(i=0; i<1024; i++)
    {
      cond_string[i] = 0;
    }
}

void init_local_variable_string()
{
  int i;
  for(i=0; i<1024; i++)
    {
      local_variable_string[i] = 0;
    }
}

/* mongo db insertion routines */

void insert_function_name(char *functionname, char *argstr)
{
  char tmpstr[256];
  extern int yylineno;
  sprintf(tmpstr, "mongodb://%s:27017//", ipaddress);

  sprintf(tmp_string_2, "%s", functionname);

  // printf("func: %d: %s \n", current_line_number, tmp_string);   

  mongoc_init ();
  client = mongoc_client_new (tmpstr);
  collection = mongoc_client_get_collection (client, dbname, colname);

  doc = bson_new ();
  bson_oid_init (&oid, NULL);
  BSON_APPEND_OID (doc, "_id", &oid);
  BSON_APPEND_UTF8 (doc, "property", "function");
  BSON_APPEND_UTF8 (doc, "function_name", functionname);
  BSON_APPEND_UTF8 (doc, "file_name", filename);
  BSON_APPEND_UTF8 (doc, "arguments", argstr);
  BSON_APPEND_INT32 (doc, "line_number", current_line_number);

  if (!mongoc_collection_insert (collection, MONGOC_INSERT_NONE, doc, NULL, &error))
    {
	  fprintf (stderr, "%s\n", error.message);
    }

  bson_destroy (doc);

  mongoc_collection_destroy (collection);
  mongoc_client_destroy (client);
  mongoc_cleanup ();
}

void insert_loop(char *condstr)
{
  char tmpstr[256];
  extern int yylineno;
  sprintf(tmpstr, "mongodb://%s:27017//", ipaddress);

  mongoc_init ();
  client = mongoc_client_new (tmpstr);
  collection = mongoc_client_get_collection (client, dbname, colname);

  doc = bson_new ();
  bson_oid_init (&oid, NULL);
  BSON_APPEND_OID (doc, "_id", &oid);
  BSON_APPEND_UTF8 (doc, "property", "forloop");
  BSON_APPEND_UTF8 (doc, "file_name", filename);
  BSON_APPEND_UTF8 (doc, "conditions", condstr);
  BSON_APPEND_INT32 (doc, "line_number", current_line_number);

  if (!mongoc_collection_insert (collection, MONGOC_INSERT_NONE, doc, NULL, &error))
    {
	  fprintf (stderr, "%s\n", error.message);
    }

  bson_destroy (doc);

  mongoc_collection_destroy (collection);
  mongoc_client_destroy (client);
  mongoc_cleanup ();
}

void insert_local_variable(char *declstr)
{
  char tmpstr[256];
  extern int yylineno;
  sprintf(tmpstr, "mongodb://%s:27017//", ipaddress);

  mongoc_init ();
  client = mongoc_client_new (tmpstr);
  collection = mongoc_client_get_collection (client, dbname, colname);

  doc = bson_new ();
  bson_oid_init (&oid, NULL);
  BSON_APPEND_OID (doc, "_id", &oid);
  BSON_APPEND_UTF8 (doc, "property", "local_decl");
  BSON_APPEND_UTF8 (doc, "file_name", filename);
  BSON_APPEND_UTF8 (doc, "decls", declstr);
  BSON_APPEND_INT32 (doc, "line_number", current_line_number);

  if (!mongoc_collection_insert (collection, MONGOC_INSERT_NONE, doc, NULL, &error))
    {
	  fprintf (stderr, "%s\n", error.message);
    }

  bson_destroy (doc);

  mongoc_collection_destroy (collection);
  mongoc_client_destroy (client);
  mongoc_cleanup ();
}

void insert_realloc(char *declstr)
{
  char tmpstr[256];
  extern int yylineno;
  sprintf(tmpstr, "mongodb://%s:27017//", ipaddress);

  mongoc_init ();
  client = mongoc_client_new (tmpstr);
  collection = mongoc_client_get_collection (client, dbname, colname);

  doc = bson_new ();
  bson_oid_init (&oid, NULL);
  BSON_APPEND_OID (doc, "_id", &oid);
  BSON_APPEND_UTF8 (doc, "property", "realloc");
  BSON_APPEND_UTF8 (doc, "file_name", filename);
  // BSON_APPEND_UTF8 (doc, "decls", declstr);
  BSON_APPEND_INT32 (doc, "line_number", current_line_number);

  if (!mongoc_collection_insert (collection, MONGOC_INSERT_NONE, doc, NULL, &error))
    {
	  fprintf (stderr, "%s\n", error.message);
    }

  bson_destroy (doc);

  mongoc_collection_destroy (collection);
  mongoc_client_destroy (client);
  mongoc_cleanup ();
}

int main(int argc, char *argv[]) {
    extern int yylineno;
    yyin = stdin;

    yylloc.first_line   = yylloc.last_line   = 1;
    yylloc.first_column = yylloc.last_column = 0;
    
    sprintf(filename,"%s", argv[1]);
    sprintf(dbname,"%s", argv[2]);
    sprintf(colname,"%s", argv[3]);
    sprintf(ipaddress,"%s", argv[4]);
    
    /*
    sprintf(filename,"%s", "test");
    sprintf(dbname,"%s", "sat12");
    sprintf(colname,"%s", "test");
    sprintf(ipaddress,"%s", "192.168.11.2");
    */

    init_tmp_string(tmp_string);
    init_tmp_string(tmp_string_2);
    init_cond_string();

    do {
        yyparse();
    } while(!feof(yyin));
}

void yyerror(const char* s) {
    extern int yylineno;
    //fprintf(stderr, "**ERROR** at nearby line %d: %s\n", yylineno, s);
}

