%language "C++"
%defines
%locations

%define "parser_class_name" "sat"

%{
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <string.h>

#include <iostream>

#include <iostream>
#include <mongo/client/dbclient.h>
#include <string>

extern FILE* yyin;

using namespace std;

static int current_line_number = 0;
static char file_name[256];
static char sw_name[256];
static char var_name[256];

#include "sat-ctx.hh"
%}

%parse-param { sat_ctx &ctx }
%lex-param   { sat_ctx &ctx }

%union {
       int ival;
       double dval;
       char *string;
};

/* declare tokens */
%token <ival> NUMBER
%token <dval> DECIMAL
%token <string> REALLOC
%token <string> POINTER
%token <string> STRING
%token <string> EQUAL
%token <string> COMMA
%token <string> SEMICOLON

%{
  extern int yylex(yy::sat::semantic_type *yylval,
       yy::sat::location_type* yylloc,
       sat_ctx &ctx);

  void track_line_number();
  void track_pointer();
  void track_realloc();
%}

%initial-action {
 // Filename for locations here
 @$.begin.filename = @$.end.filename = new std::string("stdin");
}
%%

unit: /* nothing */
| unit realloc { }
| unit pointer { }
;

realloc:
| STRING EQUAL REALLOC
{
  // track_line_number();
  track_realloc();
  printf("[bison] realloc %s = realloc at %d %s \n", $1, current_line_number, file_name);
}

pointer:
| POINTER STRING COMMA
| POINTER STRING SEMICOLON
{
  // track_line_number();
  sprintf(var_name, "%s", $2);
  track_pointer();
  printf("[bison] pointer at %d *%s(%s) \n", current_line_number, $2, $2);
}

;

%%

/*
> use uaf
switched to db uaf
> show collections
realloc
*/

void track_pointer()
{
    mongo::client::GlobalInstance instance;
    mongo::OID::gen();    

    mongo::DBClientConnection client;
    client.connect("127.0.0.1:27017");

    char ns[256];

    sprintf(ns, "uaf.%s", sw_name);

    extern int yylineno;
    current_line_number = yylineno;
    
    mongo::BSONObjBuilder builder;
    builder.append("type", "pointer");
    builder.append("var_name", var_name);
    builder.append("file_name", file_name);
    builder.append("line_number", current_line_number);
    builder.append("file_name", file_name);
    mongo::BSONObj doc = builder.asTempObj();
    // cout << doc.toString() << endl;
    client.insert( ns, doc );    
 
}


void track_realloc()
{
    mongo::client::GlobalInstance instance;
    mongo::OID::gen();    

    mongo::DBClientConnection client;
    client.connect("127.0.0.1:27017");

    char ns[256];

    sprintf(ns, "uaf.%s", sw_name);

    extern int yylineno;
    current_line_number = yylineno;
    
    mongo::BSONObjBuilder builder;
    builder.append("type", "realloc");
    builder.append("file_name", file_name);
    builder.append("line_number", current_line_number);
    builder.append("file_name", file_name);
    mongo::BSONObj doc = builder.asTempObj();
    // cout << doc.toString() << endl;
    client.insert( ns, doc );    
 
}


void track_line_number()
{
    extern int yylineno;
    current_line_number = yylineno; 
}

int main(int argc, char *argv[])
{
  yyin = fopen(argv[1], "r");

  sprintf(file_name,"%s", argv[1]);
  sprintf(sw_name,"%s", argv[2]);

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
  // std::cerr << "error at " << loc << ": " << s << std::endl;
}
}

