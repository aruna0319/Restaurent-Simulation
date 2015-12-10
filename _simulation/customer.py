__author__ = 'vikra_000'
from random import randint
import random
import simpy
from threading import Timer
from time import sleep
import chef
from chef import OrderProcessing
from xtermcolor import colorize


RANDOM_SEED = randint(10,199)
NEW_CUSTOMERS = randint(5,10)  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_WAITING = 1  # Min. customer WAITING
MAX_WAITING = 3  # Max. customer WAITING
ORDER_STATUS = 0
SIM_TIME = 2
env = simpy.Environment()
boost = OrderProcessing(env)

def source(env, number, interval, counter):
    global ORDER_STATUS
    global CUST_CHECK
    for i in range(number):
        ORDER_STATUS = 0
        c = action(env, 'Customer%02d' % i, counter, time_in_restaurant=20.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)
    # More customers visit while the simulation is running
    while True:
        yield env.timeout(random.randint(1, 3))
        i += 1
        sleep(randint(3, 12))
        ORDER_STATUS = 0
        env.process(action(env, 'Customer%02d' % i, counter, time_in_restaurant=20.0))
        print ('i: ', i)


def action(env, name, counter, time_in_restaurant):
    global ORDER_STATUS
    arrive = env.now
    print ('entered')

    while ORDER_STATUS == 0:
        x = randint(1, 15) * 1
        #print x
        if x == 1 or x == 6:
            print (colorize(str(env.now) + " " + name + ' sit and relax', ansi=4))
            print (colorize(' sit and relax', ansi=4))
            sleep(randint(1, 1))
            yield env.timeout(randint(3, 8))

        elif x == 2 or x == 7 or x == 11:
            print (colorize(str(env.now) + " " + name + ' stand', ansi=4))
            sleep(randint(1, 1))
            yield env.timeout(randint(3, 8))

        elif x == 3 or x == 8 or x == 12:
            print (colorize(str(env.now) + " " + name + ' Make Order', ansi=4))
            ORDER_STATUS = 1
            sleep(randint(1, 1))
            yield env.timeout(randint(3, 8))
            #chef.processRequest(env, name)
            # boost.processRequest(env, name)
            env.process(boost.processRequest(env, name))
            #kitchen.setup(env,2,5,7)

        elif x == 4 or x == 9 or x == 13:
            print (colorize(str(env.now) + " " + name + ' Views Menu', ansi=4))
            print (colorize(' Views Menu', ansi=4))
            sleep(randint(1, 1))
            yield env.timeout(randint(3, 8))

        elif x == 5 or x == 10:
            print (colorize(str(env.now) + " " + name + ' talk to other people', ansi=4))
            yield env.timeout(randint(3, 8))
            sleep(randint(1, 1))

        else:
            with counter.request() as req:
                waiting = random.uniform(MIN_WAITING, MAX_WAITING)
                # Wait for the counter or abort at the end of our tether
                results = yield req | env.timeout(waiting)

                wait = env.now - arrive

                if req in results:
                    # We got to the counter
                    print (colorize(('%7.4f %s: Wait for ordering %6.3f' % (env.now, name, wait)), ansi=4))
                    #print('%7.4f %s: Wait for ordering %6.3f' % (env.now, name, wait))
                    sleep(randint(1, 1))
                    tib = random.expovariate(1.0 / time_in_restaurant)
                    yield env.timeout(tib)
                    print (colorize(('%7.4f %s: Make Order' % (env.now, name)), ansi=4))
                    #print('%7.4f %s: Make Order' % (env.now, name))
                    sleep(randint(1, 1))
                    ORDER_STATUS = 1
                    #chef.processRequest(env, name)
                    # temp=boost.processRequest(env, name)
                    env.process(boost.processRequest(env, name))
                    #kitchen.setup(env,2,5,7)

                else:
                    # We reneged
                    print (colorize(('%7.4f %s: Huge rush cant order exiting restaurant after %6.3f' % (env.now, name, wait)), ansi=2))
                    #print('%7.4f %s: Huge rush cant order exiting restaurant after %6.3f' % (env.now, name, wait))
                    sleep(randint(3, 8))

# Setup and start the simulation
print('Start - Random Seed: %s - Number of Customers %s' % (RANDOM_SEED, NEW_CUSTOMERS))
random.seed(RANDOM_SEED)


# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()(until=SIM_TIME)