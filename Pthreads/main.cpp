/**
 *  pthread based Producer Consumer implementation
 * 
 *  @author Yanping "Angie" Zhang
 *  @author Aaron S. Crandall
 *  @author Jovan Koledin
 *  @copyright 2021
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
#include "buffer.h"


/* Create ring buffer space */
buffer_item buffer[BUFFER_SIZE];

/* Ring buffer indicies
  See: https://en.wikipedia.org/wiki/Circular_buffer
*/
int insertBufferIndex = 0;
int removeBufferIndex = 0;

/* TODO: define semaphores and mutex here */
pthread_mutex_t mtx;
sem_t empty, full;


/* Track number of inserts and removes done */
int total_inserts, insert_index = 0;
int total_removes, remove_index = 0;

/* pthread methods forward definitions */
void *producer(void *param);
void *consumer(void *param);

/* See chapter 7 */
int insert_item(buffer_item item)
{
    /* Acquire Empty Semaphore */
    sem_wait(&empty);
    /* Acquire mutex lock to protect buffer */
    total_inserts++;
	pthread_mutex_lock(&mtx);
	//Insert
	buffer[insert_index++] = item;
	insert_index = insert_index % BUFFER_SIZE;
	total_inserts++;
    /* Release mutex lock and full semaphore */
	pthread_mutex_unlock(&mtx);
	sem_post(&full);
    return 0;
}

int remove_item(buffer_item *item)
{
    /* Acquire Full Semaphore */
	sem_wait(&full);
    /* Acquire mutex lock to protect buffer */
    total_removes++;
 	pthread_mutex_lock(&mtx);
	//Remove
	*item = buffer[remove_index++];
	buffer[remove_index++] = 0;
	remove_index = remove_index % BUFFER_SIZE;
	total_removes++;
    /* Release mutex lock and empty semaphore */
	pthread_mutex_unlock(&mtx);
	sem_post(&empty);
    return 0;
}



int main(int argc, char* argv[])
{
	//Seed time
	srand(time(0));
    int sleepTime = 1;
    int producerThreads, consumerThreads = 0;

	//Initialize semaphores and mutex
	pthread_mutex_init(&mtx, NULL);
	sem_init(&empty, 0, BUFFER_SIZE);
	sem_init(&full, 0, 0);

    if(argc != 4)
    {
        fprintf(stderr, "Usage: <sleep time> <producer threads> <consumer threads>\n");
        return -1;
    }

    /* Call atoi to get argument values from argv */
	sleepTime = atoi(argv[1]);
	producerThreads = atoi(argv[2]);
	consumerThreads = atoi(argv[3]);

    /* Create the producer and consumer threads */
    for(int j = 0; j < consumerThreads; j++)
    {
 		pthread_t t;
		pthread_attr_t attr;
		pthread_attr_init(&attr);
		pthread_create(&t, &attr, consumer, NULL);

    }

	for(int j = 0; j < producerThreads; j++)
    {
 		pthread_t t;
		pthread_attr_t attr;
		pthread_attr_init(&attr);
		pthread_create(&t, &attr, producer, NULL);

    }


    /* Sleep for user specified time */
    printf("Main thread sleeping for %d secs\n", sleepTime);
    sleep(sleepTime);
    printf("Total inserts: %d\n", total_inserts);
    printf("Total removes: %d\n", total_removes);


    if(total_removes > 0 && total_inserts > 0)
    {
        return 0;
    } else {
        return 1;
    }
}


/* Inserts into buffer if it's got empty space */
void *producer(void *param)
{
	buffer_item item;
	int random;

    while(true)
    {
		random = rand() % BUFFER_SIZE;
		sleep(random);
		item = rand();
		if(insert_item(item))
			fprintf(stderr, "report error condition, Producer");
		else
			printf("producer produced %d\n", item);

    }
}

/* Removes from buffer if there's data */
void *consumer(void *param)
{
	buffer_item item;
	int random;

    while(true)
    {
 		random = rand() % BUFFER_SIZE;
		sleep(random);
		item = rand();
		if(remove_item(&item))
			fprintf(stderr, "report error condition, Consumer");
		else
			printf("consumer consumed %d\n", item);
    }
}
