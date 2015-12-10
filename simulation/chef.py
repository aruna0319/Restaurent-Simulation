import random
import simpy
from time import sleep
from random import randint

class OrderProcessing():

    def __init__(self, env):
        self.env = env
        #obj = OrderProcessing(env)

    def gestures(self, env, num):
        wishes = ['Hi !!', 'Hello!!', 'Hi!! What can I get for you ?', 'Hello!! How can I help you']
        reply_to_wishes = ['Hello!!!', 'How are you!!']
        print num, '      Service person greets: ', random.choice(wishes), '        ', env.now
        sleep(1)
        print num, '      Customer replies: ', random.choice(reply_to_wishes), '        ', env.now

        if(randint(1,2)==1):
            queries = ['Whats available for today?', 'Hi, anything special today !!', 'Whats the cheapest one?']
            answer_available=['hii!! All the item on the list are available', 'We have burgers, fries, drinks and shakes', 'We have all the items today, you can choose anything you want']
            answer_cheap = ['Sorry, no special discount for today, all are of regular price', ' Yes, We have a variety of items that are cheap']

            temp = random.choice(queries)
            print num, '      Customer asks the service person: ', temp, '        ', env.now

            sleep(1)

            if(temp == 'Whats available for today?' or temp == 'Hi, anything special today?'):
                print num, '      Service Person replies: ', random.choice(answer_available), '        ', env.now
            else:
                print num, '      Service Person replies: ', random.choice(answer_cheap), '        ', env.now

        sleep(1)

    def chooseItems(self, env, num):

        items=['burger', 'pizza', 'burrito', 'shakes', 'drinks', 'fries']

        itemsDressing = ['Sauce','No Sauce', 'Extra Pickles', 'Extra Olives', 'No Olives', 'Extra Mayo', 'No Mayo', 'No Pickles', 'Vegetarian']
        shakesTypes = ['Vanilla Shake', 'Strawberry Shake', 'Chocolate Shake', 'Vanilla-Strawberry Shake', 'Oreo Cookie Shake']
        shakesDressing = ['No Whipped Cream', 'Extra Whipped Cream', 'Extra Chocolate']
        friesDressing = ['Regular Fries, No Salt', 'Curly Fries, No Salt', 'Regular Fries', 'Curly Fries', 'Regular Fries, Extra Salt', 'Curly Fries, Extra Salt']
        drinksDressing = ['No ice', 'Extra ice']

        no_of_orders=randint(1, 6)
        print num, '       I would like to order ', '        ', env.now
        # print 'no_of_orders: ', no_of_orders
        sleep(1)
        while no_of_orders != 0:
            order = random.choice(items)
            print num, '           ', order, '        ', env.now
            # sleep(1)
            yield self.env.timeout(randint(3, 4))

            if order == 'burger' or order == 'pizza' or order == 'burrito':
                if randint(1, 2) == 1:
                    print num, '               Modify: ', random.choice(itemsDressing), '        ', env.now
                    sleep(1)

            if order == 'fries':
                if randint(1, 2) == 1:
                    print num, '               Modify: ', random.choice(friesDressing), '        ', env.now
                    sleep(1)

            if order == 'drinks':
                if randint(1, 2) == 1:
                    print num, '               Modify: ', random.choice(drinksDressing), '        ', env.now
                    sleep(1)

            if order == 'shakes':
                print num, '                   Modify: ', random.choice(shakesTypes), '        ', env.now
                if randint(1, 2) == 1:
                    print num, '               Modify: ', random.choice(shakesDressing), '        ', env.now
                    sleep(1)

            no_of_orders -= 1

        print num, '       Service Person tells the bill Amount', '        ', env.now
        sleep(1)

    def ask(self, env, num):
        bye_messages = ['Thank You !!', 'Thank You!! Have a good day!!', 'Thank you !! Visit us again !!']

        print num, '      For here or To go', '        ', env.now
        sleep(1)

        if(randint(1, 2) == 1):
            print num, '      Customer says: For here', '        ', env.now
        else:
            print num, '      Customer says: To Go', '        ', env.now

        print num, '      Service Person says: ', random.choice(bye_messages), '        ', env.now
        sleep(1)

    def processRequest(self, env, num):

        self.gestures(env, num)
        yield self.env.timeout(randint(3, 6))
        self.chooseItems(env, num)
        yield self.env.timeout(randint(3, 6))
        self.ask(env, num)

        print num, '      Processing Request', '        ', env.now
        yield self.env.timeout(randint(3, 4))
        # sleep(randint(3,4))
        print num, '      Cook is Preparing food', '        ', env.now
        yield self.env.timeout(randint(10,20))
        # sleep(randint(3,4))
        print num, '      Cook calls the Service Person', '        ', env.now
        yield self.env.timeout(randint(5, 10))
        # sleep(randint(3,4))
        print num, '      The service person calls the Customer', '        ', env.now
        # sleep(randint(3,4))
        env.exit()
        # self.processFood(env,num)
    """
    def processFood(self, env, num):
        print env.now, num, '       Preparing food'
        sleep(randint(3,4))
        # yield self.env.timeout(1)
        self.tellServer(env, num)

    def tellServer(self, env, num):
        print env.now, num, '        Call Server'
        sleep(randint(3,4))
        self.callCustomer(env,num)

    def callCustomer(self, env, num):
        print env.now, num, '       Call Customer'
        sleep(randint(3,4))
    """