//
// Created by atuser on 10/11/19.
//

#ifndef AUTOGENTOO_GLOBALS_H
#define AUTOGENTOO_GLOBALS_H

#include <stdio.h>
#include <autogentoo/hacksaw/map.h>
#include <autogentoo/hacksaw/hacksaw.h>
#include "constants.h"

/* There may be a rule for this */

typedef struct __UseExpand UseExpand;
typedef struct __UseExpandEntry UseExpandEntry;

struct __UseExpandEntry {
	char* flag_name;
	char* description;
};

struct __UseExpand {
	Repository* parent;
	
	char* variable_name;
	Vector* possible_values;
};

Map* use_expand_new(Repository* repo);
void make_conf_parse(Emerge *em);
void make_conf_use(Emerge* em);
void make_conf_add(Map* make_conf, char* key, char* value);

#endif //AUTOGENTOO_GLOBALS_H