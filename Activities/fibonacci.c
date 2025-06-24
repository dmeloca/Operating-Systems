#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define MAX_RECURSION 3

typedef struct {
    int n;
    int depth;
    int result;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int done;
} FibArgs;

void* threaded_fib(void* args) {
    FibArgs* data = (FibArgs*)args;
    int n = data->n;
    int depth = data->depth;

    if (n == 0) {
        data->result = 0;
    } else if (n == 1) {
        data->result = 1;
    } else if (depth < MAX_RECURSION) {
        pthread_t t1, t2;
        FibArgs arg1 = {n - 1, depth + 1, 0, PTHREAD_MUTEX_INITIALIZER, PTHREAD_COND_INITIALIZER, 0};
        FibArgs arg2 = {n - 2, depth + 1, 0, PTHREAD_MUTEX_INITIALIZER, PTHREAD_COND_INITIALIZER, 0};

        pthread_create(&t1, NULL, threaded_fib, &arg1);
        pthread_create(&t2, NULL, threaded_fib, &arg2);

        // Wait for first thread
        pthread_mutex_lock(&arg1.mutex);
        while (!arg1.done) {
            pthread_cond_wait(&arg1.cond, &arg1.mutex);
        }
        pthread_mutex_unlock(&arg1.mutex);

        // Wait for second thread
        pthread_mutex_lock(&arg2.mutex);
        while (!arg2.done) {
            pthread_cond_wait(&arg2.cond, &arg2.mutex);
        }
        pthread_mutex_unlock(&arg2.mutex);

        data->result = arg1.result + arg2.result;

        pthread_join(t1, NULL);
        pthread_join(t2, NULL);
    } else {
        FibArgs arg1 = {n - 1, depth + 1, 0, PTHREAD_MUTEX_INITIALIZER, PTHREAD_COND_INITIALIZER, 0};
        FibArgs arg2 = {n - 2, depth + 1, 0, PTHREAD_MUTEX_INITIALIZER, PTHREAD_COND_INITIALIZER, 0};

        threaded_fib(&arg1);
        threaded_fib(&arg2);

        data->result = arg1.result + arg2.result;
    }

    // Notify the parent thread that result is ready
    pthread_mutex_lock(&data->mutex);
    data->done = 1;
    pthread_cond_signal(&data->cond);
    pthread_mutex_unlock(&data->mutex);

    return NULL;
}

int main() {
    int n;
    scanf("%d", &n);

    FibArgs args = {n, 0, 0, PTHREAD_MUTEX_INITIALIZER, PTHREAD_COND_INITIALIZER, 0};
    pthread_t thread;

    pthread_create(&thread, NULL, threaded_fib, &args);

    // Wait for the top-level Fibonacci result
    pthread_mutex_lock(&args.mutex);
    while (!args.done) {
        pthread_cond_wait(&args.cond, &args.mutex);
    }
    pthread_mutex_unlock(&args.mutex);

    pthread_join(thread, NULL);

    printf("Fibonacci(%d) = %d\n", n, args.result);
    return 0;
}
