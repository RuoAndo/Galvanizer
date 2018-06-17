%language "C++"
%defines
%locations

%define "parser_class_name" "sat"

%{
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>

extern FILE* yyin;

using namespace std;
static int current_line_number = 0;
static char filename[256];

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

%token <string> IDENTIFIER "identifier"
%token STAR
%token EQUAL

%token LPAREN
%token RPAREN

%token SLASH

%{
  extern int yylex(yy::sat::semantic_type *yylval,
       yy::sat::location_type* yylloc,
       sat_ctx &ctx);

  void init_string(char *tmp_string);
  void track_line_number();
%}

%initial-action {
 // Filename for locations here
 @$.begin.filename = @$.end.filename = new std::string("stdin");
}
%%

unit: /* nothing */
| unit statement{ }
;

statement:
| "identifier" { 
  // printf("identifier %s \n", $1);
  track_line_number();
  }
| STAR "identifier" EQUAL {
  track_line_number();
  // printf("pointer *%s at %d - %s \n", $2, current_line_number, filename);
  printf("*%s,%d,%s\n", $2, current_line_number, filename);
  }
;

comment:
| STAR "identifier" STAR {
}
;

%%

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

int main(int argc,char *argv[])
{
  yyin = stdin;

  sat_ctx ctx(8);    

  if(argc < 2)
  {
	printf("error argc \n");
	return 0;
  }
  
  // printf("%s \n", argv[1]);
  sprintf(filename, "%s", argv[1]);

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

