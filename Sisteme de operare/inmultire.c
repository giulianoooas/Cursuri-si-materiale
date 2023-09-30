#include  <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

int a[3][3]={{1,2,3}, {1,3,5}, {1,5,7}}, b[3][3]={{1,2,4}, {1,5,2},{2,3,4}}, c[100][100];

void *inmultire (void **arg)
{
int k, *s;
int m,i,j;
m=*((int*)arg[0]);
i=*((int *)arg[1]);
j=*((int *)arg[2]);
s=(int *)malloc(sizeof(int));
(*s)=0;
for(k=0;k<m;k++)
	(*s)+=a[i][k]*b[k][j];
return s;
}

int main()
{
int n=3,m=3,p=3,q=3;
int i,j;
int  *arg=(int *) malloc(3*sizeof(int));
arg[0]=m;

for(i=0;i<n;i++)
	for(j=0;j<q;j++)
	{
		arg[1]=i;
		arg[2]=j;
		
		pthread_t thr;
		
		if(pthread_create(&thr, NULL, (void *)inmultire,(void *) arg))
		{
			perror(NULL);
			return errno;
		}
		void  *s;
		
		if(pthread_join(thr, &s))
		{
			perror(NULL);
			return errno;
		}

		c[i][j]=*((int *)(s));
}

for(i=0;i<n;i++)
{	for(int j=0;j<m;j++)
		printf("%d ", c[i][j]);
	printf("\n");
}

return 0;
}

