#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include "timer.h"

static unsigned int travfiletime = 0;
static unsigned int travbufftime = 0;

typedef struct _result {
    int num;
    char* fname;
} result_t;
result_t result;

int traverse_buffer(char* a, char* b) {
    int i, j;
    int lena, lenb;
    int n = 0;

    lena = strlen(a);
    lenb = strlen(b);

    for (i = 0, j = 0; i < lena; ++i) {
        if (strncmp(&a[i], &b[j], 1) == 0) {
            if (j == (lenb-1)) {
                n++; j = 0;
            } else {
                j++;
            }
        } else {
            j = 0;
        }
    }

    return n;
}

int traverse_file(char* filename, char* srchstr) {
    char buf[1024];
    int n = 0, sumn = 0;
    unsigned int t;

    FILE* fd;
    if ((fd = fopen(filename, "r")) == NULL) {
        printf("file %s not found.\n", filename);
        return 0;
    }

    while (fgets(buf, 1024, fd) != NULL) {
#ifdef DEBUG
        start_timer(&t);
#endif
        n = traverse_buffer(buf, srchstr);
#ifdef DEBUG
        travbufftime += stop_timer(&t);
#endif
        sumn += n;
        //	if (n > 0) printf("%s[L%d][n=%d]: %s", filename, ++line, n, buf);
    }

    fclose(fd);
    return sumn;
}

void traverse_dir(char* dirname, char* srchstr, int* filenum) {
    struct dirent* dent;
    DIR* dd = opendir(dirname);
    unsigned int t;

    if (dd == NULL) {
        printf("Could not open the directory %s\n", dirname); return;
    }

    while ((dent = readdir(dd)) != NULL) {
        if (strncmp(dent->d_name, ".",  2) == 0) continue;
        if (strncmp(dent->d_name, "..", 3) == 0) continue;

        int size = strlen(dirname)+strlen(dent->d_name)+2;
        char* path = (char*)malloc(size);
        sprintf(path, "%s/%s", dirname, dent->d_name);

        struct stat fs;
        if (stat(path, &fs) < 0)
            continue;
        else {
            if (S_ISDIR(fs.st_mode))
                traverse_dir(path, srchstr, filenum);
            else if (S_ISREG(fs.st_mode)) {
#ifdef DEBUG
                start_timer(&t);
#endif
                int n = traverse_file(path, srchstr);
#ifdef DEBUG
                travfiletime += stop_timer(&t);
#endif
                if (n > result.num) {
                    result.num = n;
                    if (result.fname != NULL) free(result.fname);
                    result.fname = (char*)malloc(size);
                    strcpy(result.fname, path);    
                }
                (*filenum)++;
            }
        }
    }
    closedir(dd);
    return;
}

void print_result(int filenum) {
    if (result.num) {
        printf("Total %d files\n", filenum);
        printf("Max include file: %s[include %d]\n", result.fname, result.num);
    }
    return;
}

int main(int argc, char* argv[]) {
    int filenum;
    char* dirname;
    char* srchstr;
    unsigned int t, travdirtime;

    if (argc != 3) {
        printf("Usage: search_strings PATTERN [DIR]\n"); return 0;
    }
    filenum = 0;

    srchstr = (char*)argv[1];
    dirname = (char*)argv[2];

    result.num = 0;
    result.fname = NULL;

    start_timer(&t);
    traverse_dir(dirname, srchstr, &filenum);
    travdirtime = stop_timer(&t);

#ifdef DEBUG
    print_timer(travbufftime);
    print_timer(travfiletime);
#endif
    print_timer(travdirtime);

    print_result(filenum);

    if(result.fname != NULL) free(result.fname);

    return 0;
}
