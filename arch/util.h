//
// Created by atuser on 1/6/18.
//

#ifndef AUTOGENTOO_UTIL_H
#define AUTOGENTOO_UTIL_H

#include <stdio.h>
#include "aabs.h"
#include <archive.h>

void _aabs_alloc_fail(size_t size);

#define MALLOC(p, s, action) do { p = malloc(s); if(p == NULL) { _aabs_alloc_fail(s); action; } } while(0)
#define CALLOC(p, l, s, action) do { p = calloc(l, s); if(p == NULL) { _aabs_alloc_fail(l * s); action; } } while(0)
/* This strdup macro is NULL safe- copying NULL will yield NULL */
#define STRDUP(r, s, action) do { if(s != NULL) { r = strdup(s); if(r == NULL) { _aabs_alloc_fail(strlen(s)); action; } } else { r = NULL; } } while(0)
#define STRNDUP(r, s, l, action) do { if(s != NULL) { r = strndup(s, l); if(r == NULL) { _aabs_alloc_fail(l); action; } } else { r = NULL; } } while(0)

#define FREE(p) do { if (p) free(p); p = NULL; } while(0)

#define ASSERT(cond, action) do { if(!(cond)) { action; } } while(0)

void* aabs_read_archive (aabs_filelist_t* dest, struct archive** ar, char* file_path, int close);
aabs_time_t _aabs_parsedate (const char* line);
off_t _aabs_str_to_off_t(const char *line);

#endif //AUTOGENTOO_UTIL_H
