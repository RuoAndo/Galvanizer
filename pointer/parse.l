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

[a-zA-z][a-zA-Z_0-9]+ { 
     // printf("STRING %s\n", strdup(yytext)); 
     // yylval->sval = new std::string(yytext);
     yylval->string = strdup(yytext);
     return token::IDENTIFIER;
}

"*" { 
     // printf("star \n");
     // yylval->string = strdup(yytext); 
     return token::STAR;
}

"=" {
     return token::EQUAL;
}

"(" {
     return token::LPAREN;
}

")" {
     return token::RPAREN;
}

"\/" {
     return token::SLASH;
}

\n      {  
          yylloc->lines(1);
          //return token::EOL; 
}

 /* skip over comments and white space */
"//".*  |
[ \t]   {  
           yylloc->step (); 
}

.	{ 
           //printf("unknown character %c\n", *yytext); 
}


%%

