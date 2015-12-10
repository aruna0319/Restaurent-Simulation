import random

import simpy


RANDOM_SEED = 42
NUM_MACHINES = 2  # Number of machines in the OrderProcessing
cooktime = 5      # Minutes it takes to clean a order
T_INTER = 9       # Create a order every ~7 minutes
SIM_TIME = 20     # Simulation time in minutes


class OrderProcessing(object):
    """A OrderProcessing has a limited number of machines (``NUM_MACHINES``) to
    clean orders in parallel.

    orders have to request one of the machines. When they got one, they
    can start the cooking processes and wait for it to finish (which
    takes ``cooktime`` minutes).

    """
    def __init__(self, env, num_machines, cooktime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.cooktime = cooktime

    def cook(self, order):
        """The cooking processes. It takes a ``order`` processes and tries
        to clean it."""
        yield self.env.timeout(cooktime)
        print("OrderProcessing completed %s." %order)


def order(env, name, cw):
    """The order process (each order has a ``name``) arrives at the OrderProcessing
    (``cw``) and requests a cleaning machine.

    It then starts the cooking process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s Order request arrived at %.2f.' % (name, env.now))
    with cw.machine.request() as request:
        yield request

        print('%s chef starts order preparation at %.2f.' % (name, env.now))
        yield env.process(cw.cook(name))

        print('%s chef completes order preparation at %.2f.' % (name, env.now))


def setup(env, num_machines, cooktime, t_inter):
    """Create a OrderProcessing, a number of initial orders and keep creating orders
    approx. every ``t_inter`` minutes."""
    # Create the OrderProcessing
    orderprocessing = OrderProcessing(env, num_machines, cooktime)

    # Create 4 initial orders
    for i in range(4):
        env.process(order(env, 'order', orderprocessing))

    # Create more orders while the simulation is running
    while True:
         yield env.timeout(random.randint(t_inter-2, t_inter+2))
    #     i += 1
    #     env.process(order(env, 'order', orderprocessing))


# Setup and start the simulation
print('OrderProcessing')
#print('Check out http://youtu.be/fXXmeP9TvBg while simulating ... ;-)')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_MACHINES, cooktime, T_INTER))

# Execute!
if __name__ == '__main__':
    env.run(until=SIM_TIME)