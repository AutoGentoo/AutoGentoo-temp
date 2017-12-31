#ifndef __AUTOGENTOO_HANDLE_H__
#define __AUTOGENTOO_HANDLE_H__

#include "server.h"
#include "response.h"

typedef response_t (*SHFP)(Connection*, char**, int);
typedef struct __RequestLink RequestLink;

struct __RequestLink {
    char* request_ident;
    SHFP call;
};

extern RequestLink requests[];

/**
 * Parse the request and write the arguemnts to args
 * @param parse_line the input request to read from
 * @param args the arguments parsed from the request
 * @return a pointer to function that should be called
 */
SHFP parse_request (char* parse_line, char** args);

/**
 * HTTP request to download file
 * @param conn the connection that holds the request
 * @param args [path] [HTTP/1.0 or 1.1]
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t GET (Connection* conn, char** args, int start);

/**
 * Install a packages to the bounded host
 * @param conn the connection that holds the request
 * @param args [emerge argument[s]]
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t INSTALL (Connection* conn, char** args, int start);

/* SRV Configure requests */

/**
 * Create a new client \
 * ARGUMENTS ARE SEPARATED BY NEW LINES!
 * @param conn the connection that holds the request
 * @param args [argc of ETC] [HOSTNAME] [PROFILE] [CHOST] [CFLAGS] [USE] [ETC]
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_CREATE (Connection* conn, char** args, int start);

//response_t SRV_DEVCREATE (Connection* conn, char** args, int start);

/**
 * Edit an existing Host
 * @param conn the connection that holds the request
 * @param args [argc of ETC] [ID] [HOSTNAME] [PROFILE] [CHOST] [CFLAGS] [USE] [ETC]
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_EDIT (Connection* conn, char** args, int start);

/**
 * Bind the connections ip address to the specified Host*
 * @param conn the connection that holds the request
 * @param args [HOST_ID]
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_ACTIVATE (Connection* conn, char** args, int start);

/**
 * Delete a host (currently all users can do this) \
 * This will be changed
 * @param conn the connection that holds the request
 * @param args [HOST_ID]
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_HOSTREMOVE (Connection* conn, char** args, int start);

/* SRV Utility request */

/**
 * Initialize a host \
 * This has a scheduled deprecation due to HostTemplate implementations
 * @param conn the connection that holds the request
 * @param args (none)
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_INIT (Connection* conn, char** args, int start);

/**
 * Initilize the STAGE1 of the bounded host \
 * This has a scheduled deprecation due to HostTemplate implementations
 * @param conn the connection that holds the request
 * @param args (none)
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_STAGE1 (Connection* conn, char** args, int start);

/**
 * Mount all the directories required to chroot() to Host
 * @param conn the connection that holds the request
 * @param args (none)
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_MNTCHROOT (Connection* conn, char** args, int start);

/* SRV Metadata requests */

/**
 * Returns metadata of the Host selected
 * @param conn the connection that holds the request
 * @param args [HOST_ID]
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_GETHOST (Connection* conn, char** args, int start);

/**
 * Returns an int (host count) followed by a list of the created hosts \
 * All of these are newline separated
 * @param conn the connection that holds the request
 * @param args (none)
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_GETHOSTS (Connection* conn, char** args, int start);

/**
 * Returns the ID of the bounded host of the IP from the current request
 * @param conn the connection that holds the request
 * @param args (none)
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_GETACTIVE (Connection* conn, char** args, int start);

/**
 * Returns information outputed from 'lscpu' of the build server
 * @param conn the connection that holds the request
 * @param args (none)
 * @param start Start index to read from request
 * @return HTTP standard codes
 */
response_t SRV_GETSPEC (Connection* conn, char** args, int start);

/* SRV Kernel request (unimplmented) */

#endif
