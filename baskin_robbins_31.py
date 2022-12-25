# TODO: pretty ugly 

from random import randint, choices, random
from itertools import groupby

def episode(policy1):
    game = [-1] * 31
    policy0 = random_policy()
    # player0 begins the game 
    roll = choices([1,2,3], policy0[0])[0]
    for i in range(roll):
        game[i] = 0
    cur_num = roll
    
    cur_player = 1
    cur_policy = policy1
    while cur_num < 31:
    
        roll = choices([1, 2, 3], cur_policy[cur_num - 1])[0]
        for i in range(roll):
            game[cur_num + i] = cur_player
        
        cur_player = (cur_player + 1) % 2
        cur_policy = policy0 if cur_player == 0 else policy1
        cur_num += roll 

    return game

# both at random
def prediction(episodes):
    returns = [0] * 31
    returns_loses = [0] * 31
    n = 0
    wins = 0
    for epi in episodes:
        n += 1
        # player 1 wins
        if epi[-1] == 0:
            wins += 1
            pos = 0
            for k, g in groupby(epi):
                pos += len(list(g))
                if k == 0:
                    returns[pos-1] += 1
        else:
            pos = 0
            for k, g in groupby(epi):
                pos += len(list(g))
                if k == 0:
                    returns_loses[pos-1] += 1

    return [v1/(v1+v2) for v1, v2 in zip(returns, returns_loses)]

# on-policy epsilon-soft
def epsilon_soft(epsilon=0.3, n_episodes=10):
    policy = random_policy()
    q = [[0, 0, 0] for _ in range(31)]
    rets = [[0, 0, 0] for _ in range(31)]

    n = 0 
    wins = 0
    for _ in range(n_episodes):
        n += 1
        epi = episode(policy)
        # player1 wins
        if epi[-1] == 0:
            wins += 1

            pos = 0
            epig = [list(g) for _, g in groupby(epi)]
            for g1, g2 in zip(epig, epig[1:]):

                pos += len(g1)
                action = len(g2)
                if g1[0] == 0:
                    rets[pos - 1][action - 1] += 1
                    q[pos-1][action-1] = rets[pos-1][action-1] / n
                    optimal_action = find_maxpos(q[pos-1]) 
                    if pos == 30:
                        nactions = 1
                    elif pos == 29:
                        nactions = 2
                    else: 
                        nactions = 3

                    for i in range(nactions):
                        if i == optimal_action:
                            policy[pos-1][i] = 1 - epsilon  +  epsilon/ nactions 
                        else:
                            policy[pos-1][i] = epsilon / nactions 
    return policy 

def find_maxpos(xs):
    m = max(xs)
    return choices([i for i, x in enumerate(xs) if x == m])[0]

# ties broken consi
def find_maxpos_c(xs):
    return xs.index(max(xs))


# def importance_sampling(n_episodes=10):
#     qvals = [[random(), random(), random()] for _ in range(31)]
#     c = [[0, 0, 0] for _ in range(31)]
#     behavior = random_policy() 
#     n = 0 
#     wins = 0
#     for _ in range(n_episodes):
#         n += 1
#         epi = episode(p0)
#         # player1 wins
#         if epi[-1] == 0:
#             wins += 1

#             pos = 0
#             epig = [list(g) for _, g in groupby(epi)]

#             w = 1 
#             probs_target = 1
#             probs_behavior = 1
#             for g1, g2 in zip(epig, epig[1:]):
#                 pos += len(g1)
#                 action = len(g2)
#                 if g1[0] == 0:
#                     qval = qvals[pos-1][action-1]

#                     # qvals[pos-1][action-1] = qval + (w / c[pos-1][action-1])*(30- qval)
#                     qvals[pos-1][action-1] = qval + (1/10)*(1- qval)

#                     optimal_action1 = find_maxpos_c(qvals[pos-1]) 
#                     optimal_action2 = find_maxpos_c(policy[pos-1]) 
#                     policy[pos-1] = [1 if i == optimal_action1 else 0 for i in range(3)]

#                     if optimal_action1 != optimal_action2:
#                         break

#                     if pos == 30:
#                         nactions = 1
#                     elif pos == 29:
#                         nactions = 2
#                     else: 
#                         nactions = 3

#                     w = w * nactions                   

#     # for i, x in enumerate(qvals):
#     #     print(i+1, x)

#     return policy 


# total random policy
def random_policy():
    probs = [[1.0 / 3, 1.0 / 3, 1.0 / 3] for _ in range(28)]
    probs.append([1.0 / 2, 1.0 / 2, 0])
    probs.append([1.0, 0, 0]) 
    return probs 

# def simp_policy():
#     probs = [[0, 1.0, 0] for _ in range(28)]
#     probs.append([0, 1.0, 0])
#     probs.append([1.0, 0, 0]) 
#     return probs 


p0 = random_policy()
for i, val in enumerate(prediction(episode(p0) for _ in range(100000))):
    print(i+1, val)

# res = epsilon_soft(epsilon=0.1, n_episodes=10)
# res = importance_sampling(n_episodes=10000)
# for i, x in enumerate(res):
#     print(i+1, x)


# for i, val in enumerate(prediction(episode(res) for _ in range(10000))):
#     print(i, val)