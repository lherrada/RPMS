#include <sys/stat.h>

#define SAME_INODE(a,b) ((a).st_ino == (b).st_ino\
                        && (a).st_dev == (b).st_dev)

struct dev_ino 
{
 ino_t st_ino;
 dev_t st_dev;
};

struct dev_ino *get_root_dev_ino(struct dev_ino *);
void shift_buffer(char *,char *);
char *getcwd(char *);
ino_t getinode_number(struct stat *p);

