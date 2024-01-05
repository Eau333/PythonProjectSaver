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

for i in range(0, flips):
    if flipcoin() == coin.heads:
        headscount += 1
percentage = headscount / flips * 100
print("You got "+str(headscount)+" heads. That is "+str(percentage)+"% heads.")

numsims = int(input("How many times do you want to play the game?"))
# game rules: each player throws a dice 3 times and if all of one players dice throws is higher than the other, that person wins
wins = 0
for i in range(0, numsims):
    subwins = 0
    for j in range(0,3):
        if random.randint(1, 6) > random.randint(1, 6):
            subwins += 1
    if subwins == 3:
        wins += 1
percentage = wins / numsims * 100
print("You won "+str(wins)+" times and you won "+str(percentage)+"% times.")