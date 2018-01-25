#ifndef __AUTOGENTOO_H__
#define __AUTOGENTOO_H__

#include "hacksaw/hacksaw.h"
#include "chroot.h"
#include "command.h"
#include "download.h"
#include "endian_convert.h"
#include "getopt.h"
#include "handle.h"
#include "host.h"
#include "kernel.h"
#include "endian_convert.h"
#include "getopt.h"
#include "handle.h"
#include "host.h"
#include "response.h"
#include "server.h"
#include "thread.h"
#include "stage.h"
#include "writeconfig.h"


/* Port to 9491 so we don't overlap with our main service */
//#define AUTOGENTOO_DEBUG

//#define AUTOGENTOO_NO_THREADS

#ifdef AUTOGENTOO_DEBUG
#define AUTOGENTOO_PORT 9491
#else
#define AUTOGENTOO_PORT "9490"
#endif

void set_location (Opt* op, char* loc);
void print_help_wrapper (Opt* op, char* arg);
void set_port (Opt* op, char* c);
void set_debug (Opt* op, char* c);
void set_daemon (Opt* op, char* c);
void pipe_to_log (Opt* op, char* logfile);
int main (int argc, char** argv);

#endif