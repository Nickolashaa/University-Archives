import json


def SPERMA(name):
    with open('app/games/weird_game.json', 'r') as f:
        stat = json.load(f)
        f.close()
    if name not in stat.keys():
        stat[name] = 1
    else:
        stat[name] += 1
    with open('app/games/weird_game.json', 'w') as f:
        json.dump(stat, f)
        f.close()
    return stat[name]