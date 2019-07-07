#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <pthread.h>
#include <alloca.h>
#include "timer.h"

#include <regex.h>

#include<sys/ioctl.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#include<linux/if.h>
#include<net/ethernet.h>
#include<netpacket/packet.h>
#include<netinet/if_ether.h>
#include<netinet/ip.h>
#include<netinet/ip6.h>
#include<netinet/ip_icmp.h>
#include<netinet/icmp6.h>
#include<netinet/tcp.h>
#include<netinet/udp.h>

#include <map>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <bitset>

#include <cstdio>
#include <cctype>
#include <iostream>

#include "tbb/concurrent_hash_map.h"
#include "tbb/blocked_range.h"
#include "tbb/parallel_for.h"
#include "tbb/tick_count.h"
#include "tbb/task_scheduler_init.h"
#include "tbb/concurrent_vector.h"
//  #include "tbb/tbb_allocator.hz"
#include "utility.h"

#include "csv.hpp"

using namespace std;
using namespace tbb;

#define N 3
#define WORKER_THREAD_NUM N
#define MAX_QUEUE_NUM N
#define END_MARK_FNAME   "///"
#define END_MARK_FLENGTH 3

#define DISP_FREQ 100000

typedef concurrent_hash_map<string, std::vector<int>> global_tx_lineNumber;
static global_tx_lineNumber table_tx_lineNumber;

typedef concurrent_hash_map<string, std::vector<string>> global_tx_funcName;
static global_tx_funcName table_tx_funcName;

typedef concurrent_hash_map<string, std::vector<int>> global_rx_lineNumber;
static global_rx_lineNumber table_rx_lineNumber;

typedef concurrent_hash_map<string, std::vector<string>> global_rx_funcName;
static global_rx_funcName table_rx_funcName;   

typedef struct _result {
    int num;
    char* fname;
    pthread_mutex_t mutex;    
} result_t;
result_t result;

typedef struct _queue {
    char* fname[MAX_QUEUE_NUM];
    int flength[MAX_QUEUE_NUM];
    int rp, wp;
    int remain;
    pthread_mutex_t mutex;
    pthread_cond_t not_full;
    pthread_cond_t not_empty;
} queue_t;

typedef struct _thread_arg {
    int id;
    int cpuid;
    queue_t* q;
    char* srchstr;
    char* dirname;
    int filenum;
} thread_arg_t;

int traverse_file(char* filename, char* srchstr, int thread_id) {

  const string csv_file_1 = std::string(filename); 
  vector<vector<string>> data_1; 

  tbb::tick_count mainStartTime = tbb::tick_count::now();
    
  try {
    Csv objCsv2(csv_file_1);
    if (!objCsv2.getCsv(data_1)) {
      cout << "read ERROR" << endl;
      return 1;
    }

    // cout << data_1.size() << endl;
    for (unsigned int row = 0; row < data_1.size(); row++) {
         vector<string> rec_rx = data_1[row]; 
	 std::string path_rx = rec_rx[2];
	    	    	    
	 global_rx_lineNumber::accessor rx_lineNumber;
	 table_rx_lineNumber.insert(rx_lineNumber, path_rx);
	 rx_lineNumber->second.push_back(stoi(rec_rx[1]));	    

	 global_rx_funcName::accessor rx_funcName;
	    table_rx_funcName.insert(rx_funcName, path_rx);
	    rx_funcName->second.push_back(rec_rx[0]);	    
    }
  }
  catch (...) {
    cout << "EXCEPTION!" << endl;
    return 1;
  }

  // cout << table_rx_lineNumber.size() << endl;

  /*
    counter = 0;
    for( global_tx_lineNumber::iterator i=table_tx_lineNumber.begin(); i!=table_tx_lineNumber.end(); ++i )
      {
	    for(auto itr = i->second.begin(); itr != i->second.end(); ++itr) 
	      counter++;
      }
    cout << "table_tx_lineNumber->second :" << counter << endl;   
    cout << table_tx_funcName.size() << endl;
  */

  cout << "threadID:" << thread_id << ":" << filename << ":" << table_rx_lineNumber.size() << endl;  
  utility::report_elapsed_time((tbb::tick_count::now() - mainStartTime).seconds());
  
  return 0;
}

void initqueue(queue_t* q) {
    int i;
    q->rp = q->wp = q->remain= 0;
    for (i = 0; i < MAX_QUEUE_NUM; ++i) q->fname[i] = NULL;
    pthread_mutex_init(&q->mutex,    NULL);
    pthread_cond_init(&q->not_full,  NULL);
    pthread_cond_init(&q->not_empty, NULL);
    return;
}

void enqueue(queue_t* q, char* path, int size) {
  
    pthread_mutex_lock(&q->mutex);
    while (q->remain == MAX_QUEUE_NUM) {
        pthread_cond_wait(&q->not_full, &q->mutex);
    }
    char** fname = (char**)&q->fname[q->wp];
    if (*fname != NULL) free(*fname);
    *fname = (char*)malloc(size);
    strcpy(*fname, path);
    q->flength[q->wp] = size;
    q->wp++; q->remain++;

    if (q->wp == MAX_QUEUE_NUM) q->wp = 0;

    pthread_cond_signal(&q->not_empty);
    pthread_mutex_unlock(&q->mutex);
    return;
}

void dequeue(queue_t* q, char** fname, int* flen) {

    pthread_mutex_lock(&q->mutex);
    while (q->remain == 0) 
        pthread_cond_wait(&q->not_empty, &q->mutex);

    *flen  = q->flength[q->rp];
    if (*fname != NULL) free(*fname);
    *fname = (char*)malloc(*flen);
    strcpy(*fname, q->fname[q->rp]);
    q->rp++; q->remain--;
    if (q->rp == MAX_QUEUE_NUM) q->rp = 0;
    pthread_cond_signal(&q->not_full);
    pthread_mutex_unlock(&q->mutex);
    if (strcmp(*fname,"")==0) printf("rp=%d\n", q->rp-1);
    return;
}

int traverse_dir_thread(queue_t* q, char* dirname) {
    static int cnt = 0;
    struct dirent* dent;
    DIR* dd = opendir(dirname);

    if (dd == NULL) {
        printf("Could not open the directory %s\n", dirname); return 0;
    }

    while ((dent = readdir(dd)) != NULL) {
        if (strncmp(dent->d_name, ".",  2) == 0) continue;
        if (strncmp(dent->d_name, "..", 3) == 0) continue;	

        int size = strlen(dirname) + strlen(dent->d_name) + 2;
#if 0
        char* path = (char*)malloc(size);
        sprintf(path, "%s/%s", dirname, dent->d_name);

        struct stat fs;
        if (stat(path, &fs) < 0)
            continue;
        else {
            if (S_ISDIR(fs.st_mode))
                traverse_dir_thread(q, path);
            else if (S_ISREG(fs.st_mode)) {
                enqueue(q, path, size);
                cnt++;
            }
        }
#else
        {
            char* path = (char*)alloca(size);
            sprintf(path, "%s/%s", dirname, dent->d_name);

            struct stat fs;
            if (stat(path, &fs) < 0)
                continue;
            else {
                if (S_ISDIR(fs.st_mode))
                    traverse_dir_thread(q, path);
                else if (S_ISREG(fs.st_mode)) {
                    enqueue(q, path, size);
                    cnt++;
                }
            }
        }
#endif
    }
    closedir(dd);
    return cnt;
}

void master_func(thread_arg_t* arg) {
    queue_t* q = arg->q;
    int i;
    arg->filenum = traverse_dir_thread(q, arg->dirname);

    /* enqueue END_MARK */
    for (i = 0; i < WORKER_THREAD_NUM; ++i) 
        enqueue(q, END_MARK_FNAME, END_MARK_FLENGTH);
    return;
}

void worker_func(thread_arg_t* arg) {
    int flen;
    char* fname = NULL;
    queue_t* q = arg->q;
    char* srchstr = arg->srchstr;

    int thread_id = arg->id;

    printf("worker func %d launched \n", thread_id);
    
#ifdef __CPU_SET
    cpu_set_t mask;    
    __CPU_ZERO(&mask);
    __CPU_SET(arg->cpuid, &mask);
    if (sched_setaffinity(0, sizeof(mask), &mask) == -1)
        printf("WARNING: faild to set CPU affinity...\n");
#endif

#if 0
    while (1) {
        int n;

        dequeue(q, &fname, &flen));

        if (strncmp(fname, END_MARK_FNAME, END_MARK_FLENGTH + 1) == 0)
            break;

        n = traverse_file(fname, srchstr, thread_id);
        pthread_mutex_lock(&result.mutex);

        if (n > result.num) {
            result.num = n;
            if (result.fname != NULL) free(result.fname);
            result.fname = (char*)malloc(flen);
            strcpy(result.fname, fname);
        }
        pthread_mutex_unlock(&result.mutex);
    }
#else
    char* my_result_fname;
    int my_result_num = 0;
    int my_result_len = 0;
    while (1) {
        int n;

        dequeue(q, &fname, &flen);

        if (strncmp(fname, END_MARK_FNAME, END_MARK_FLENGTH + 1) == 0)
            break;

        n = traverse_file(fname, srchstr, thread_id);

        if (n > my_result_num) {
            my_result_num = n;
            my_result_len = flen;
            my_result_fname = (char*)alloca(flen);
            strcpy(my_result_fname, fname);
        }
    }
    pthread_mutex_lock(&result.mutex);
    if (my_result_num > result.num) {
        result.num = my_result_num;
	if (result.fname != NULL) free(result.fname);
        result.fname = (char*)malloc(my_result_len);
        strcpy(result.fname, my_result_fname);	
    }
    pthread_mutex_unlock(&result.mutex);
#endif
    return;
}

void print_result(thread_arg_t* arg) {
    if (result.num) {
        printf("Total %d files\n", arg->filenum);
        printf("Max include file: %s[include %d]\n", result.fname, result.num);	
    }
    return;
}

int main(int argc, char* argv[]) {
    int i;
    int thread_num = 1 + WORKER_THREAD_NUM;
    unsigned int t, travdirtime;
    queue_t q;
    
    thread_arg_t targ[thread_num];
    pthread_t master;
    pthread_t worker[thread_num];
    
    int cpu_num;
    int counter;
    
    if (argc != 3) {
        printf("Usage: ./traverse [DIR] FILENAME \n"); return 0;
    }
    cpu_num = sysconf(_SC_NPROCESSORS_CONF);

    initqueue(&q);

    for (i = 0; i < thread_num; ++i) {
        targ[i].q = &q;
        targ[i].dirname = argv[1];
        targ[i].filenum = 0;
        targ[i].cpuid = i%cpu_num;
    }
    result.fname = NULL;

    // parsing global tx
    // scsi_request,9,linux/include/scsi/scsi_request.h	  
    // std::replace(path_tx.begin(), path_tx.end(), '/', '|');

    const string csv_file_2 = std::string(argv[2]); 
    vector<vector<string>> data_2; 

    tbb::tick_count mainStartTime = tbb::tick_count::now();
    
    try {
	  Csv objCsv2(csv_file_2);
	  if (!objCsv2.getCsv(data_2)) {
	    cout << "read ERROR" << endl;
	    return 1;
	  }

	  cout << data_2.size() << endl;
	  for (unsigned int row = 0; row < data_2.size(); row++) {
	    vector<string> rec_tx = data_2[row]; 
	    std::string path_tx = rec_tx[2];
	    	    	    
	    global_tx_lineNumber::accessor tx_lineNumber;
	    table_tx_lineNumber.insert(tx_lineNumber, path_tx);
	    tx_lineNumber->second.push_back(stoi(rec_tx[1]));	    

	    global_tx_funcName::accessor tx_funcName;
	    table_tx_funcName.insert(tx_funcName, path_tx);
	    tx_funcName->second.push_back(rec_tx[0]);	    
	  }
    }
    catch (...) {
      cout << "EXCEPTION!" << endl;
      return 1;
    }

    cout << table_tx_lineNumber.size() << endl;

    counter = 0;
    for( global_tx_lineNumber::iterator i=table_tx_lineNumber.begin(); i!=table_tx_lineNumber.end(); ++i )
      {
	    for(auto itr = i->second.begin(); itr != i->second.end(); ++itr) 
	      counter++;
      }
    cout << "table_tx_lineNumber->second :" << counter << endl;   
    cout << table_tx_funcName.size() << endl;
    
    utility::report_elapsed_time((tbb::tick_count::now() - mainStartTime).seconds());
    
    pthread_mutex_init(&result.mutex, NULL);
    
    pthread_create(&master, NULL, (void*)master_func, (void*)&targ[0]);
    for (i = 1; i < thread_num; ++i)
      { 
        targ[i].id = i;
        pthread_create(&worker[i], NULL, (void*)worker_func, (void*)&targ[i]);
      }
    
    for (i = 1; i < thread_num; ++i) 
        pthread_join(worker[i], NULL);
 
    return 0;
}
