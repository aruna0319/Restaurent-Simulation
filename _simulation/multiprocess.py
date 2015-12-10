__author__ = 'vikra_000'
from random import randint
import random
import simpy
from threading import Timer
from time import sleep
import multiprocessing as mp
from multiprocessing import Process, freeze_support


RANDOM_SEED = randint(10,199)
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience
ORDER_STATUS = 0

# def source(env, number, interval, counter):
#     global ORDER_STATUS
#     for i in range(number):
#         ORDER_STATUS = 0
#         c = action(env, 'Customer%02d' % i, counter, time_in_bank=20.0)
#         env.process(c)
#         t = random.expovariate(1.0 / interval)
#         yield env.timeout(t)


def action():
    global ORDER_STATUS
    env = simpy.Environment()
    counter = simpy.Resource(env, capacity=1)
    time_in_bank = 20
    for k in range(NEW_CUSTOMERS):
        name = 'Customer%02d' % k
    arrive = env.now
    print arrive
    while ORDER_STATUS == 0:
        x = randint(1, 6) * 1
        #print x
        if x == 1:
            output.put(env.now, name, 'sit and relax')
            #t = randint(1, 5)
            #print t
            sleep(randint(1,20))
            #Timer(t, action,args=(env, name, counter, time_in_bank)).start()
        elif x == 2:
            output.put(env.now, name, 'stand')
            sleep(randint(1,20))
            #Timer(randint(1, 5), action,args=(env, name, counter, time_in_bank)).start()
        elif x == 3:
            output.put(env.now, name, 'Make Order')
            ORDER_STATUS = 1
            sleep(randint(1,20))
        elif x == 4:
            output.put(env.now, name, 'Views Menu')
            #Timer(randint(1, 5), action,args=(env, name, counter, time_in_bank)).start()
            sleep(randint(1,20))
        elif x == 5:
            output.put(env.now, name, 'talk to other people')
            #Timer(randint(1, 5), action,args=(env, name, counter, time_in_bank)).start()
            sleep(randint(1,20))
        else:
            with counter.request() as req:
                patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
                # Wait for the counter or abort at the end of our tether
                results = yield req | env.timeout(patience)

                wait = env.now - arrive

                if req in results:
                    # We got to the counter
                    print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

                    tib = random.expovariate(1.0 / time_in_bank)
                    yield env.timeout(tib)
                    print('%7.4f %s: Finished' % (env.now, name))
                    ORDER_STATUS = 1

                else:
                    # We reneged
                    print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))
                    sleep(randint(1,20))


if __name__ == '__main__':
    freeze_support()

    # Setup and start the simulation
    print('Start - Random Seed: %s' % RANDOM_SEED)
    random.seed(RANDOM_SEED)


    # Define an output queue
    output = mp.Queue()

    # Setup a list of processes that we want to run
    processes = [mp.Process(target=action) for x in range(NEW_CUSTOMERS)]
    print processes

    # Run processes
    for p in processes:
        p.daemon = False
        print p
        f = p.start()
        #print f
    # Exit the completed processes
    # for p in processes:
    #     p.join()

        # Get process results from the output queue
        #result = [output.get() for p in processes]

        #print(result)


        # Start processes and run
        # counter = simpy.Resource(env, capacity=1)
        # env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
        # env.run()