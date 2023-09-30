#include  <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

/// Dumitru Florentin Giuliano
/// Grupa 233
/// lab 6 ex 1

void * reverse(void  *v)
{
	char  *s= (char*) v;
	int i;
	char *t=(char *)malloc(strlen(s)+1);
	int k=0;
	for(i=strlen(s)-1;i>=0;i--)
		t[k++]=s[i];
	t[k]='\0';
	return t;
}

int main(int narg, char **argv)
{
	if(narg<2)
	{
		printf("Date gresite\n");
		return 0;
	}	
	
	pthread_t thr;
	if(pthread_create(&thr, NULL, reverse,argv[1]))
	{
		perror(NULL);
		return errno;
	}

	void * result;
	if(pthread_join(thr, &result))
	{
		perror(NULL);
		return errno;
	}
	printf("%s \n",(char *)result);
	return 0;
}
		
