#include <iostream>
#include <mongo/client/dbclient.h>
 
int main(void) {
  using namespace std;
  try {

    mongo::client::initialize();
    
    /* connect */
    mongo::DBClientConnection client;
    client.connect("localhost:27017");
 
    /* database: test, collection: users */
    const string ns = "test.users";///
    /* insert */
    /* { "name": "Ryo", "age": 26 } */
    /* { "name": "Ryo", "age": 26, "address": "tokyo" } */
    cout << "--- insert ---" << endl;
    mongo::BSONObjBuilder builder;
    builder.append("name", "Ryo").append("age", 26);  // method chain
    mongo::BSONObj doc = builder.asTempObj();
    cout << doc.toString() << endl;
    client.insert(ns, doc);
    builder.append("address", "tokyo");
    mongo::BSONObj doc2 = builder.obj();
    cout << doc2.toString() << endl;
    client.insert(ns, doc2);
 
    /* find */
    /* { } , fetch all documents */
    cout << "--- find ---" << endl;
    auto_ptr<mongo::DBClientCursor> cursor =
      client.query(ns, mongo::BSONObj()); // represent { }
    while(cursor->more()) {
      mongo::BSONObj p = cursor->next();
      mongo::OID oid = p["_id"].OID();  // retrieve ObjectId
      string name = p["name"].str();  // retrieve string value
      int age = p["age"].numberInt();  // retrieve integer value
      string address = p["address"].str();
      cout << "ObjectId: " << oid << endl;
      cout << "name: " << name << endl;
      cout << "age: " << age << endl;
      cout << "address: " << address << endl;
    }
 
    /* update (using BSON macro) */
    /* { "$set": { "name": "Joe" } } */
    cout << "--- update ---" << endl;
    mongo::Query query(BSON("name" << "Ryo"));
    mongo::BSONObj modifier = BSON("$set" << BSON("name" << "Joe"));
    cout << modifier.toString() << endl;
    client.update(ns, query, modifier,
                  /* upsert */ false, /* multi */ true);
 
    cursor = client.query(ns, mongo::BSONObj());
    while(cursor->more()) {
      mongo::BSONObj p = cursor->next();
      cout << p.toString() << endl; // JSON string output
    }
 
    /* remove */
    /* { "name": "Joe" } */
    cout << "--- remove ---" << endl;
    client.remove(ns, mongo::Query(BSON("name" << "Joe")));
 
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
