
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>


struct thread_args{
    int i;
    char **argv;
    int thread_num;
    int num_threads;
};

void *thread_function(struct thread_args *args)
{
    int i = args->i;
    char **argv = args->argv;
    int thread_num = args->thread_num;
    int num_threads = args->num_threads;
    //printf("Hello from thread number %d of %d!\n", thread_num, num_threads);
    printf("Thread %d/%d: %s\n", thread_num, num_threads, argv[i]);
}

int main(int argc, char **argv)
{
    int num_threads = argc;

    pthread_t *threads = malloc(sizeof(pthread_t) * num_threads);
    struct thread_args *args_arr = malloc(sizeof(struct thread_args) * num_threads);
    for (int i = 0; i < num_threads; i++)
    {
        args_arr[i] = (struct thread_args) {.i = i, .argv = argv, .thread_num = i, .num_threads = num_threads};
        pthread_create(threads+i, NULL, &thread_function, args_arr+i);
    }

    for (int i = 0; i < num_threads; i++)
    {
        pthread_join(threads[i], NULL);
    }

/*
    for (int i = 0; i < argc; i++)
    {
        printf("%s\n", argv[i]);
    }
*/
}
