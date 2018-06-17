%{
#include <stdio.h>
#include "parse.tab.h"

// #include "parse.h"

%}
%option yylineno
%x COMMENT

%%

"/*"           { BEGIN(COMMENT) ; }
<COMMENT>"*/"  { BEGIN(INITIAL); }
<COMMENT>([^*]|\en)+|.

"realloc" {
      return yytext[0]; 
}

"for" {
      // printf("for \n");
      return yytext[0]; 
}

"int" {
      return yytext[0]; 
}

"=" { 
      // printf("equal \n");
      return yytext[0]; 
}

"++" { 
     // printf("increment \n");
     return yytext[0]; 
}

"<" |
">" { return yytext[0]; }


"(" |
")" { return yytext[0]; }

"{" |
"}" { return yytext[0]; }


"," { 
    return yytext[0];
}

";" { 
    return yytext[0];
}

":" { 
    return yytext[0];
}

"*" { 
    return yytext[0];
}

"&" { 
    return yytext[0];
}

"\n" { 
    return yytext[0];
}

[\n][a-zA-Z_][a-zA-Z_0-9]* {
    yylval.string = strdup(yytext);
    return DECL; 
}

[a-zA-Z_][a-zA-Z_0-9]* {
    yylval.string = strdup(yytext);
    return STRING; 
}

[0-9*] {
    int n = strtol(yytext, NULL, 10);
    yylval.ival = n;
    return NUMBER;
}

. {}

[\n][ \s.] {
   // printf("SPACES \n");
   return SPACES;
}

%%

