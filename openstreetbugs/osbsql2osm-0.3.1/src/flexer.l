%{
#include <stdio.h>
#include "parser.h"
//#define YY_USER_ACTION puts(yytext);
%}
%x SQSTRCOND DQSTRCOND
%%
"INSERT INTO `bugs` (`id`, `lon`, `lat`, `text`, `type`, `last_changed`, `date_created`, `nearby_place`) VALUES"  return (INSERTHEAD);

<SQSTRCOND>([^']|"\\'")*  yylval=strdup(yytext);  return(SQSTRING);
<DQSTRCOND>([^"]|"\\\"")* yylval=strdup(yytext);   return(DQSTRING);
<SQSTRCOND>"'"	    BEGIN(0);
<DQSTRCOND>"\""	    BEGIN(0);
"'"		    BEGIN(SQSTRCOND);
"\""	    BEGIN(DQSTRCOND);
"("		    return(LRB);
")"		    return(RRB);
","		    return(KMM);
";"		    return(SEMIC);
"-"?[0-9]+("."[0-9]+("e""-"?[0-9][0-9])?)?    yylval=strdup(yytext); return(ZAHL);
"\n"	return (NL);
[:space:]  ;return(WS);
.		    ;


%%

#if 0
int 
main(argc , argv)
int argc;
char **argv;
{
	yyin = stdin;

	yylex();
}

#endif




