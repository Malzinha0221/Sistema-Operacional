import threading
import time
import random

class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []
        self.empty = threading.Semaphore(size)
        self.full = threading.Semaphore(0)
        self.mutex = threading.Lock()

    def insert(self, item):
        self.empty.acquire()
        self.mutex.acquire()
        self.buffer.append(item)
        print(f"Produzido: {item}, Buffer: {self.buffer}")
        self.mutex.release()
        self.full.release()

    def remove(self):
        self.full.acquire()
        self.mutex.acquire()
        item = self.buffer.pop(0)
        print(f"Consumido: {item}, Buffer: {self.buffer}")
        self.mutex.release()
        self.empty.release()
        return item

def producer(buffer, id):
    while True:
        item = random.randint(1, 100)
        buffer.insert(item)
        time.sleep(random.random())

def consumer(buffer, id):
    while True:
        item = buffer.remove()
        time.sleep(random.random())

if __name__ == "__main__":
    buffer_size = 5
    buffer = Buffer(buffer_size)

    num_producers = 2
    num_consumers = 2

    producers = []
    consumers = []

    for i in range(num_producers):
        producers.append(threading.Thread(target=producer, args=(buffer, i)))

    for i in range(num_consumers):
        consumers.append(threading.Thread(target=consumer, args=(buffer, i)))

    for producer_thread in producers:
        producer_thread.start()

    for consumer_thread in consumers:
        consumer_thread.start()

    for producer_thread in producers:
        producer_thread.join()

    for consumer_thread in consumers:
        consumer_thread.join()