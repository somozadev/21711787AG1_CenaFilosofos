
# Symmetric solution to the "dining philosophers"
# problem. Uses a semaphore as the "butler" to avoid
# deadlock.

import sys
import threading
import time

class Semaphore(object):

    def __init__(self, initial): # initial method
        self.lock = threading.Condition(threading.Lock()) # thread lock condition
        self.value = initial
 
    def up(self):  # new philosopher sits
        with self.lock:
            self.value += 1
            self.lock.notify()

    def down(self):  # philosopher gets up
        with self.lock:
            while self.value == 0:
                self.lock.wait()
            self.value -= 1

class ChopStick(object):

    def __init__(self, number):
        self.number = number           # chop stick ID
        self.user = -1                 # keep track of philosopher using it
        self.lock = threading.Condition(threading.Lock()) # thread lock condition
        self.taken = False # this fork is now available

    def take(self, user):         # used for synchronization, philosopher takes fork
        with self.lock:
            while self.taken == True: # while this fork is taken, wait
                self.lock.wait()
            self.user = user # the philosopher that has this fork
            self.taken = True # this fork is not available
            sys.stdout.write("p[%s] took c[%s]\n" % (user, self.number))
            self.lock.notifyAll() # notifies every thread

    def drop(self, user):         # used for synchronization, philosopher drops fork
        with self.lock:
            while self.taken == False: # while this fork is free, wait
                self.lock.wait()
            self.user = -1 # none philosopher that has this fork
            self.taken = False # this fork is now available
            sys.stdout.write("p[%s] dropped c[%s]\n" % (user, self.number))
            self.lock.notifyAll() # notifies every thread


class Philosopher (threading.Thread):

    def __init__(self, number, left, right, butler): #init method
        threading.Thread.__init__(self) #init thead to current philosopher
        self.number = number            # philosopher number
        self.left = left                # assing left fork
        self.right = right              # assing right fork
        self.butler = butler            # assing butler

    def run(self):
        for i in range(20):
            self.butler.down()              # start service by butler
            time.sleep(0.1)                 # think
            self.left.take(self.number)     # pickup left chopstick
            time.sleep(0.1)                 # (yield makes deadlock more likely)
            self.right.take(self.number)    # pickup right chopstick
            time.sleep(0.1)                 # eat
            self.right.drop(self.number)    # drop right chopstick
            self.left.drop(self.number)     # drop left chopstick
            self.butler.up()                # end service by butler
        sys.stdout.write("p[%s] finished thinking and eating\n" % self.number)


def main():
    # number of philosophers / chop sticks
    n = 5

    # butler for deadlock avoidance (n-1 available)
    butler = Semaphore(n-1)

    # list of chopsticks
    c = [ChopStick(i) for i in range(n)]

    # list of philsophers
    p = [Philosopher(i, c[i], c[(i+1)%n], butler) for i in range(n)]

    for i in range(n): # foreach philosopher in array -> start thread
        p[i].start()


if __name__ == "__main__":
    main()

