#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>


void show();
int makeInt(char * a){
int p = 0;
for (int i = 0; i < strlen(a); i ++){
	p =p *10 + (a[i]-'0');
}
return p;
}

int verificare1 (int p, char *a[]){
	int d[p];
	for (int i = 0; i < p; i ++) d[i] = 0;
	for (int i = 0; i < p; i ++){
		int d1 = makeInt(a[i]);
		if (d1 < 0 || d1 >= p) return -1;
		d[i] = 1;
	}
	for (int i = 0; i < p; i ++) if (d[i] == 0) return -1;
	return 0;
}

int verificare(int val){
if (val == 2 || val == 3)
return 1;
return 0;
}

char *res[10000];
int nr = 0;

void add(char *a){
res[nr] = (char*) malloc(strlen(a));
strcpy(res[nr], a);
nr ++;
}

int readL(char path[]){

struct stat s;
if (stat(path, &s)) return -1;
int fd;
fd = open(path, O_RDONLY);
if (fd < 0) return -1;
char h[s.st_size];
int marime = read(fd, h, s.st_size);
if (marime < 0) return -1;
h[s.st_size] = '\0';

const char sep [] = " \n-.,:;!?";

char * p = strtok(h,sep);

while (p != NULL){
add(p);
p = strtok(NULL, sep);
}
close(fd);
return 0;
}

int readR(char path1[],char path2[]){

struct stat s1,s2;
if (stat(path1, &s1)) return -1;
int fd1;
fd1 = open(path1, O_RDONLY);
if (stat(path2, &s2)) return -1;
int fd2;
fd2 = open(path2, O_RDONLY);
if (fd1 < 0 || fd2 < 0) return -1;
const char sep1[] = " \n-.,:;!?";
const char sep2[] = " \n";

int m1, m2;
char h1[s1.st_size], h2[s2.st_size];
m1 = read(fd1,h1,s1.st_size);
m2 = read(fd2, h2,s2.st_size);
if (m1 < 0 || m2 < 0) return -1;

char *p;

p = strtok(h1, sep1);

char * a[1000];
int poz = -1;
while (p!= NULL){
	poz ++;
	a[poz] = (char*) malloc (strlen(p));
	strcpy(a[poz], p);
	p =strtok(NULL,sep1);
	}

p = strtok(h2,sep2);
int i = 0;
while (p != NULL && i <= poz){
	add(a[i]);
	int d = makeInt(p);
	if (d != strlen(a[i]) )return -1;
	add(p);
	char *vec [d];
	p = strtok(NULL,sep2);
	int j = 0;
	while (p!= NULL && j < d){
		vec[j] = (char*) malloc (strlen(p));
		strcpy(vec[j],p);
		add(vec[j]);
		j ++;
		p = strtok(NULL,sep2);
	}
	if (verificare1(d,vec)){ 
		break;
	}
	i ++;
}
close(fd1);
close(fd2);
if (i != poz) return -1;
return 0;
}


void show(){
	for (int i = 0; i < nr; i ++)
		printf("%s\n",res[i]);
}

int main (int argc, char* argv[]){

if (!verificare(argc)) return -1;

if (argc == 2){
if (readL(argv[1])){ 
	printf("Ceva n-a mers bine!\n");	
	return -1;
	}
printf("Voi face criptare.\n");
execve("criptare", res, NULL);
} else {
if (readR(argv[1],argv[2])){ 
	printf("Ceva n-a mers bine!\n");
	return -1;
	}
printf("Voi face decriptare.\n");
execve("decriptare",res, NULL);
}

return 0;
}
