%language "C++"
%defines
%locations

%define "parser_class_name" "sat"

%{
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>

#include <mongo/client/dbclient.h> 

extern FILE* yyin;

using namespace std;
static int current_line_number = 0;
static char location[256];

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
%token LP
%token RP
%token LBK
%token RBK
%token LBR
%token RBR
%token SEMICOLON
%token EQUAL
%token PERIOD
%token LESS_THAN
%token MORE_THAN

%{
  extern int yylex(yy::sat::semantic_type *yylval,
       yy::sat::location_type* yylloc,
       sat_ctx &ctx);

void track_line_number()
{
    extern int yylineno;
    current_line_number = yylineno;
}

int insertTest(char *type2, int linenumber)
{

  char type[256];
  sprintf(type, "%s", type2); 

  using namespace std;
  try {

    mongo::client::initialize();
    
    /* connect */
    mongo::DBClientConnection client;
    client.connect("localhost:27017");
 
    /* database: test, collection: users */
    const string ns = "sat.looptype";///
    /* insert */
    /* { "name": "Ryo", "age": 26 } */
    /* { "name": "Ryo", "age": 26, "address": "tokyo" } */
    cout << "--- insert ---" << endl;
    mongo::BSONObjBuilder builder;
    // builder.append("name", "Ando").append("age", 26);  // method chain
    // builder.append("name", name).append("age", 26);  // method chain
    builder.append("type", type).append("linenumber", linenumber).append("location", location);  // method chain

    mongo::BSONObj doc = builder.asTempObj();
    cout << doc.toString() << endl;
    client.insert(ns, doc);

    /*
    builder.append("address", "tokyo");
    mongo::BSONObj doc2 = builder.obj();
    cout << doc2.toString() << endl;
    client.insert(ns, doc2);
    */

  } catch(const mongo::ConnectException& e) {
    cerr << "connect error" << endl;
    cerr << e.getCode() << endl;
    cerr << e.what() << endl;
  } catch(const mongo::DBException& e) {
    cerr << e.getCode() << endl;
    cerr << e.what() << endl;
  }
  return 0;
}

%}

%initial-action {
 // Filename for locations here
 @$.begin.filename = @$.end.filename = new std::string("stdin");
}
%%

input
: input line
    | line
;

line:
| string
| loop1
| loop2
| loop3
| loop4
| loop5
;

string:
| "identifier" {
  // printf("string %s \n", $1);
  }
;

// for (i = 0; i <= tinfo.max_cpu_index; i++)
loop1:
| 'for' LP string EQUAL NUMBER SEMICOLON string '<=' string PERIOD string SEMICOLON string '++' RP {
  track_line_number();
  printf("forloop detected with type 1 on bison %d \n", current_line_number);
  insertTest("type1", current_line_number);
}
;

// for (i = 0; i < num; i++)
loop2:
| 'for' LP string EQUAL NUMBER SEMICOLON string LESS_THAN string SEMICOLON string '++' RP {
  track_line_number();
  printf("forloop detected with type 2 on bison %d \n", current_line_number);
  insertTest("type2", current_line_number);
}
;

// for (i = 0; sl[i] != NULL; i++)
loop3:
| 'for' LP string EQUAL NUMBER SEMICOLON string LBK string RBK '!=' string SEMICOLON string '++' RP {
  track_line_number();
  printf("forloop detected with type 3 on bison %d \n", current_line_number);
  insertTest("type3", current_line_number);
}
;

// for (index = i = 0; i < ret; i++)
loop4:
| 'for' LP string EQUAL string EQUAL NUMBER SEMICOLON string LESS_THAN string SEMICOLON string '++' RP {
  track_line_number();
  printf("forloop detected with type 4 on bison %d \n", current_line_number);
  insertTest("type4", current_line_number);
}
;

// for (i = 0;; i++) {
loop5:
| 'for' LP string EQUAL NUMBER ';;' string '++' RP {
  track_line_number();
  printf("forloop detected with type 5 on bison %d \n", current_line_number);
  insertTest("type5", current_line_number);
}
;

%%

int mongo_writeTest()
{
 mongo::client::initialize();

    try {

        mongo::DBClientConnection client;
	        client.connect( "localhost" );

        //name（値）
	        mongo::BSONObjBuilder builder;
		        builder.append( "name", "today" );

        //value（配列）
	        mongo::BSONArrayBuilder value_array;
		        int i, values[] = { 21, 28, 25, 26, 27, 34 };

        for( i = 0; i < 6; ++i ) {
	            value_array.append( values[i] );
		            }

        builder.append( "value",  value_array.arr() );

        //データの挿入
	        mongo::BSONObj obj = builder.obj();
		        client.insert( "sample.test", obj );

    } catch( const mongo::DBException &e ) {

        std::cout << "caught " << e.what() << std::endl;

    }

    return EXIT_SUCCESS;
}

int main(int argc, char *argv[]) 
{
  yyin = stdin;

  sprintf(location,"%s",argv[1]);

  sat_ctx ctx(8);    

  // mongo_writeTest();

  // char *name = "ando";
  // insertTest(name);

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

