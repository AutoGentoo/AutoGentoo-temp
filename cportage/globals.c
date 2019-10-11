//
// Created by atuser on 10/11/19.
//

#define _GNU_SOURCE

#include <stdio.h>
#include "globals.h"
#include "directory.h"
#include "portage.h"
#include "emerge.h"
#include <string.h>
#include <ctype.h>
#include <share.h>

char* strupr(char* str) {
	for (char* c = str; *c; c++)
		*c = (char)toupper(*c);
	return str;
}

char* strlwr(char* str);

Map* use_expand_new(Repository* repo) {
	char* use_expand_location = NULL;
	asprintf(&use_expand_location, "%s/profiles/desc", repo->location);
	
	FPNode* use_expand_dir = open_directory(use_expand_location);
	free(use_expand_location);
	
	Map* out = map_new(128, 0.8);
	
	for (FPNode* dir = use_expand_dir; dir; dir = dir->next) {
		char* dot_split = strchr(dir->filename, '.');
		char* key_name = strndup(dir->filename, dot_split - dir->filename);
		
		UseExpand* el = malloc(sizeof(UseExpand));
		el->parent = repo;
		el->variable_name = strupr(key_name);
		el->possible_values = vector_new(VECTOR_UNORDERED | VECTOR_REMOVE);
		
		map_insert(out, el->variable_name, el);
		
		FILE* fp = fopen(dir->path, "r");
		char* line = NULL;
		size_t line_size = 0;
		while (getline(&line, &line_size, fp) > 0) {
			if (line[0] == '#')
				continue;
			char* name_tok = strtok(line, " - ");
			if (!name_tok)
				continue;
			char* desc_tok = strtok(NULL, "\n");
			if (!desc_tok)
				continue;
			
			UseExpandEntry* entry = malloc(sizeof(UseExpandEntry));
			entry->flag_name = strdup(name_tok);
			entry->description = strdup(desc_tok + 2);
			
			vector_add(el->possible_values, entry);
		}
		
		free(line);
		fclose(fp);
	}
	
	fpnode_free(use_expand_dir);
	
	return out;
}


Map* make_conf_new(Emerge *em) {
	char* filename = NULL;
	asprintf(&filename, "%s/etc/portage/make.conf", em->root);
	
	FILE* fp = fopen(filename, "r");
	Map* out = mc_parse(fp);
	
	fclose(fp);
	
	return out;
}

UseFlag* make_conf_use(Emerge* em) {
	UseFlag* out = NULL;
	
	StringVector* keys = map_all_keys(em->use_expand);
	
	/* USE_EXPAND */
	for (int i = 0; i < keys->n; i++) {
		char* key = string_vector_get(keys, i);
		char* value = map_get(em->make_conf, key);
		
		if (!value)
			continue;
		
		key = strlwr(strdup(key));
		value = strdup(value);
		
		for (char* tok = strtok(value, " "); tok; tok = strtok(NULL, " ")) {
			UseFlag* temp = malloc(sizeof(UseFlag));
			temp->next = out;
			out = temp;
			
			if (tok[0] == '-') {
				out->status = USE_DISABLE;
				asprintf(&out->name, "%s_%s", key, tok + 1);
			}
			else {
				out->status = USE_ENABLE;
				asprintf(&out->name, "%s_%s", key, tok);
			}
		}
	}
	
	char* use_str = map_get(em->make_conf, "USE");
	if (use_str) {
		for (char* tok = strtok(use_str, " "); tok; tok = strtok(NULL, " ")) {
			UseFlag* temp = malloc(sizeof(UseFlag));
			temp->next = out;
			out = temp;
			
			if (tok[0] == '-') {
				out->status = USE_DISABLE;
				out->name = strdup(tok + 1);
			}
			else {
				out->status = USE_ENABLE;
				out->name = strdup(tok);
			}
		}
	}
	
	return out;
}