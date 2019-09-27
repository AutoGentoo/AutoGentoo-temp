//
// Created by atuser on 9/24/19.
//

#ifndef AUTOGENTOO_SET_H
#define AUTOGENTOO_SET_H

#include "vector.h"

typedef struct __Set Set;
typedef int (*element_cmp) (void*, void*);

struct __Set {
	Vector* parent;
	element_cmp cmp_func;
};

Set* set_new(element_cmp cmp_func);
void set_add(Set* set, void* element);
void* set_get(Set* s, int i);
int set_inside(Set* s, void* item);
Set* set_dup(Set* s);
void set_union(Set* s1, Set* s2);
Set* set_collapse(Set* to_collapse, void* (*merge_func)(void*, void*));
void set_free(Set* ptr);

#endif //AUTOGENTOO_SET_H
