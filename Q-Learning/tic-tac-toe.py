import random

# Computer(Q-agent) always plays 'X' and Player plays 'O'

def drawBoard(board):
    # This function prints out the board that it was passed.
    # "board" is a list of 10 strings representing the board (ignore index 0)
    #print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    #print('   |   |')
    print('-----------')
    #print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    #print('   |   |')
    print('-----------')
    #print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    #print('   |   |')

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def getBoardCopy(board):
# Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []
    for i in board:
        dupeBoard.append(i)
    return dupeBoard

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def makeMove(board, letter, move):
    if move is not None:
        board[move] = letter

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

def isWinner(bo, le):
    # Given a board and a player’s letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don’t have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []

    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getPlayerMove(board):
    # First, check if Player can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    # Check if the Q-agent could win on its next move, and block them.
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    # Move on one of the sides.
    possibleActions = getPossibleActions(board)
    return chooseRandomMoveFromList(board, possibleActions)

def generateStates():
    states = {tuple([' '] * 10)}

    for i in range(1,4):
        for j in range(1,4):
            temp_states = states.copy()
            states.clear()
            for s in temp_states:
                s = list(s)
                for c in (" ","X","O"):
                    s[(i-1)*3 + j] = c
                    states.add(tuple(s))

    return states

def generateQ(states):
    states = list(states)
    Q = {}

    for s in states:
        actions = getPossibleActions(s)
        for a in actions:
            q_list = [s,a]
            Q[tuple(q_list)] = 0.0


    return Q

def getPossibleActions(board):
    possibleMoves = []
    movesList = [x for x in range(1,10)]

    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    return possibleMoves


def qLearning(train_type,test_type):

    print("train type: {}, test type: {}".format(train_type,test_type))

    # Computer always plays X and human plays O

    Q = generateQ(states)

    for epsiode in range(1,10001):

        tie = 0
        win = 0
        lose = 0

        if epsiode == 10000:            # final test
            epslon = 0
            testitr = 1000
        elif epsiode%200 == 0:          # test
            epslon = 0
            testitr = 100
        else:                           # train
            epslon = epslon_init
            testitr = 1

        for titr in range(testitr):

            # if train, iterate only once, if test, iterate 100 times for each epsiode
            s = [' '] * 10
            s_prime = [' '] * 10
            r = 0  # reward is always 0
            a = 0
            a_prime = 0
            turn = whoGoesFirst()
            # print('The ' + turn + ' will go first.')
            isGameOn = True

            while isGameOn:
                if turn == 'computer':  # our QLearning agent
                    actions = getPossibleActions(s)  # all possible actions

                    if random.random() > epslon:  # greedy action
                        maximum = -1000.0
                        for act in actions:
                            if Q[tuple([tuple(s), act])] > maximum:
                                maximum = Q[tuple([tuple(s), act])]
                                a = act
                    else:  # random action
                        a = chooseRandomMoveFromList(s, actions)

                    s_prime = getBoardCopy(s)
                    makeMove(s_prime, "X", a)  # move-1
                    # print("Computer move")
                    # drawBoard(s_prime)

                    if isWinner(s_prime, "X"):
                        #drawBoard(s_prime)
                        #print('The computer has beaten you! You lose.')
                        Q[tuple([tuple(s), a])] = \
                            Q[tuple([tuple(s), a])] + alpha * (10 - Q[tuple([tuple(s), a])])
                        win += 1
                        isGameOn = False
                    else:
                        if isBoardFull(s_prime):
                            #drawBoard(s_prime)
                            #print('The game is a tie!')
                            tie += 1
                            break
                        else:
                            turn = 'player'
                else:

                    if epslon == 0:                     # test
                        if test_type == "random":
                            m = chooseRandomMoveFromList(s_prime, getPossibleActions(s_prime))
                        else:
                            m = getPlayerMove(s_prime)
                    else:                               # train
                        if train_type == "random":
                            m = chooseRandomMoveFromList(s_prime, getPossibleActions(s_prime))
                        elif train_type == "safe":
                            m = getPlayerMove(s_prime)
                        else:
                            if random.random() < 0.5:
                                m = chooseRandomMoveFromList(s_prime, getPossibleActions(s_prime))
                            else:
                                m = getPlayerMove(s_prime)

                    makeMove(s_prime, "O", m)  # move-2
                    # print("Player move")
                    # drawBoard(s_prime)
                    # s_prime is generated here

                    if isWinner(s_prime, "O"):
                        #drawBoard(s_prime)
                        #print('Hooray! You have won the game!')
                        Q[tuple([tuple(s), a])] = \
                            Q[tuple([tuple(s), a])] + alpha * (-10 - Q[tuple([tuple(s), a])])
                        lose += 1
                        isGameOn = False
                    else:
                        if isBoardFull(s_prime):
                            #drawBoard(s_prime)
                            #print('The game is a tie!')
                            tie += 1
                            break
                        else:
                            turn = 'computer'

                    if a != 0 and isGameOn:
                        actions_prime = getPossibleActions(s_prime)  # max over a_prime Q(s_prime,a_prime)
                        maximum_prime = -1000.0
                        for act_prime in actions_prime:
                            if Q[tuple([tuple(s_prime), act_prime])] > maximum_prime:
                                maximum_prime = Q[tuple([tuple(s_prime), act_prime])]
                                a_prime = act_prime  # a_prime is generated here

                        Q[tuple([tuple(s), a])] = \
                            Q[tuple([tuple(s), a])] + alpha * (0 + gamma * Q[tuple([tuple(s_prime), a_prime])] - Q[tuple([tuple(s), a])])

                    s = getBoardCopy(s_prime)

        if epsiode%200 == 0:
        # if epsiode == 10000:
            print("****************************")
            print("test epoch: ", epsiode/200)
            print("win: ",win)
            print("tie: ",tie)
            print("lose: ",lose)
            print("****************************")

print('Welcome to Tic Tac Toe!')

playerLetter, computerLetter = ['O', 'X']
epslon_init = 0.2
alpha = 0.9
gamma = 0.5

states = generateStates()

qLearning("random","random")
qLearning("random","safe")
qLearning("safe","random")
qLearning("safe","safe")
qLearning("both","random")
qLearning("both","safe")

