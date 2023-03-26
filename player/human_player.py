import random

def human_player(game, state):
    print("Are available this tile: "+str(list(game.actions(state))))
    data=input("Insert tuple <column,row>: ").split(",")
    tuple=int(data[0]),int(data[1])
    return tuple