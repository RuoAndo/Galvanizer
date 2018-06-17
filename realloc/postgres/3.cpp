#include <iostream>
#include <pqxx/pqxx> 
#include <string.h>

using namespace std;
using namespace pqxx;

int main(int argc, char* argv[])
{
   char * sql;

   char tablename[256];
   char sqlstr[256];
   
   sprintf(tablename, "%s", argv[1]);
   
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

      sprintf(sqlstr,"CREATE TABLE %s (REALLOC_LINENUMBER INT NOT NULL, FILENAME CHAR(50), FUNCTION_LINENUMBER CHAR(50));", tablename);
      
      /*
      sql = "CREATE TABLE COMPANY("  \
      "ID INT PRIMARY KEY     NOT NULL," \
      "NAME           TEXT    NOT NULL," \
      "AGE            INT     NOT NULL," \
      "ADDRESS        CHAR(50)," \
      "SALARY         REAL );";
      */

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
