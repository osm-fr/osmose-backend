AC_INIT([osbsql2osm],[0.3.1],[john@tuxcode.org])
AM_INIT_AUTOMAKE()


AC_PROG_LEX
if test "x$LEX" != xflex; then
    LEX="$SHELL $missing_dir/missing flex"
    AC_SUBST([LEX_OUTPUT_ROOT], [lex.yy])
    AC_SUBST([LEXLIB], [''])
fi

AC_PROG_YACC


AC_PROG_CC
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([Makefile src/Makefile])




AC_OUTPUT
