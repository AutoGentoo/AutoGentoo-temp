//
// Created by atuser on 4/23/19.
//

#ifndef AUTOGENTOO_PORTAGE_H
#define AUTOGENTOO_PORTAGE_H

typedef struct __Repository Repository;

#include <autogentoo/hacksaw/map.h>
#include <openssl/evp.h>
#include "constants.h"
#include "manifest.h"
#include "keywords.h"

struct __Repository {
	char* name;
	char* location; //!< Root of repository (/usr/portage)
	
	
	char** masters;
	int priority; // -1000
	int strict_misc_digests; // true
	int sync_allow_hardlinks; // true
	char* sync_openpgp_key_path; // /usr/share/openpgp-keys/gentoo-release.asc
	int sync_openpgp_key_refresh_retry_count; // 40
	int sync_openpgp_key_refresh_retry_delay_exp_base; // 2
	int sync_openpgp_key_refresh_retry_delay_max; // 60
	int sync_openpgp_key_refresh_retry_delay_mult; // 4
	int sync_openpgp_key_refresh_retry_overall_timeout; // 1200
	int sync_rcu; // false
	char* sync_type; // rsync
	char* sync_uri; // rsync://rsync.gentoo.org/gentoo-portage
	int sync_rsync_verify_max_age; // 24
	int sync_rsync_verify_jobs; // 1
	char** sync_rsync_extra_opts;
	int sync_rsync_verify_metamanifest; // yes
	
	int auto_sync; // true
	
	Manifest* category_manifests;
	Map* packages;
	
	Repository* next;
};

Repository* emerge_repos_conf(Emerge* emerge);

Repository* repository_new();

int portage_get_hash(sha_hash* target, char* path, const EVP_MD* algorithm);
int portage_get_hash_fd(sha_hash* target, int fd, const EVP_MD* algorithm);


#endif //AUTOGENTOO_PORTAGE_H
