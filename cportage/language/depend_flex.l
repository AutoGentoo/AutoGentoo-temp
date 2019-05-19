%{
#define _GNU_SOURCE
#include "depend.tab.h"
#include <stdio.h>
#include <share.h>
#include <string.h>

int error = 0;

int yyerror(char *s) {
    fprintf(stderr, "%s in line %d near '%s'\n", s, yylineno, yytext);
    error = 1;
    exit(1);
    return error;
}

Dependency* depend_parse (char* buffer) {
    YY_BUFFER_STATE bs = yy_scan_string(buffer);
    yy_switch_to_buffer(bs);
    yyparse();
    return (Dependency*)yyout;
}

P_Atom* atom_parse (char* buffer) {
    YY_BUFFER_STATE bs = yy_scan_string(buffer);
    yy_switch_to_buffer(bs);
    yyparse();
    P_Atom* atom_out = ((Dependency*)yyout)->atom;
    free((void*)yyout);
    return atom_out;
}

RequiredUse* required_use_parse (char* buffer) {
    YY_BUFFER_STATE bs = yy_scan_string(buffer);
    yy_switch_to_buffer(bs);
    yyparse();
    return (RequiredUse*)yyout;
}

%}

letter          [a-zA-Z]
digit           [0-9]
version_suf     ("_alpha"|"_beta"|"_pre"|"_rc"|""|"_p")
version         {digit}+("."{digit}+)*{letter}?({version_suf}{digit}*)*("-r"{digit}+)?[\*]?
identifier      ({letter}|{digit}|_|\+|\*|\-)+
atom            {identifier}\/{identifier}(\-{version})?
slotname        ({letter}|{digit}|"_")({letter}|{digit}|"_"|"-"|"."|"+")*
slot            [\:]({slotname}(\/{slotname})?)?[\*|\=]?
repo            [\:][\:]{identifier}

%%
[\n]                    {yylineno++;}
[ \t\r\\]+              ;
{repo}                  {yylval.identifier = strdup(yytext + 2); return REPOSITORY;}
{slot}                  {
                            size_t len = strlen(yytext);
                            yylval.slot.sub_opts = ATOM_SLOT_IGNORE;
                            if (yytext[len - 1] == '*') {
                                yylval.slot.sub_opts = ATOM_SLOT_IGNORE;
                                yytext[len - 1] == 0;
                            }
                            else if (yytext[len - 1] == '=') {
                                yylval.slot.sub_opts = ATOM_SLOT_REBUILD;
                                yytext[len - 1] == 0;
                            }

                            char* name_splt = strchr(yytext + 1, '/');
                            if (name_splt)
                                *name_splt = 0;
                            if (yytext[1] == 0) {
                                yylval.slot.name = NULL;
                                yylval.slot.sub_name = NULL;
                                return SLOT;
                            }
                            yylval.slot.name = strdup(yytext + 1);
                            if (name_splt)
                                yylval.slot.sub_name = strdup(name_splt + 1);
                            else
                                yylval.slot.sub_name = NULL;

                            return SLOT;
                        }
"??"                    {yylval.use_select = USE_MOST_ONE; return USESELECT;}
"||"                    {yylval.use_select = USE_LEAST_ONE; return USESELECT;}
"^^"                    {yylval.use_select = USE_EXACT_ONE; return USESELECT;}
"(+)"                   {yylval.use_default = ATOM_DEFAULT_ON; return USE_DEFAULT;}
"(-)"                   {yylval.use_default = ATOM_DEFAULT_OFF; return USE_DEFAULT;}
"-"                     {return '-';}
"<"                     {return '<';}
">"                     {return '>';}
"="                     {return '=';}
"!"                     {return '!';}
[\[]                    {return '[';}
[\]]                    {return ']';}
[\?]                    {return '?';}
[\(]                    {return '(';}
[\)]                    {return ')';}
[\^]                    {return '^';}
[\|]                    {return '|';}
[\,]                    {return ',';}
[\~]                    {return '~';}
{atom}                  {
                            yylval.atom_type = atom_new(yytext);
                            return ATOM;
                        }

[\*]                    {return '*';}

{identifier}            {
                            yylval.identifier = yytext;
                            return (IDENTIFIER);
                        }


[<<EOF>>|'']            {return END_OF_FILE;}
.                       {printf("Unknown character: %s\n", yytext);}

%%