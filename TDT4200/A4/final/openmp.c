
#include <stdio.h>
#include <omp.h>


int main(int argc, char **argv)
{
    #pragma omp parallel for
    for (int i = 0; i < argc; i++) {
        printf("Thread %d/%d: %s\n", omp_get_thread_num(), omp_get_num_threads(), argv[i]);
    }
}
