//
// Created by atuser on 4/1/18.
//

#ifndef AUTOGENTOO_REQUEST_H
#define AUTOGENTOO_REQUEST_H

#include <stdio.h>

typedef struct __Request Request;

/**
 * Links a string to a request handler
 */
typedef struct __RequestLink RequestLink;
typedef struct __RequestNameLink RequestNameLink;

typedef enum {
	PROT_AUTOGENTOO = 0, // guarentees first byte is 0 (cant be HTTP)
	PROT_HTTP,
} protocol_t;

typedef enum {
	DIR_CONNECTION_END, //!< Kill the connection after this request ends
	DIR_CONNECTION_OPEN, //!< Handle another request after this one
	DIR_CONNECTION_STREAM, //!< PROT_AUTOGENTOO only, stream content through SMW
} directive_t;

typedef enum {
	REQ_GET,
	REQ_HEAD,
	REQ_POST,
	REQ_START,
	
	REQ_HOST_NEW,
	REQ_MAKE_CONF,
	REQ_HOST_DEL,
	REQ_HOST_EMERGE,
	
	REQ_HOST_MNTCHROOT,
	REQ_SRV_INFO,
	REQ_SRV_REFRESH,
	REQ_AUTH_ISSUE_TOK,
	REQ_AUTH_REFRESH_TOK,
	REQ_AUTH_REGISTER,
	REQ_JOB_STREAM,
	REQ_HOST_STAGE3,
	
	REQ_MAX,
	
	/* Modify request with options */
	/** Set the request a stream (send the response code immediatly)
	  * Also flushes data and writes as fast as posible for realtime responses
 	  * Incompatible request type will return 400 Bad Request
 	 **/
	REQ_OPT_STREAM = 1 << 30
	
} request_t;

#include <autogentoo/response.h>
#include <autogentoo/http.h>
#include <autogentoo/request_structure.h>

/**
 * A function pointer for to handle requests
 * @param conn the connection of the request
 * @param args a list of arguments passed to the handler
 * @param the index to start reading the request at
 */
typedef void (* HTTP_FH)(Connection* conn, HttpRequest* req);
typedef void (* AUTOGENTOO_FH) (Response* res, Request* request);

typedef union __FunctionHandler FunctionHandler;

union __FunctionHandler {
	AUTOGENTOO_FH ag_fh;
	HTTP_FH http_fh;
};

struct __Request {
	Server* parent;
	Connection* conn;
	protocol_t protocol;
	request_t request_type;
	FunctionHandler resolved_call;
	directive_t directive;
	
	void* body;
	size_t length;
	
	int struct_c;
	Vector* structures_parent;
	
	RequestStructure** structures;
};

/**
 * Links a string to a request handler
 */
struct __RequestLink {
	request_t request_ident; //!< The string that matches the request
	FunctionHandler call; //!< A pointer to the function handler
};

struct __RequestNameLink {
	request_t ident;
	char* name;
};

Request* request_handle (Connection* conn);
void request_call(Response* res, Request* req);
void request_free (Request* req);

#endif //AUTOGENTOO_REQUEST_H
