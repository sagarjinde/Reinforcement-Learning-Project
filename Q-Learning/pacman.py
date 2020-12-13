# NOTE: This code is initialized with size = 3 and number of food pellet = 3
# The total number of states generated for 3*3 world is: 37665
# In case you would like to test this code for a greater size world,
# please increase the epoch_count which is initially size to 10000 to atleast 10 million
# reason: This is because for a world of size=4, we get 2484480 number of states.
# And this number of states increases exponentially with increase of world size.


import random
from itertools import combinations
import matplotlib.pyplot as plt 

# print("enter world size")
# size = int(input())
# print("size: ", size)

# food_pellet_count = random.randint(1, size * size + 1)

pacman_actions = [(0,0),(-1,0),(1,0),(0,-1),(0,1)]
ghost_actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
epslon = 0.01
# alpha = 0.9
gamma = 0.9
size = 3
food_pellet_count = size
Q = {}
alpha_count = {}
epoch_count = 10000

def outOfBound(size, r, c):
    if r == -1 or r == size:
        return True
    elif c == -1 or c == size:
        return True
    else:
        return False


total_locations = []
for i in range(size):
    for j in range(size):
        total_locations.append((i, j))

def generateQ(size):
    locations = total_locations.copy()

    for f in range(size+1):
        for ploc in locations:
            pacman_loc = ploc                           # pacman location
            ptemp_locations = locations.copy()
            ptemp_locations.remove(pacman_loc)          # locations left after removing pacman
            # adding a location (-1,-1) to ghost which represents all states where ghost is out of bound
            for gloc in ptemp_locations + [(-1,-1)]:
                ghost_loc = gloc                        # ghost location
                food_locations = tuple(combinations(ptemp_locations, f))
                for food_loc in food_locations:
                    food_loc = frozenset(set(food_loc))
                    s = tuple([pacman_loc,ghost_loc,food_loc])
                    for a in pacman_actions:
                        Q[tuple([s,a])] =  0.0          # Q_method(size,s,a)
                        alpha_count[tuple([s,a])] = 0

def updateQ(s,a,r,s_prime,a_prime=(-1, -1)):
    alpha_count[tuple([s,a])] += 1
    if r > 0:
        Q[tuple([s,a])] = Q[tuple([s,a])] + (r + gamma*Q[tuple([s_prime,a_prime])] - Q[tuple([s,a])] )/alpha_count[tuple([s,a])]
    else:
        Q[tuple([s,a])] = Q[tuple([s,a])] + (r - Q[tuple([s,a])] )/alpha_count[tuple([s,a])]


def print_board(s):

    (pacman,ghost,food_pellet_loc) = s
    #print(pacman,ghost,food_pellet_loc)
    for i in range(-1,size+1):
        for j in range(-1,size+1):
            if i == -1 or i == size or j == -1 or j == size:
                print('W',end=' ')
            elif (i,j) == pacman:
                print('P',end=' ')
            elif (i,j) == ghost:
                print('G',end=' ')
            elif (i,j) in food_pellet_loc:
                print('F',end=' ')
            else:
                print('.',end=' ')
        print()

    print('stay',Q[tuple([s,(0,0)])])
    print('left',Q[tuple([s,(0,-1)])])
    print('right',Q[tuple([s,(0,1)])])
    print('bottom',Q[tuple([s,(1,0)])])
    print('top',Q[tuple([s,(-1,0)])])
    print()


class Environment:
    def __init__(self, size, food_pellet_count):
        self.size = size
        self.food_pellet_count_env = food_pellet_count

    def initialize(self):

        self.score = 0
        self.reward = 0
        self.food_pellet_count = self.food_pellet_count_env

        # creating all possible map locations
        self.locations = total_locations.copy()

        random.shuffle(self.locations)

        # initialize pacman, ghost, food pellat location
        self.pacman = self.locations.pop()
        self.ghost = self.ghost_init(self.pacman)
        self.locations.remove(self.ghost)

        self.food_pellet_loc = []
        for f in range(self.food_pellet_count):
            self.food_pellet_loc.append(self.locations.pop())

    def ghost_init(self, pacman):
        (r,c) = pacman
        possible_ghost_locations = {(r,0),(0,c),(r,self.size-1),(self.size-1,c)}
        possible_ghost_locations.discard(pacman)
        possible_ghost_locations = list(possible_ghost_locations)
        return random.choice(possible_ghost_locations)

    def getState(self):
        state = []
        state.append(self.pacman)
        state.append(self.ghost)
        state.append(frozenset(set(self.food_pellet_loc)))
        state = tuple(state)
        return state

    def policy(self,s,actions):
        # epslon-greedy policy

        #print("********************")
        a = (-1, -1)
        if random.random() > epslon:
            #print("greedy")
            maximum = -1000
            pac_actions = []
            for act in actions:
                if Q[tuple([s,act])] == maximum:
                    pac_actions.append(act)
                #print("Q[{},{}]: {}".format(s,act,Q[tuple([s,act])]))  # TODO
                if Q[tuple([s,act])] > maximum:
                    pac_actions.clear()                                 # if multiple actions have same max Q value,
                    maximum = Q[tuple([s,act])]                         # then we need to pick one the max at random
                    pac_actions.append(act)
            a = random.choice(pac_actions)
        else:
            #print("random")
            a = random.choice(pacman_actions)

        #print("returning: ",a)
        #print("********************")

        return a

    def terminal(self):
        """Return whether the episode is over."""
        # if self.reward == -100:
        #     return True
        # elif self.food_pellet_count == 0:
        #     return True
        # else:
        #     return False

        if self.reward == -100:
            return True
        else:
            return False

    def getReward(self):
        return self.reward

    def getScore(self):
        return self.score

    def getOptimalAction(self,s):
        maximum = -10000
        a = (-1,-1)
        for act in pacman_actions:
            if Q[tuple([s,act])] > maximum:                     # problem here: if ghost is out of bound, then what??
                maximum = Q[tuple([s,act])]
                a = act

        return a


    def update(self,s,a):
        # get present location
        (pacman,ghost,food_pellet_loc) = s

        (pr,pc) = pacman
        (gr,gc) = ghost

        # pacman makes move. Update pacman location
        (dr,dc) = a
        (upr,upc) = (pr+dr,pc+dc)
        self.pacman = (upr,upc)

        # ghost makes move, Update ghost location
        if outOfBound(self.size,gr,gc):                          # if ghost went out of bounds in the previous trun
            self.ghost = self.ghost_init(self.pacman)
        else:
            (dr,dc) = random.choice(ghost_actions)
            (ugr,ugc) = (gr+dr,gc+dc)
            if outOfBound(self.size,ugr,ugc):
                (ugr,ugc) = (-1,-1)
            self.ghost = (ugr, ugc)

        self.reward = 1

        # Negative reward for hitting the ghost
        if self.pacman == self.ghost:
            self.reward = -100
        # if ghost and pacman cross each other
        elif (pacman, ghost) == (self.ghost, self.pacman):
            self.reward = -100
        # Negative reward for hitting a wall
        elif outOfBound(self.size,upr,upc):
            self.reward = -100
        # Positive reward for consuming a pellet
        elif self.pacman in food_pellet_loc:
            self.food_pellet_count -= 1
            self.score += 1
            self.reward = 10
            self.food_pellet_loc.remove(self.pacman)


def qLearning():

    score_list = []
    avg_score_list = [0]*100
    generateQ(size)
    env = Environment(size, food_pellet_count)
    print("Welcome to the game of pacman!")
    print("Q-Learning")
    print("Dictionary size: ", len(Q))
    print("Please wait. pac-man is learning")

    for epoch in range(1, epoch_count+1):
        env.initialize()
        s = env.getState()
        total_reward = 0
        while env.terminal() == False:
            a = env.policy(s, pacman_actions)
            env.update(s, a)
            reward_got = env.getReward()

            # randomly initialize food pallets again
            if env.food_pellet_count == 0:
                env.food_pellet_count = random.randint(1, food_pellet_count)

                locations = total_locations.copy()
                locations.remove(env.pacman)
                random.shuffle(locations)
                for f in range(env.food_pellet_count):
                    env.food_pellet_loc.append(locations.pop())

            s_prime = env.getState()

            (r, c) = s_prime[0]
            if outOfBound(size, r, c) or (s_prime[0] == s_prime[1]) or ((s[0], s[1]) == (s_prime[1], s_prime[0])):
                updateQ(s, a, reward_got, s_prime)
                break
            else:  # check if ghost is outofbound, if yes then set it to (-1,-1)
                (r, c) = s_prime[1]
                if outOfBound(size, r, c):  # setting ghost location to (-1,-1)
                    s_prime = list(s_prime)
                    s_prime[1] = (-1, -1)
                    s_prime = tuple(s_prime)
                a_prime = env.getOptimalAction(s_prime)
                updateQ(s, a, reward_got, s_prime, a_prime)
                total_reward += reward_got

            s = s_prime

        avg_score_list.pop(0)
        avg_score_list.append(total_reward)
        if epoch % (epoch_count/100) == 0:
            avg_score = sum(avg_score_list)/len(avg_score_list)
            print(avg_score)
            score_list.append(avg_score)

    fig = plt.figure()
    plt.plot(score_list)
    fig.suptitle('Q-Learning')
    plt.xlabel('epoch x 100')
    plt.ylabel('score')
    # fig.savefig('score.png')
    # plt.ylim(-2,10)
    plt.show()

def sarsa():

    score_list = []
    avg_score_list = [0]*100
    generateQ(size)
    env = Environment(size, food_pellet_count)
    print("Welcome to the game of pacman!")
    print("SARSA")
    print("Dictionary size: ", len(Q))
    print("Please wait. pac-man is learning")

    for epoch in range(1, epoch_count+1):
        env.initialize()
        s = env.getState()
        total_reward = 0
        a = env.policy(s, pacman_actions)
        while env.terminal() == False:
            env.update(s, a)
            reward_got = env.getReward()

            if env.food_pellet_count == 0:  # mostly should move it up
                env.food_pellet_count = random.randint(1, food_pellet_count)

                locations = total_locations.copy()
                locations.remove(env.pacman)
                random.shuffle(locations)
                for f in range(env.food_pellet_count):
                    env.food_pellet_loc.append(locations.pop())  # HERE

            s_prime = env.getState()

            (r, c) = s_prime[0]
            if outOfBound(size, r, c) or (s_prime[0] == s_prime[1]) or ((s[0], s[1]) == (s_prime[1], s_prime[0])):
                updateQ(s, a, reward_got, s_prime)
                break
            else:  # check if ghost is outofbound, if yes then set it to (-1,-1)
                (r, c) = s_prime[1]
                if outOfBound(size, r, c):  # setting ghost location to (-1,-1)
                    s_prime = list(s_prime)
                    s_prime[1] = (-1, -1)
                    s_prime = tuple(s_prime)
                a_prime = env.policy(s_prime,pacman_actions)
                updateQ(s, a, reward_got, s_prime, a_prime)
                total_reward += reward_got

            s = s_prime
            a = a_prime


        avg_score_list.pop(0)
        avg_score_list.append(total_reward)
        if epoch % (epoch_count/100) == 0:
            avg_score = sum(avg_score_list)/len(avg_score_list)
            print(avg_score)
            score_list.append(avg_score)

    fig = plt.figure()
    plt.plot(score_list)
    fig.suptitle('SARSA')
    plt.xlabel('epoch x 100')
    plt.ylabel('score')
    # fig.savefig('score.png')
    # plt.ylim(-2,10)
    plt.show()

# qLearning()
sarsa()
