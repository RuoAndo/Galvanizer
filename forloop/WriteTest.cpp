#include <cstdlib>
#include <iostream>
#include "mongo/client/dbclient.h"

int main() {

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
