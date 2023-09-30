#include <stdlib.h>
#include <stdio.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <errno.h>


void show(int i);
FILE *f;
char *criptat[1000];
int size[1000], ind = 0;
int *pozitii[1000];
pthread_t p;

int makeInt(char *p){
int d =0;
for (int i = 0; i < strlen(p); i ++)
d = d* 10 + (p[i] - '0');
return d;
}


void* makeDecriptare(void *p){
	int *ind = (int*) malloc(sizeof(int));
	ind = (int*) p;
	int i = *ind;
	char p1[size[i]];
	p1[size[i]] = '\0';
	for (int j = 0; j < size[i]; j ++){
		p1[pozitii[i][j]] = criptat[i][j];
	}
	fprintf(f,"%s\n", p1);
	return NULL;
}

void show(int i){
	printf("%s -> %d \n",criptat[i],size[i]);
	for (int j = 0; j < size[i]; j  ++)
		printf("%d ", pozitii[i][j]);
	printf("\n");  
}

int main(int argc, char * argv[]){

f  = fopen("decriptare.txt","w+");

int i = 0;

while (i < argc){
	criptat[ind] = (char*) malloc(strlen(argv[i]));
	strcpy(criptat[ind],argv[i]);
	size[ind] = makeInt(argv[i+1]);
	pozitii[ind] = (int*)malloc(size[ind]*sizeof(int));
	for (int i1 = 1; i1 <= size[ind]; i1 ++){
		pozitii[ind][i1-1] = makeInt(argv[i+1+i1]);
	}
	i += (size[ind] + 2);
	ind ++;
}

for (i = 0; i < ind; i ++){
	if (pthread_create(&p,NULL,makeDecriptare, &i)) {
		printf("1 -> %d\n",i);
		perror(NULL);
		return -1;
	}
	if (pthread_join(p,NULL)){
		printf("2 -> %d\n",i);
		perror(NULL);
		return -1;
	}
}

fclose(f);
return 0;
}
