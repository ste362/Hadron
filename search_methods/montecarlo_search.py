import random
import time

import numpy as np

MAX_TIME = 1.9
MAX_ITER = 100000


def monte_carlo_tree_search_base(game, state, N=500):
    # print("N:",N)
    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        """expand the leaf node by adding all its children states"""
        if not n.children and not game.is_terminal(n.state):
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                          for action in game.actions(n.state)}
        return select(n)

    def simulate(game, state):
        """simulate the utility of current state by random picking a step"""
        player = state.to_move
        while not game.is_terminal(state):
            action = random.choice(list(game.actions(state)))
            state = game.result(state, action)
        v = game.utility(state, player)
        return -v

    def backprop(n, utility):
        """passing the utility back to all parent nodes"""

        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)

        """
        node=n
        node_utility=utility
        while True:
            if utility > 0:
                node.U+=utility
            node_utility=-node_utility
            node=node.parent
            node.N+=1
            if(node):
                break
        """

    root = MCT_Node(state=state)

    start = time.time()
    count = 0
    while ((time.time() - start) < MAX_TIME and count < MAX_ITER):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backprop(child, result)
        count += 1
    print("Ricorsivo: ",count)

    max_state = max(root.children, key=lambda p: p.N)

    return 0, root.children.get(max_state)



def monte_carlo_tree_search(game, state, N=500):

    #print("N:",N)
    def select(n):
        """select a leaf node in the tree"""
        while(True):
            if n.children:
                n=max(n.children.keys(), key=ucb)
            else:
                break
        return n
        """
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n
        """

    def expand(n):
        """expand the leaf node by adding all its children states"""
        if not n.children and not game.is_terminal(n.state):
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                          for action in game.actions(n.state)}
        return select(n)

    def simulate(game, state):
        """simulate the utility of current state by random picking a step"""
        player = state.to_move
        while not game.is_terminal(state):
            action = random.choice(list(game.actions(state)))
            state = game.result(state, action)
        v = game.utility(state, player)
        return -v

    def backprop(n, utility):
        """passing the utility back to all parent nodes"""

        """
        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)
            
        """
        node=n
        node_utility=utility
        while True:
            if utility >0:
                node.U+=node_utility
            node.N+=1
            if not node.parent:
                break
            node=node.parent
            node_utility=-node_utility


    root = MCT_Node(state=state)

    start = time.time()
    count = 0
    while((time.time()-start)<MAX_TIME and count<MAX_ITER):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backprop(child, result)
        count += 1
    print("iterativo: ",count)

    max_state = max(root.children, key=lambda p: p.N)

    return 0,root.children.get(max_state)



# Monte Carlo tree node and ucb function


class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None


def ucb(n, C=1.4):
    const=n.N
    return np.inf if const == 0 else n.U / const + C * np.sqrt(np.log(n.parent.N) / const)
