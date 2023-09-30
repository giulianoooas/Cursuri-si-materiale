#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/shm.h>

/// Dumitru Florentin Giuliano
/// grupa 233
/// laboratorul 5- shm

int makeInt(){
int result = 0, n = strlen(a);
for (int i = 0; i < n; i ++)
result = result * 10 + (a[i] -'0');
return result;
} /// cu functia asta voi transforma argumentele in numere intregi

int main(int argc, char* argv[]) {
	printf("Starting Parent %d\n", getpid());
	char shm_name[] = "myshm";
	int shm_fd;
	shm_fd = shm_open(shm_name , O_CREAT|O_RDWR, S_IRUSR|S_IWUSR);
	if (shm_fd < 0) {
		perror(NULL) ;
		return errno;
	}

	size_t shm_size = getpagesize() * argc;
	size_t page_size = getpagesize();
	if(ftruncate(shm_fd, shm_size) == -1) {
		perror(NULL);
		shm_unlink(shm_name);
		return errno;
	}

	char* shm_ptr;
	for(int i = 1; i < argc; i++) {
		shm_ptr = mmap(0, page_size, PROT_WRITE, MAP_SHARED, shm_fd, (i-1) * page_size);
		pid_t pid = fork();
		if(pid < 0)
			return errno;
		else
		if (pid == 0) {
			int numarul = makeInt(argv[i]);
			shm_ptr += sprintf(shm_ptr, "%d: ", numarul);
			while(numarul != 1) {
				shm_ptr += sprintf(shm_ptr, "%d ", numarul);
				if(numarul % 2 == 0)
					numarul = numarul / 2;
				else
					numarul = 3*numarul + 1;
			}
			printf("Done Parent %d Me %d\n",  getppid(), getpid());
			exit(1);
		}
	       munmap(shm_ptr, page_size);
	}

	for (int i = 1; i < argc; i++) {
		wait(NULL);
	}

	for (int i = 1; i <= argc; i++) {
		shm_ptr = mmap(0, page_size, PROT_READ, MAP_SHARED, shm_fd, (i-1) * page_size);
		printf("%s\n", shm_ptr);
		munmap(shm_ptr, page_size);
	}
	shm_unlink(shm_name);
	printf("Done Parent %d Me %d\n", getppid(), getpid());

	return 0;
}
