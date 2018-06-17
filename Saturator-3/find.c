#include <bson.h>
#include <bcon.h>
#include <mongoc.h>
#include <stdio.h>
#include <stdlib.h>

int main( void ){
  mongoc_client_t *     conn    = NULL;
  mongoc_collection_t * coll    = NULL;
  mongoc_cursor_t *     cusr    = NULL;
  const bson_t *        doc     = NULL;
  char *                ret_str = NULL;
  bson_t                query;
  // DB接続
  conn = mongoc_client_new (
             "mongodb://192.168.11.4:27017/"  // 接続先URI
         );
  if( NULL == conn ){
    // error
    exit(-1);
  }
  // データ取得
  coll = mongoc_client_get_collection (
           conn   ,    // コネクション
           "xen_4_1_2" , // DB名
           "caller"   // コレクション名
         );
  if( NULL == coll ){
    // error
    mongoc_client_destroy ( conn );
    exit(-1);
  }
  bson_init (&query);
  cusr = mongoc_collection_find (
           coll              , // コレクション
           MONGOC_QUERY_NONE , // mongoc_query_flags_t(検索条件なしを指定)
           0                 , // 開始位置(最初から取得)
           0                 , // 最大取得数(全て取得)
           0                 , // batchサイズ( default指定(=100) )
           &query            , // クエリ(指定なし)
           NULL              , // フィールド(全てを対象)
           NULL                // 取得クラスタ(default指定(=プライマリから取得))
         );
  if( NULL == cusr ){
    // error
    mongoc_client_destroy ( conn );
    bson_destroy (&query);
    exit(-1);
  }
  while (mongoc_cursor_next ( cusr , &doc ) ) {
    ret_str = bson_as_json ( doc , NULL );
    printf ( "%s\n", ret_str );
    bson_free ( ret_str );
  }
  // 後片づけ
  mongoc_collection_destroy( coll );
  mongoc_client_destroy ( conn );
  bson_destroy (&query);
  return 0;
}

