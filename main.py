#GroceryStoreSim.py
#Name: Salsabiel Khair Allah
#Date: Nov.30
#Assignment: Lab 11

# Commit message:
# Add full SimPy grocery store simulation and summary
# - Implemented shopper, checker, and arrival processes
# - Added extra statistics including avg items, max wait, and idle time
# - Created summary document explaining what was learned

import simpy
import random

eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items // 2  # 0.5 min per item
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        # No shoppers waiting
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)

        # Take next shopper
        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1
        yield env.timeout(checkoutTime)

        # Log event: (id, items, arrival, doneShopping, doneCheckout)
        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))


# -----------------------------
# Customer arrival generator
# -----------------------------
def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(2)  # arrival every 2 minutes


# -----------------------------
# Process results + extra stats
# -----------------------------
def processResults():
    totalWait = 0
    totalItems = 0
    totalShopping = 0
    maxWait = 0

    totalShoppers = len(eventLog)

    for e in eventLog:
        shopperItems = e[1]
        shoppingTime = e[3] - e[2]
        waitTime = e[4] - e[3]

        totalItems += shopperItems
        totalShopping += shoppingTime
        totalWait += waitTime

        if waitTime > maxWait:
            maxWait = waitTime

    avgWait = totalWait / totalShoppers
    avgItems = totalItems / totalShoppers
    avgShopping = totalShopping / totalShoppers

    print("Total shoppers:", totalShoppers)
    print("Average items bought: %.2f" % avgItems)
    print("Average shopping time: %.2f minutes" % avgShopping)
    print("Average wait time: %.2f minutes" % avgWait)
    print("Max wait time: %.2f minutes" % maxWait)
    print("Total idle time for all checkers:", idleTime)


# -----------------------------
# Main simulation setup
# -----------------------------
def main():
    numberCheckers = 5

    env = simpy.Environment()
    env.process(customerArrival(env))

    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180)  # 3 hours

    processResults()


if __name__ == "__main__":
    main()

