#test= 'apoorva,"|56>5|1>0|0>255>255 ochinhcin,"|56>5|1>0|0>255>255 ochinhcinwqe,"|56>5|1>0|0>255>255??|56>5|1>0|0>255>255 |56>5|1>0|0>255>255'
def list_cleaner(L):
    without_empty_strings = []
    for string in L:
        if (string != ""):
            without_empty_strings.append(string)
    return without_empty_strings


#print(without_empty_strings)
def decode(recived_data):
    Sounds_to_play_decoded=[]
    recived_data=recived_data.split('??')
    snack_data=recived_data[1]
    snake_data=recived_data[0]
    additionnal_data=recived_data[2]
    Sounds_to_play=recived_data[3].split('=')
    for sound in Sounds_to_play:
        if sound!='':
            Sounds_to_play_decoded.append(tuple(sound.split('*')))

    snacks=snack_data.split(' ')
    #print(snacks)
    snakes=snake_data.split(' ')
    #print(snakes)
    snake_list=[]
    snack_list=[]
    for snake in snakes:
        if snake!='':
            #print(snake)
            x=snake.split(',')
            snake_name=x[0]
            snake_data=x[1].split('"')
            snake_lives=x[2]
            cubes=[]
            #print(snake)
            #print(snake_data)
            for cube in snake_data:
                if cube!='':
                    cube_data=cube.split('|')
                    cube_data=list_cleaner(cube_data)
                    #print('Cube',cube_data)
                    cube_position=cube_data[0].split('>')
                    #print('position',cube_position)
                    cube_position = list(map(int, cube_position))
                    cube_orientation=cube_data[1].split('>')
                    cube_orientation = list(map(int, cube_orientation))
                    cube_color=cube_data[2].split('>')
                    cube_color = list(map(int, cube_color))
                    cubes.append([cube_position,cube_orientation,cube_color])
            snake_list.append([snake_name,cubes,snake_lives])
    for snack in snacks:
        if snack!='':
            snack_data=snack.split('|')
            snack_data=list_cleaner(snack_data)
            #print('snack',snack_data)
            snack_position=snack_data[0].split('>')
            #print('position',snack_position)
            snack_position = list(map(int, snack_position))
            snack_orientation=snack_data[1].split('>')
            snack_orientation = list(map(int, snack_orientation))
            snack_color=snack_data[2].split('>')
            snack_color = list(map(int, snack_color))
            snack_list.append([snack_position,snack_orientation,snack_color])
    #print('snack_list',snack_list)
    return snake_list,snack_list,additionnal_data,Sounds_to_play_decoded
##snake_list,snack_list=decode(test)
##print(snake_list)
##print(snack_list)
