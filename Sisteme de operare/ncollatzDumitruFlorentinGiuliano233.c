#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

/// Dumitru Florentin Giuliano, laboratorul 4 exercitiul 3

int main(int argc, char* argv[]) {

	int i; 
	printf("Starting Parent %d\n", getpid());
	for(i = 1; i <= argc; i++) {
		pid_t pid = fork();
		if(pid < 0)
			return errno;
		else 
		if (pid == 0) {
			int value = atoi(argv[i]);
			printf("%d: ", value );
			while(value != 1) {
				printf("%d ", value );
				if(value  % 2 == 0)
					value  = value  / 2;
				else
					numarul = 3*value  + 1;
			}
			printf("\nDone Parent %d Me %d\n",  getppid(), getpid());
			exit(1);
		}
	}

	for(i = 1; i <= argc; i++)
		wait(NULL);
	printf("Done Parent %d Me %d\n", getppid(), getpid());

	return 0;
}
