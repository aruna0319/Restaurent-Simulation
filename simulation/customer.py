__author__ = 'vikra_000'
from random import randint
import random
import simpy
from threading import Timer
from time import sleep
import chef
from chef import OrderProcessing

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

"""
wishes = ['Hi !!', 'Hello!!', 'Hi!! What can I get for you ?', 'Hello!! How can I help you']
reply_to_wishes = ['Hello!!!', 'How are you!!']

queries = ['Whats available for today?', 'Hi, anything special today?', 'Whats the cheapest one?']

answer_available=['hii!! All the item on the list are available', 'We have burgers, fries, drinks and shakes', 'We have all the items today, you can choose anything you want']
answer_cheap = ['Sorry, no special discount for today', ' We have a variety of items that are cheap']

bye_messages = ['Thank You !!', 'Thank You!! Have a good day!!', 'Thank you !! Visit us again !!']
"""


def action(env, name, counter, time_in_restaurant):
    global ORDER_STATUS
    arrive = env.now

    while ORDER_STATUS == 0:
        x = randint(1, 14)

        if x == 1:
            print name, '      Sit and Relax for a while', '        ', env.now
            sleep(1)
            yield env.timeout(randint(3, 8))

        elif x == 2:
            print name, '      Stand in the corner', '        ', env.now
            sleep(1)
            yield env.timeout(randint(3, 8))

        elif x == 3 or x == 5 or x == 7 or x == 9 or x == 11:
            print name, '      Make Order', '        ', env.now
            """
            gestures()
            chooseItems()
            ask()
            """
            ORDER_STATUS = 1
            sleep(randint(1, 2))
            yield env.timeout(randint(3, 8))
            env.process(boost.processRequest(env, name))

        elif x == 4:
            print name, '      Unable to decide, Views Menu', '        ', env.now
            sleep(1)
            yield env.timeout(randint(3, 8))

        elif x == 6:
            print name, '      Talk to surrounding people', '        ', env.now
            sleep(1)
            yield env.timeout(randint(3, 8))
            sleep(1)

        elif x == 8:
            print name, '      Doing his own personal work', '        ', env.now
            sleep(1)
            time=env.timeout(randint(3, 8))
            yield time

        elif x == 10:
            print name, '      Quarrels with other customers and leaves', '        ', env.now
            ORDER_STATUS = 1
            sleep(1)
            time=env.timeout(randint(3, 8))
            yield time

        elif x == 12:
            print name, '      Not interested, wishes to leave', '        ', env.now
            ORDER_STATUS = 1
            sleep(1)
            time=env.timeout(randint(3, 8))
            yield time

        elif x == 13:
            print name, '      Visits the washroom', '        ', env.now
            sleep(1)
            time=env.timeout(randint(3, 8))
            yield time

        else:
            with counter.request() as req:
                waiting = random.uniform(MIN_WAITING, MAX_WAITING)
                # Wait for the counter or abort at the end of our tether
                results = yield req | env.timeout(waiting)

                wait = env.now - arrive

                if req in results:
                    # We got to the counter
                    print('%7.4f %s:        Wait for ordering %6.3f' % (env.now, name, wait))
                    sleep(randint(1, 1))
                    tib = random.expovariate(1.0 / time_in_restaurant)

                    yield env.timeout(tib)

                    print name, '      Make Order', '        ', env.now
                    """
                    gestures()
                    chooseItems()
                    ask()
                    """
                    ORDER_STATUS = 1
                    sleep(randint(1, 2))
                    yield env.timeout(randint(3, 8))
                    env.process(boost.processRequest(env, name))
                else:
                    # We reneged
                    print('%7.4f %s:        Huge rush cant order exiting restaurant after %6.3f' % (env.now, name, wait))
                    ORDER_STATUS = 1
                    sleep(randint(3, 8))

# Setup and start the simulation
# print('Start - Random Seed: %s - Initial Number of Customers %s' % (RANDOM_SEED, NEW_CUSTOMERS))
random.seed(RANDOM_SEED)

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()(until=SIM_TIME)