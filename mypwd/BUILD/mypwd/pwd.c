//Program written by Luis Herrada
// This is a light-weight version of command line pwd (present working directory)


#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "getcwd.h"


int main(void) {
char *filename=(char *)malloc(PATH_MAX);
getcwd(filename);
puts(filename);
return 0;
}
