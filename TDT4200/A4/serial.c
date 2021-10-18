
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <omp.h>

struct thread_args {
    char **argv;
    int i;
    int thread_num;
};

void pthread_func(struct thread_args *args)
{
    char **argv = args->argv;
    int i = args->i;
    int thread_num = args->thread_num;
    printf("Thread %d: %s\n", thread_num, argv[i]);
}

int main(int argc, char **argv)
{
    int num_threads = argc;
    pthread_t *threads = malloc(sizeof(pthread_t) * num_threads);
    struct thread_args *args = malloc(sizeof(struct thread_args) * num_threads);
    for (int i = 0; i < num_threads; i++){
        args[i] = (struct thread_args) {.argv = argv, .i = i, .thread_num = i};
        pthread_create(&(threads[i]), NULL, &pthread_func, args+i);
    }

    for (int i = 0; i < num_threads; i++){
        pthread_join(threads[i], NULL);
    }

/*
    for (int i = 0; i < argc; i++) {
        printf("%s\n", argv[i]);
    }
*/
}
