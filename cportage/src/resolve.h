//
// Created by atuser on 12/6/19.
//

#ifndef CPORTAGE_RESOLVE_H
#define CPORTAGE_RESOLVE_H

#include <autogentoo/hacksaw/vector.h>
#include "atom.h"

typedef struct __ResolvedEbuild ResolvedEbuild;


typedef enum {
	PORTAGE_NEW = 1 << 0, //!< New package
	PORTAGE_SLOT = 1 << 1, //!< Install side by side
	PORTAGE_REMOVE = 1 << 2, //!< Remove package 'old'
	PORTAGE_UPDATE = 1 << 3, //!< Install a new package and remove the old one
	PORTAGE_DOWNGRADE = 1 << 4,
	PORTAGE_REPLACE = 1 << 5,
	PORTAGE_USE_FLAG = 1 << 6,
	PORTAGE_BLOCK = 1 << 7
} dependency_t;

struct __ResolvedEbuild {
	Emerge* environ;
	ResolvedEbuild* parent;
	
	/* Creates the backtracking iteration */
	ResolvedEbuild* next;
	
	Dependency* selected_by;
	InstalledEbuild* installed;
	Ebuild* ebuild;
	
	UseFlag* useflags;
	UseFlag* explicit_flags;
	
	dependency_t action;
	
	/* Index where this resolve appears  */
	int resolve_index;
	
	int unstable_keywords;
	
	Vector* pre_dependency;
	Vector* post_depenendcy;
};

int ebuild_match_atom(Ebuild* ebuild, P_Atom* atom);
ResolvedEbuild* resolved_ebuild_new(Ebuild* ebuild, P_Atom* atom);
ResolvedEbuild* resolved_ebuild_resolve(Emerge* em, P_Atom* atom);
Package* package_resolve_atom(Emerge* em, P_Atom* atom);
void resolved_ebuild_free(ResolvedEbuild* ptr);

#endif //CPORTAGE_RESOLVE_H
