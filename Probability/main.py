import enum
import random


class coin(enum.Enum):
    heads = 1
    tails = 2

def flipcoin():
    if random.random() > 0.5:
        return coin.tails
    else:
        return coin.heads

flips = int(input("How many coin flips?"))
headscount = 0

for i in range(0, 10):
    if flipcoin() == coin.heads:
        headscount += 1
