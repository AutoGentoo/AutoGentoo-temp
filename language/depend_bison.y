%define api.prefix {depend}

%code requires {
  #include "depend.h"
  #include <stdlib.h>
}

%{
#include <stdio.h>
#include <depend.h>

int dependparse(void);
int dependwrap() { return 1; }
int dependlex();
extern int dependlineno;
extern char* dependtext;
extern DependExpression* dependout;

void dependerror(const char *message);
%}

%start program

%union {
    Atom* atom;
    DependExpression* dependexpression;
    Use* use;
}

%token <use> NO_USE
%token <use> YES_USE
%token <use> EXACT_ONE
%token <use> LEAST_ONE
%token <use> MOST_ONE

%token <atom> ATOM

%token END_OF_FILE

%type <dependexpression> expr
%type <atom> select
%type <use> use

%%

program:    | expr  {
                        dependout = $1;
                    }
            | END_OF_FILE
            ;

expr :  use[out] '(' expr[in] ')'       {
                                            $$ = new_dependexpression(
                                                new_check_use($out, $in), 
                                                USE_EXPR
                                            );
                                        }
        | expr expr                     {
                                            DependExpression* ar[] = {
                                                $1,
                                                $2
                                            };
                                            $$ = new_dependexpression (ar, EXPR_EXPR);
                                        }
        | ATOM                          {
                                            $$ = new_dependexpression($1, SEL_EXPR);
                                        }
     ;

use : NO_USE
    | YES_USE
    | EXACT_ONE
    | LEAST_ONE
    | MOST_ONE
    ;