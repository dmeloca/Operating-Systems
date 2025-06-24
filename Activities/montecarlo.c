#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define NUM_THREADS 4
#define TOTAL_POINTS 1000000

int global_inside_count = 0;
pthread_mutex_t count_mutex;

typedef struct {
    int points_per_thread;
    unsigned int seed;
} ThreadData;

void* monte_carlo_pi(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    int local_count = 0;

    for (int i = 0; i < data->points_per_thread; i++) {
        double x = (double)rand_r(&data->seed) / RAND_MAX;
        double y = (double)rand_r(&data->seed) / RAND_MAX;
        if (x * x + y * y <= 1.0) {
            local_count++;
        }
    }

    // Update global count with mutex protection
    pthread_mutex_lock(&count_mutex);
    global_inside_count += local_count;
    pthread_mutex_unlock(&count_mutex);

    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    ThreadData thread_data[NUM_THREADS];

    int points_per_thread = TOTAL_POINTS / NUM_THREADS;
    pthread_mutex_init(&count_mutex, NULL);

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_data[i].points_per_thread = points_per_thread;
        thread_data[i].seed = time(NULL) ^ (i * 10007);  // Unique seed for each thread
        pthread_create(&threads[i], NULL, monte_carlo_pi, &thread_data[i]);
    }

    // Join threads
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    // Estimate π
    double pi_estimate = 4.0 * global_inside_count / TOTAL_POINTS;
    printf("Estimated π = %.6f\n", pi_estimate);

    pthread_mutex_destroy(&count_mutex);
    return 0;
}
