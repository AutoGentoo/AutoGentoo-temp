/*
 * request.h
 * 
 * Copyright 2017 Unknown <atuser@Hyperion>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */


#ifndef __AUTOGENTOO_CLIENT_EMERGE__
#define __AUTOGENTOO_CLIENT_EMERGE__

#include <stdio.h>
#include <response.h>
#include <s_emerge.h>
#include <serve_client.h>
#include <autogentoo.h>

typedef enum {
    install_s,  // Install only on the server (used for build tools)
    _remove,   // Remove package from server removes from client if possible
    install,  // Install on the client and server
    remove_c,   // Remove from the client
} request_t;

extern char *request_names[];

struct client_request {
    char * atom;
    request_t type;
};

struct method_s {
    request_t type;
    response_t (*method)(char*, struct manager *, struct serve_client);
};

#define INSTALL_S (struct method_s) {install_s,m_install_s}
#define REMOVE (struct method_s) {_remove,m_remove_s}
#define INSTALL (struct method_s) {install,m_install_c}
#define REMOVE_C (struct method_s) {remove_c,m_remove_c}

extern struct method_s methods [];

response_t m_install_s (char*, struct manager *, struct serve_client);
response_t m_remove_s (char*, struct manager *, struct serve_client);
response_t m_install_c (char*, struct manager *, struct serve_client);
response_t m_remove_c (char*, struct manager *, struct serve_client);

response_t exec_method (request_t type, struct manager * man, char* command, int sockfd);

response_t ask_server (char* ip, struct client_request req);
#endif
