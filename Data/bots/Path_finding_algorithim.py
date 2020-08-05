from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

matrix=[]
# matrix.append([ 1 , 1 , 1 , 1 , 1 , 1 , 1 ])
# matrix.append([ 1 , 1 , 0 , 1 , 1 , 1 , 1 ])
# matrix.append([ 1 , 1 , 0 , 1 , 1 , 1 , 1 ])
# matrix.append([ 1 , 1 , 1 , 1 , 1 , 1 , 1 ])
# matrix.append([ 1 , 1 , 1 , 1 , 1 , 1 , 1 ])
# matrix.append([ 1 , 1 , 1 , 1 , 1 , 1 , 1 ])
# matrix.append([ 1 , 1 , 0 , 1 , 1 , 1 , 1 ])
# print(matrix)
# print(Grid)
Clear_Grid=[]
Grid_factor=4
Grid_size=[int(16*Grid_factor),int(9*Grid_factor)]
for loop in range(Grid_size[1]):
	Clear_Grid.append([ 1 ]*Grid_size[0])
for loop in Clear_Grid:
	print(loop)

def find_path_to_snack(Snake_bodies,Start_pos,Snack_pos):
	Clear_Grid=[]
	Grid_factor=4
	Grid_size=[int(16*Grid_factor),int(9*Grid_factor)]
	for loop in range(Grid_size[1]):
		Clear_Grid.append([ 1 ]*Grid_size[0])

	for position in Snake_bodies:
		#print(position)
		#print(Clear_Grid[position[1]])
		# if position[0]==Grid_size[0] and position[1]<Grid_size[1]:
		# 	position=(63,position[1])
		try:
			Clear_Grid[position[1]][position[0]]=0
		except:
			print('Error snake off grid')
			pass
	grid = Grid(matrix=Clear_Grid)

	start = grid.node(Start_pos[0], Start_pos[1])
	end = grid.node(Snack_pos[0], Snack_pos[1])

	finder = AStarFinder()
	path, runs = finder.find_path(start, end, grid)
	#print(path)
	#print(grid.grid_str(path=path, start=start, end=end))
	#print('found path')
	return path

#print(find_path_to_snack(Clear_Grid,[(25,22),(12,20)],(2,0),(10,30)))
#find_path_to_snack(
#print(find_path_to_snack([(25, 2), (2, 33), (1, 33), (0, 33), (63, 33)], (3, 33) ,(60, 7)))