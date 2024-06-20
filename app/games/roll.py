import random
import json


def rolling(name):
    res = random.randint(0, 1)
    with open('app/games/roll.json', 'r') as f:
        stat = json.load(f)
        f.close()
    if name not in stat.keys() or not res:
        stat[name] = 0
    else:
        stat[name] += 1
    with open('app/games/roll.json', 'w') as f:
        json.dump(stat, f)
        f.close()
    return stat[name]