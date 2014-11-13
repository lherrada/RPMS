//Program written by Luis Herrada
// This is a light-weight version of command line pwd (present working directory)

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
//#include <unistd.h>
#include "getcwd.h"


struct dev_ino *get_root_dev_ino(struct dev_ino *root_d_i)
{
struct stat statbuf;
char path[] = "/";
if (lstat(path,&statbuf)){
return NULL;
}
root_d_i->st_ino=statbuf.st_ino;
root_d_i->st_dev=statbuf.st_dev;
return root_d_i;
}

//Function shift_buffer has the purpose to store the whole path in a single array.
//Logic is that as new directory names are being found from the inodes 
//these names are pushed to the beginning of the array. Already stored names are 
//shifted to the right.
// Ex. directory /home/users/lherrada
// First node found:  |lherrada|
// Second node found: |users|lherrada
// Third node found: |home|users|lherrada
// Last node found (root): |/|home|users|lherrada

void shift_buffer(char *filename,char *buf) {
 strcat(buf,"/");
 memmove(filename+strlen(buf),filename,strlen(filename));
 memcpy(filename,buf,strlen(buf));
}

//All the magic occurs in getcwd.
//The logic is as follows:
//function finds out what is the i-node number of the current working directory (.) through the  call of function
// getinode_number. Then it compares the root inode number and the just found inode number.
//If it is the same , it means current working directory is '/' and function returns the array with the complete path of the 
//current working directory.
//If it not, it opens a directory stream of directory above (..) and scan for the name directory which corresponds to
// the inode number in the previous step.
// Finally it stores the found name in the buffer filename. 
//


char *getcwd(char *filename) {

 struct stat buf_child;
 struct dev_ino *root_dev_ino=(struct dev_ino *)malloc(sizeof(struct dev_ino));;
 get_root_dev_ino(root_dev_ino);
 char buf[256]; 

 while(1) {

 DIR *dirp;
 stat(".",&buf_child);
 ino_t dir_inode=getinode_number(&buf_child);

 if (SAME_INODE(buf_child,*root_dev_ino)) {
    filename[strlen(filename)-1]='\0';
    memset((void *)buf,0,256);
    shift_buffer(filename,buf);
    break;
    }
  dirp = opendir("..");
 struct dirent const *dp;

//Looking for name entry for inode found in current directory "."
  while ( (dp=readdir(dirp)) !=NULL) {
   if (dp->d_ino == dir_inode) {
     memset((void *)buf,0,256);
     strcpy(buf,dp->d_name);
   break;
    }
   }
shift_buffer(filename,buf);

 closedir(dirp);
 chdir("..");
 }
 return(filename);
}

ino_t getinode_number(struct stat *st) {
return st->st_ino;
}
