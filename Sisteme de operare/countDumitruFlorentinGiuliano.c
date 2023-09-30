#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <pthread.h>
#define MAX_RESOURCES 5
int available_resources = MAX_RESOURCES;
pthread_mutex_t mtx;

/// Dumitru Florentin Giuliano 
/// Grupa 233
/// laborator 7 ex 1

int decrease_count(int count) {
  pthread_mutex_lock( & mtx); 
  if (available_resources < count) { 
    pthread_mutex_unlock( & mtx);
    return -1;
  } else {
    available_resources -= count; 
    printf("Got %d resources %d remaining\n", count, available_resources);
  }
  pthread_mutex_unlock( & mtx); 
  return 0;

}

int increase_count(int count) {

  pthread_mutex_lock( & mtx); 
  available_resources += count; 
  printf("Released %d resources %d remaining\n", count, available_resources);
  pthread_mutex_unlock( & mtx); 

  return 0;
}

void * solve(void * arg) {

  int count = * (int * ) arg;

  while (decrease_count(count) == -1);
  increase_count(count);

  return NULL;
}

int main(int argc, char * argv[]) {

  if (pthread_mutex_init( & mtx, NULL)) {
    perror(NULL);
    return errno;
  }
  int count;
  pthread_t thr[MAX_RESOURCES + 2]; //vectori pentru a retine id-urile threadurilor
  printf("MAX_RESOURCES = %d\n", available_resources);
  for (int i = 0; i < MAX_RESOURCES; i++) { //creez MAX_RESOURCES threaduri, fiecare urmand sa aiba nevoie de un numar random de resurse
    count = rand() % (MAX_RESOURCES + 1);
    if (pthread_create( & thr[i], NULL, solve, & count)) { //creearea threadului, executand functia solve cu argumentul count (nr random de resurse)
      perror(NULL);
      return errno;
    }
  }

  for (int i = 0; i < MAX_RESOURCES; i++)
    pthread_join(thr[i], NULL); //uneste inapoi thread-urile la main-thread
  pthread_mutex_destroy( & mtx); //distruge mutex-ul

  return 0;
}


