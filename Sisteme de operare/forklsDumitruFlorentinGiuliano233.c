#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/// Dumitru Florentin Giuliano laboratorul 4, exercitiul 1

int main(int argc, void *arg[])
{
pid_t pid =fork();
if(pid<0)
	return errno;
else
	if(pid==0)
	{/// Corpul de instructiuni al copilului 
		printf("My PID=%d, Child PID=%d\n", getppid(), getpid());
		char *argv[]={"ls", NULL};
		execve("/bin/ls", argv, NULL);
		perror(NULL);
	}
	else
	{	
		int stats

		pid_t pidc = wait(&stats);
                if(!stats)
                	printf("Child %d finished\n", pidc);
                else
                	printf("EROARE");
	}
		
	}
return 0;
}
