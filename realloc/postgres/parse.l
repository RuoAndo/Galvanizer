%option noyywrap
%option yylineno

%{
# include <cstdlib>
# include <stdio.h>
# include <cerrno>
# include <climits>
# include <string>

# include "sat-ctx.hh"
# include "parse.tab.hh"

#define YY_DECL int yylex(yy::sat::semantic_type *yylval, \
    yy::sat::location_type *yylloc, sat_ctx &ctx)

// make location include the current token
# define YY_USER_ACTION  yylloc->columns (yyleng);

typedef yy::sat::token token;

%}

%%

%{
     // start where previous token ended
     yylloc->step ();
%}

"realloc" {
     printf("realloc %d \n", yylineno);
     return token::REALLOC;    
}

[a-z0-9][a-z0-9] {
     yylval->string = strdup(yytext);
     // return token::BYTE;    
     // return yytext[0];
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

