from itertools import combinations, combinations_with_replacement, product
from autochess import *
from Entitys import *

CHAMPIONS_1: dict[str, dict[str, int]] = {champion['name']: Champion(**champion, level=1) for champion in json['personajes']}
CHAMPIONS_2: dict[str, dict[str, int]] = {champion['name']: Champion(**champion, level=2) for champion in json['personajes']}
CHAMPIONS_3: dict[str, dict[str, int]] = {champion['name']: Champion(**champion, level=3) for champion in json['personajes']}
CHAMPIONS_1=list(CHAMPIONS_1.values())[0:3]
CHAMPIONS_2=list(CHAMPIONS_2.values())[0:3]
CHAMPIONS_3=list(CHAMPIONS_3.values())[0:3]
golds = range(0, 101)
rounds = range(0, 50)

x = combinations_with_replacement(CHAMPIONS_1+[None], 5)
y = combinations_with_replacement(CHAMPIONS_1 + CHAMPIONS_2 + CHAMPIONS_3+[None], 18)
z = product(rounds, golds, x, y)

print(str(next(z)))


