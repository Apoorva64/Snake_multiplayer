#PATH Finding Client
import queue
Grid=[]
Grid.append([" "," ", " ", " ", " ", " "," "])
Grid.append([" "," ", " ", " ", " ", " "," "])
Grid.append([" ","#", "#", "#", "#", "#"," "])
Grid.append([" "," ", " ", " ", " ", " "," "])
Grid.append([" "," ", " ", " ", " ", " "," "])
Grid.append([" "," ", " ", " ", " ", " "," "])
Grid.append([" "," ", " ", " ", " ", " ","O"])
def print_grid(Grid):
	for Layer in Grid:
		print(Layer)
Start_pos=(0,0)
def valid(Start_pos,Grid, moves):
    # for x, pos in enumerate(Grid[0]):
    #     if pos == "O":
    #         start = x

    x = Start_pos[0]
    y = Start_pos[1]
    #Grid[y][x]='+'
    for move in moves:
        if move == "L":
            x -= 1

        elif move == "R":
            x += 1

        elif move == "U":
            y -= 1

        elif move == "D":
            y += 1

        if not(0 <= x < len(Grid[0]) and 0 <= y < len(Grid)):
            return False
        elif (Grid[y][x] == "#"):
            return False
        #Grid[y][x]='+'
    #print_grid(Grid)
    return True
def Check_if_end(Start_pos,Grid, moves):
    x = Start_pos[0]
    y = Start_pos[1]
    #Grid[y][x]='+'
    for move in moves:
        if move == "L":
            x -= 1

        elif move == "R":
            x += 1

        elif move == "U":
            y -= 1

        elif move == "D":
            y += 1
    if Grid[y][x] == "O":
    	print('Found Path')
    	return True

nums = queue.Queue()
nums.put("")
add = ""

while not Check_if_end(Start_pos,Grid, add): 
    add = nums.get()
    #print(add)
    for j in ["L", "R", "U", "D"]:
        put = add + j
        if valid(Start_pos,Grid, put):
            nums.put(put)
print(valid(Start_pos,Grid,'DDDDRRRRR'))