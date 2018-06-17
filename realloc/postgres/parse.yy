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
#include <pqxx/pqxx> 

extern FILE* yyin;

using namespace std;
using namespace pqxx;

static int current_line_number = 0;
static char file_name[256];
static char swname[256];

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

%{
  extern int yylex(yy::sat::semantic_type *yylval,
       yy::sat::location_type* yylloc,
       sat_ctx &ctx);

  static int track_line_number();
%}

%initial-action {
 // Filename for locations here
 @$.begin.filename = @$.end.filename = new std::string("stdin");
}
%%

unit: /* nothing */
| unit realloc { }
;

realloc:
| REALLOC
{
  track_line_number();
  printf("bison realloc at %d %s \n", current_line_number, file_name);
}
;

%%

static int track_line_number()
{
    extern int yylineno;
    char * sql;

    char sqlstr[256];

    current_line_number = yylineno; 

    printf("realloc at %d %s %s \n", current_line_number, file_name, swname);

   try{
      connection C("dbname=realloc user=postgres password=cohondob \
      hostaddr=127.0.0.1 port=5432");
      if (C.is_open()) {
         cout << "Opened database successfully: " << C.dbname() << endl;
      } else {
         cout << "Can't open database" << endl;
         return 1;
      }
      
      /* Create SQL statement */
      /*
      sql = "CREATE TABLE TEST("  \
      "REALLOC_LINENUMBER     INT     NOT NULL," \
      "FILENAME           CHAR(50)," \
      "FUNCTION_LINENUMBER CHAR(50));";
      */

      /*
      sprintf(sqlstr,"CREATE TABLE %s (REALLOC_LINENUMBER INT NOT NULL, FILENAME CHAR(50), FUNCTION_LINENUMBER CHAR(50));", swname);
      */

      sprintf(sqlstr, "INSERT INTO %s (REALLOC_LINENUMBER, FILENAME) VALUES ('%d', '%s') ; ", swname, current_line_number, file_name);

      printf("%s \n", sqlstr);
      // strcpy(sql, sqlstr);
      // printf("%s \n", sql);
      
      /* Create a transactional object. */
      work W(C);
      
      /* Execute SQL query */
      W.exec( sqlstr );
      W.commit();
      cout << "Table created successfully" << endl;
      C.disconnect ();
   }catch (const std::exception &e){
      cerr << e.what() << std::endl;
      return 1;
   }

   return 0;


}

int main(int argc, char *argv[])
{
  yyin = fopen(argv[1], "r");

  sprintf(file_name,"%s", argv[1]);
  sprintf(swname,"%s", argv[2]);

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

