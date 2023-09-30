#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE *f1, * f2;

int exists(int a, int vec[], int size){
for (int i = 0; i < size; i ++)
if ( a == vec[i]) return 1;
return 0;
}

int  makePerm(char *a){

int size = strlen(a);
int vec [size];
int par = 0;
for (int i = 0; i < size; i ++){
int j = rand()%size;
while (exists(j,vec, par)){
j = rand()%size;
}
vec[par] = j;
par ++;
}
fprintf(f1, "%d\n", size);
for (int i = 0; i < size; i ++)
fprintf(f1,"%d ", vec[i]);
fprintf(f1,"\n");
char g[strlen(a)];
for (int i = 0; i < size; i ++)
g[i] = a[vec[i]];
fprintf(f2, "%s\n", g);
return 1;
}

int main(int argc, char *argv[]){

f1 = fopen("criptare.txt", "w+");
f2 = fopen("criptare1.txt", "w+");

for (int i = 0; i < argc; i ++){
pid_t pid = fork();
if (pid < 0) return -1;
if ( pid == 0){

if (makePerm(argv[i]))return -1;
exit(1);

} else {
wait(NULL);
}
}

fclose(f1);
fclose(f2);

return 0;
}
