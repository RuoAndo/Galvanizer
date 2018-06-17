%option noyywrap
%{
# include <cstdlib>
# include <stdio.h>
# include <cerrno>
# include <climits>
# include <string>
// # include <cstdint>
# include <stdint.h>

# include "sat-ctx.hh"
# include "parse.tab.hh"

#define YY_DECL int yylex(yy::sat::semantic_type *yylval, \
    yy::sat::location_type *yylloc, sat_ctx &ctx)

// make location include the current token
# define YY_USER_ACTION  yylloc->columns (yyleng);

typedef yy::sat::token token;
%}

%option yylineno

%%

%{
     // start where previous token ended
     yylloc->step ();
%}

"for" {
     return yytext[0];
}

";;" {
     return yytext[0];
}

"<=" {
     return yytext[0];
}

"!=" {
     return yytext[0];
}

"++" {
     return yytext[0];
}

"." {
     return token::PERIOD;
}

"(" {
     return token::LP;
}

")" {
     return token::RP;
}

"[" {
     return token::LBK;
}

"]" {
     return token::RBK;
}

"{" {
     return token::LBR;
}

"}" {
     return token::RBR;
}

";" {
     return token::SEMICOLON;
}

"=" {
     return token::EQUAL;
}

"<" {
     return token::LESS_THAN;
}

">" {
     return token::MORE_THAN;
}

[_[:alpha:]][_[:alnum:]]* { 
     // printf("STRING %s\n", strdup(yytext)); 
     // yylval->sval = new std::string(yytext);
     yylval->string = strdup(yytext);
     return token::IDENTIFIER;
}

[0-9*] {
     int n = strtol(yytext, NULL, 10);
     yylval->ival = n;
     return token::NUMBER;
}

\n      {  
          yylloc->lines(1);
          // return token::EOL; 
}

  /* skip over comments and white space */
"//".*  |
[ \t]   {  
           yylloc->step (); 
}

.	{ 
           //printf("Mystery character %c\n", *yytext); 
}


%%

