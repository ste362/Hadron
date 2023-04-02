import random

def human_player(game, state):
    while(True):
        moves=list((x,y) for (y,x) in list(game.actions(state)))
        print("Are available this tile: ",moves)
        data=input("Insert tuple <row,column>: ").split(",")
        tuple=int(data[1]),int(data[0])
        if(tuple in set(game.actions(state))):
            break

    return tuple