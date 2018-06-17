%language "C++"
%defines
%locations

%define "parser_class_name" "sat"

%{
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>

#include <bson.h>
#include <mongoc.h>

mongoc_client_t *client;
mongoc_collection_t *collection;
mongoc_cursor_t *cursor;
bson_error_t error;
bson_oid_t oid;
bson_t *doc;

extern FILE* yyin;

using namespace std;
static int current_line_number = 0;

#include "sat-ctx.hh"
%}

%parse-param { sat_ctx &ctx }
%lex-param   { sat_ctx &ctx }

%union {
       int ival;
       char *string;
};

/* declare tokens */
%token <ival> NUMBER
%token ADD SUB MUL DIV ABS
%token OP CP COMMA
%token OB CB SEMICOLON
%token EOL
%token EQ
%token REF
%token NUMBER
%token INV

%token <string> IDENTIFIER "identifier"
%token STAR
%token SIZEOF

// %type <ival> exp factor term

%{
  extern int yylex(yy::sat::semantic_type *yylval,
       yy::sat::location_type* yylloc,
       sat_ctx &ctx);

  char term_string[1024];
  char arg_string[1024];

  char backup_string[1024];
  char backup_string_2[1024];

  void init_string(char *tmp_string);
  void track_line_number();
%}

%initial-action {
 // Filename for locations here
 @$.begin.filename = @$.end.filename = new std::string("stdin");
}
%%

unit: /* nothing */
| unit term { }
| unit arg { }
| unit decl { } 
| unit assign { } 
| unit cond { } 
;

decl: arg SEMICOLON { 
     printf("decl \n");
}
| term SEMICOLON{
     printf("decl \n");
}
;

assign: term EQ term SEMICOLON {
   	printf("assign term \n");
}
|
term EQ NUMBER SEMICOLON {
        // yylval->ival = myatoi(ctx.getradix(), yytext); return token::NUMBER;
   	printf("assign NUMBER \n");
}

arg: OP term CP
| OP term COMMA term CP { 
  sprintf(arg_string,"%s,%s",backup_string, backup_string_2);
  printf("arg %s \n", arg_string);

  init_string(backup_string);
  init_string(backup_string_2);
}
;

cond: OP assign { 
  printf("condtion \n");
} 
;

term:
| term string string { 
  printf("term %s @ %d \n", term_string, current_line_number); 
  ctx.test(term_string, current_line_number);

  //printf("ctx.list() \n");
  //ctx.list();

  sprintf(backup_string_2, "%s", backup_string);
  sprintf(backup_string, "%s", term_string);

  init_string(term_string);
}
| term REF term 
{
	printf("term ref term \n");
}
| COMMA { printf("COMMA \n");}
| OP { printf("OP \n");}
| CP { printf("CP \n");}
| OB { printf("OB \n");}
| CB { printf("CB \n");}
| SEMICOLON { printf("SEMICOLON \n");}
| NUMBER { printf("NUMBER \n");}
;

string:
| "identifier" { 
  // printf("identifier %s \n", $1);
  track_line_number();

  sprintf(term_string, "%s %s", term_string, $1);
  }
| STAR "identifier" { 
  // printf("pointer *%s\n", $2);
  track_line_number();

  sprintf(term_string, "%s *%s", term_string, $2);
  }
;

%%

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

void track_line_number()
{
    extern int yylineno;
    current_line_number = yylineno;
}

void init_string(char *tmp_string)
{
  int i;

      for(i=0; i<1024; i++)
        {
		tmp_string[i] = 0;
    	}
}

main()
{
  yyin = stdin;

  sat_ctx ctx(8);    

 do {
    yy::sat parser(ctx); // make a sat parser
    int v = parser.parse();  // and run it
    // return v;
 } while(!feof(yyin));

}

namespace yy {
void
sat::error(location const &loc, const std::string& s)
{
  std::cerr << "error at " << loc << ": " << s << std::endl;
}
}

