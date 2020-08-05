# programme pour pas spawn les snake et leur manger a l'endoit ou ils sont
import random


##x=40
##y=40
##Grid_size=(x,y)
##No_spawn_positions = [(15,15),(0,0),(33,33),(11,11),(2,2),(2, 39), (3, 39), (4, 39), (5, 39), (6, 39), (7, 39), (8, 39)]
##def Get_spawn_location(Grid_size,No_spawn_positions):
##    Grid_position_list=[]
##    #mettre chaque position possible dans une liste
##    for position_y in range(Grid_size[1]):
##        for position_x in range(Grid_size[0]):
##            Grid_position_list.append((position_x,position_y))
##    #mettre les postions des snakes et du manger dans une liste
##
##    #retirer les postions du snake et des manger dans la liste
##    Grid_position_list = [ele for ele in Grid_position_list if ele not in No_spawn_positions]
##    #chosir un spawn_location
##    Spawn_location=random.choice(Grid_position_list)
##    return Spawn_location


def Get_spawn_location(Grid_position_list, No_spawn_positions):
    ##    Grid_position_list=[]
    ##    #mettre chaque position possible dans une liste
    ##    for position_y in range(Grid_size[1]):
    ##        for position_x in range(Grid_size[0]):
    ##            Grid_position_list.append((position_x,position_y))
    Filtred_list = list(filter(lambda i: i not in No_spawn_positions, Grid_position_list))
    return random.choice(Filtred_list)


# print('Une position valable de spawn pr un snake ou un manger est ',Get_spawn_location(Grid_size,No_spawn_positions))
##### testing
testing = False
if testing:
    for loop in range(10000):
        x = Get_spawn_location(Grid_size, No_spawn_positions)
        if x in No_spawn_positions:
            print('it fcked up')
