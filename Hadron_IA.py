from collections import namedtuple, Counter, defaultdict
import random
import math
import functools

from player.human_player import human_player
from player.random_player import random_player
from search_methods.alphabeta_search import h_alphabeta_search, alphabeta_search, h_alphabeta_search1, \
    h_alphabeta_search_base
from search_methods.montecarlo_aphabeta_search import montecarlo_alphabeta_search
from search_methods.montecarlo_search import monte_carlo_tree_search, monte_carlo_tree_search_base


class Game:
    """A game is similar to a problem, but it has a terminal test instead of
    a goal test, and a utility for each terminal state. To create a game,
    subclass this class and implement `actions`, `result`, `is_terminal`,
    and `utility`. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError


def play_game(game, strategies: dict, verbose=False):
    """Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move."""
    state = game.initial  #è un campo di game è inizializzato in Hadron ed è una instanza di Board
    count=0
    while not game.is_terminal(state):
        startTime=time.time()
        player = state.to_move
        move = strategies[player](game, state)
        state = game.result(state, move)
        count+=1
        if verbose:
            print('Player', player, 'move:', move)
            print(state)
            print("Tempo mossa:",time.time()-startTime)
    #print(player,"  mosse ",count)
    return state,player



infinity = math.inf




def isAllowable(t, board, setBoard):
    (x,y) = t
    redCounter=0
    blueCounter=0

    if ((x-1,y) in setBoard):
        if(board[x-1, y] == 'R'):
            redCounter+=1
        else:
            blueCounter+=1

    if ((x+1,y) in setBoard):
        if(board[x+1, y] == 'R'):
            redCounter+=1
        else:
            blueCounter+=1

    if ((x,y-1) in setBoard):
        if(board[x, y-1] == 'R'):
            redCounter+=1
        else:
            blueCounter+=1

    if ((x,y+1) in setBoard):
        if(board[x, y+1] == 'R'):
            redCounter+=1
        else:
            blueCounter+=1

    #print("red "+str(redCounter)+ " blue "+str(blueCounter) + " pos "+str((x,y)))
    return redCounter==blueCounter


class Hadron(Game):
    """Play TicTacToe on an `height` by `width` board, needing `k` in a row to win.
    'X' plays first against 'O'."""

    def __init__(self, height=3, width=3, k=3):
        self.k = k # k in a row
        self.squares = {(x, y) for x in range(width) for y in range(height)}
        self.initial = Board(height=height, width=width, to_move=START, utility=0)

    def actions(self, board):
        """Legal moves are ...."""
        setBoard=set(board)
        return {(x, y) for (x, y) in self.squares - setBoard
                if isAllowable( (x,y), board, setBoard ) }

    def result(self, board, square):
        """Place a marker for current player on square."""
        player = board.to_move
        board = board.new({square: player}, to_move=('B' if player == 'R' else 'R'))
        win = len(self.actions(board))==0
        board.utility = (0 if not win else +1000000 if player == 'R' else -1000000)
        return board

    def utility(self, board, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return board.utility if player == 'R' else -board.utility

    def is_terminal(self, board):
        """A board is a terminal state if it is won or there are no empty squares."""
        return board.utility != 0

    def display(self, board): print(board)



class Board(defaultdict):
    """A board has the player to move, a cached utility value,
    and a dict of {(x, y): player} entries, where player is 'R' or 'B'."""
    empty = '.'
    off = '#'

    def __init__(self, width=8, height=8, to_move=None, **kwds):
        self.__dict__.update(width=width, height=height, to_move=to_move, **kwds)

    def new(self, changes: dict, **kwds) -> 'Board':
        "Given a dict of {(x, y): contents} changes, return a new Board with the changes."
        board = Board(width=self.width, height=self.height, **kwds)
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off

    def __hash__(self):
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)

    def __repr__(self):
        def row(y): return str(y)+"  "+' '.join(self[x, y] for x in range(self.width))


        return "   "+" ".join(str(y) for y in range(self.height))+"\n"+"\n".join(map(row, range(self.height))) + '\n'



def player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    return lambda game, state: search_algorithm(game, state)[1]



#####################################################################################################################################################################



import time
start= time.time()

START='R'
size=9
r=0
N=20
for _ in range(0,N):
    start= time.time()
    win=play_game(Hadron(width=size,height=size), dict(R=player(monte_carlo_tree_search), B=player(monte_carlo_tree_search_base)), verbose=False)[1]
    if win == 'R':
        r+=1
    print(win,end="")
print("Time: ",time.time()-start)

print("\nRed ", r)
print("Blue",N-r)
"""
print("#####################")
r=0
for _ in range(0,N):
    win=play_game(Hadron(width=size,height=size), dict(R=player(h_alphabeta_search1), B=player(montecarlo_alphabeta_search)), verbose=False)[1]
    if win == 'R':
        r+=1
print("Red ", r)
print("Blue",N-r)

"""

#play_game(Hadron(width=4,height=4), dict(R=player(alphabeta_search), B=player(alphabeta_search)), verbose=True).utility


#print("Time "+str(time.time()-start))
#play_game(Hadron(width=4,height=4), dict(R=player(alphabeta_search), B=player(minimax_search)), verbose=True).utility

#per giocare nella 7*7 inizia il blu
#play_game(Hadron(width=size,height=size), dict(R=player(montecarlo_alphabeta_search), B=human_player), verbose=True)






#play_game(Hadron(width=4,height=4), {'R':player(alphabeta_search_tt), 'B':random_player},verbose=True)

#play_game(Hadron(), {'X':player(alphabeta_search), 'O':player(minimax_search)})





#play_game(Hadron(), {'X':player(h_alphabeta_search), 'O':player(h_alphabeta_search)})


#for _ in range(0,20):
#    play_game(Hadron(width=size,height=size), dict(R=player(monte_carlo_tree_search), B=player(h_alphabeta_search1)),verbose=False).utility

class CountCalls:
    """Delegate all attribute gets to the object, and count them in ._counts"""
    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()

    def __getattr__(self, attr):
        "Delegate to the original object, after incrementing a counter."
        self._counts[attr] += 1
        return getattr(self._object, attr)

def report(game, searchers):
    for searcher in searchers:
        game = CountCalls(game)
        searcher(game, game.initial)
        print('Result states: {:7,d}; Terminal tests: {:7,d}; for {}'.format(
            game._counts['result'], game._counts['is_terminal'], searcher.__name__))

#report(Hadron(height=6,width=6), (h_alphabeta_search,h_alphabeta_search1,montecarlo_alphabeta_search))