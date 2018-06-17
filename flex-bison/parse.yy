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

