from search_methods.alphabeta_search import h_alphabeta_search1, h_alphabeta_search, alphabeta_search
from search_methods.montecarlo_search import monte_carlo_tree_search


def montecarlo_alphabeta_search(game,state):
    if(len(game.actions(state))>7):
        return monte_carlo_tree_search(game,state,800)
    return h_alphabeta_search(game,state)