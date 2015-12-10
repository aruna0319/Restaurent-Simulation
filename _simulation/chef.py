import random
import simpy
from time import sleep
from random import randint

class OrderProcessing():
    def __init__(self, env):
        self.env = env
        #obj = OrderProcessing(env)

    def processRequest(self, env, num):
        print env.now,num,'Processing Request'
        yield self.env.timeout(randint(5,10))
        # sleep(randint(3,4))
        print env.now,num,'Preparing food'
        yield self.env.timeout(randint(5,10))
        # sleep(randint(3,4))
        print env.now,num,'Call Server'
        yield self.env.timeout(randint(5, 10))
        # sleep(randint(3,4))
        print env.now,num,'Call Customer'
        # sleep(randint(3,4))
        env.exit()
        # self.processFood(env,num)

    def processFood(self, env, num):
        print env.now,num,'Preparing food'
        sleep(randint(3,4))
        # yield self.env.timeout(1)
        self.tellServer(env, num)


    def tellServer(self, env, num):
        print env.now,num,'Call Server'
        sleep(randint(3,4))
        self.callCustomer(env,num)

    def callCustomer(self, env, num):
        print env.now,num,'Call Customer'
        sleep(randint(3,4))



