#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

int main()
{

if(write(2,"HelloWorld!\n",12)!=12)
{
perror("Eroare");
return errno;
}
return 0;
}
