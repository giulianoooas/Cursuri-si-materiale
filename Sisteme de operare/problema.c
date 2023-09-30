#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/types.h>

int main(int narg, char *argv[])
{
for(int i=1;i<narg;i++)
{
int n=atoi(argv[i]);
pid_t pid=fork();

if(pid<0)
return errno;

if(pid==0)
{
printf("%d ",n);

        while(n!=1)
{
                if(n%2==0)
                        n=n/2;
                else
                        n=3*n+1;
                printf("%d ",n);
                }
printf("\n");
return 0;
}
}

for(int i=1;i<narg;i++)
{
int pidd=wait(NULL);
printf("Child %d ", pidd);
}
return 0;
}


