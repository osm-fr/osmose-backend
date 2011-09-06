%{
#include <stdio.h>
#include <string.h>
#include <errno.h>
#define YYSTYPE char *

#ifndef CMTTRENNZ
#define CMTTRENNZ " ## "
#endif



char * glob_bu;
size_t glob_busize;
char *a, *b;
extern int errno;
void usage();


void yyerror(const char *str);
int yywrap();
char *strup(char *in);

%}



%start zeilen
%token SQSTRING DQSTRING LRB RRB KMM SEMIC ZAHL WS INSERTHEAD NL

%%

zeilen	: /*empty*/
        |zeilen mysqlline NL
	;



mysqlline :
	  INSERTHEAD values  SEMIC 
	  ;

values: values KMM value 
      | value
      ;
       /* 1 2  3  4  5 6   7 8    9 10   11 12          13 14         15 16          17 */
value: /* ( id , lon , lat , text , type , last_changed , date_created, nearby_place )*/
     LRB  ZAHL KMM ZAHL KMM ZAHL KMM SQSTRING KMM ZAHL KMM SQSTRING KMM SQSTRING KMM SQSTRING RRB
     {
	a=strup($8);
	b=strup($16);
	printf("  <node id='%s' timestamp='%s' visible='true' version='1' lat='%s' lon='%s'>\n"
		"\t  <tag k='text' v='%s' />\n"
		"\t  <tag k='type' v='%s' />\n"
		"\t  <tag k='last_changed' v='%s' />\n"
		"\t  <tag k='date_created' v='%s' />\n"
		"\t  <tag k='nearby_place' v='%s' />\n"
		"  </node>\n\n",$2,$12,$6,$4,a,$10,$12,$14,b); 
	free(a);
	free(b);

    /*like this:
   <node id='${id}' timestamp='${last_changed}' visible='true' lat='${lat}' lon='${lon}'>
    <tag k='text' v='${text}' />
    <tag k='type' v='${type}' />
    <tag k='last_changed' v='${last_changed}' />
    <tag k='date_created' v='${date_created}' />
    <tag k='nearby_place' v='${nearby_place}' />
  </node> */
      }
     ;


%%


#include "flexer.c"


void yyerror(const char *str)
{
        fprintf(stderr,"error: %s %s\n",str,yytext);
}

int yywrap()
{
    return 1;
}

int main(int argc,char **argv)
{
    if (argc > 1) {
	usage();
	return 1;
	}
    glob_busize = 10240;
    glob_bu = malloc(10240);

    puts(""
"<?xml version='1.0' encoding='UTF-8'?>\n"
"<osm version='0.6' generator='osbsql2osm'>\n");
    yyparse();
    puts(""
"</osm>\n");
    return 0;
}

void usage()
{
    puts(
    "osmsql2osm takes an openstreetbugs database dump on stdin and prints a osm xml-ish file on stdout\n"
    "Thou shalt not give any arguments yet!\n"
	);
}


char * strup(char * in){
    size_t fup;
    unsigned int i;
    char * targ = glob_bu;
    char c;

    fup = strlen(in);
    if(glob_busize < (5*fup))
	{
		free(glob_bu);
		glob_bu =  malloc(5*fup);
		targ=glob_bu;
	}
    for (i=0;i<fup;i++)
    {
	switch(c=*(in+i))
	    {
	    case '<': /* Its definitely an <hr /> tag... */
		strcpy(targ,CMTTRENNZ);
		targ += sizeof(CMTTRENNZ);
		i +=5;
		break;
	    case '\\':
		if(*(in+i+1)=='\'')
		{
			strcpy(targ,"&apos;");
			targ +=6;
			i++;
			break;
		}
	    case '&':
/*quot 	" 	U+0022 (34) 	XML 1.0 	(double) quotation mark
amp 	& 	U+0026 (38) 	XML 1.0 	ampersand
apos 	' 	U+0027 (39) 	XML 1.0 	apostrophe (= apostrophe-quote)
lt 	< 	U+003C (60) 	XML 1.0 	less-than sign
gt 	> 	U+003E (62) 	XML 1.0 	greater-than sign
*/
		if((strncmp("amp;",(in+i+1),4) &&
		 strncmp("apos;",(in+i+1),5)   &&
		 strncmp("lt;",(in+i+1),3)     &&
		 strncmp("gt;",(in+i+1),3)     &&
		 strncmp("quot;",(in+i+1),5) ) )
			{
			strcpy(targ,"&amp;");
			targ += 5;
			break;}
	    default :
		*targ = c;
		targ++;
	    }
    }
    *targ ='\0';
    return strdup(glob_bu);
}
	



