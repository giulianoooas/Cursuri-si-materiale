#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <string.h>

/// Dumitru Florentin Giuliano, laboratorul 4 exercitiul 3

int makeInt(char *a){
int result = 0, n = strlen(a);
for (int i = 0; i < n; i ++)
	result = result * 10 + (a[i] -'0');
return result;
}

int main(int arg, char  *argv[])
{
pid_t pid=fork();

if(pid<0)
	return errno;
else
	if(pid==0)
	{
		/// Comenzile copiului
		int value= makeInt(argv[1]);
		printf("%d: %d ",value,value);
		while(value!=1)
		{
		if(value%2==0)
			value=value/2;
		else
			value=3*value+1;
		printf("%d ",value);
		}
	}
	else
	{
		/// Comenzile tatalui
		pid_t pid=wait(NULL);
		printf("\nChild %d finished\n", pid);
	}
return 0;
}
