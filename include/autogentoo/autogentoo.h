#ifndef __AUTOGENTOO_H__
#define __AUTOGENTOO_H__

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include "hacksaw/hacksaw.h"
#include "chroot.h"
#include "endian_convert.h"
#include "hacksaw/getopt.h"
#include "handle.h"
#include "host.h"
#include "kernel.h"
#include "endian_convert.h"
#include "handle.h"
#include "host.h"
#include "response.h"
#include "server.h"
#include "thread.h"
#include "writeconfig.h"
#include "crypt.h"

#define AUTOGENTOO_PORT "9490"
#define AUTOGENTOO_PORT_ENCRYPT "9491"

void set_encrypt_opts (Opt* op, char* arg);

void set_is_unencrypted (Opt* op, char* c);

void set_is_server(Opt* op, char* c);

void set_location(Opt* op, char* loc);

void print_help_wrapper(Opt* op, char* arg);

void set_port(Opt* op, char* c);

void set_debug(Opt* op, char* c);

void set_daemon(Opt* op, char* c);

void pipe_to_log(Opt* op, char* logfile);

void set_target(Opt* op, char* target);

void set_cli(Opt* op, char* arg);

//int main(int argc, char** argv);

#endif