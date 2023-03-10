first_player = 1 #player first
#player = 1
#bot = -1
memory = {
	'[[0, 0, 1], [0, 0, 0], [0, 0, 0]]':[[0,0,1],[0,-1,0],[0,0,0]],
	'[[0, 0, 0], [0, 0, 0], [1, 0, 0]]':[[0,0,0],[0,-1,0],[1,0,0]],
	'[[0, 0, 0], [0, 0, 0], [0, 0, 1]]':[[0,0,0],[0,-1,0],[0,0,1]]
}
def flatten(board):
	return board[0]+board[1]+board[2]
def unflatten(flatten_board):
	return [flatten_board[0:3],flatten_board[3:6],flatten_board[6:10]]
#def result(of player)? -> -1, 0, 1 or None
def result(board):
	# for row if sum=3 return 1 else if sum=-3 return -1
	for i in range(3):
		if abs(board[i][0]+ board[i][1]+ board[i][2])==3 :
			return (board[i][0]+ board[i][1]+ board[i][2])//3
	# for column if sum=3 return 1 else if sum=-3 return -1
	for i in range(3):
		if abs(board[0][i]+ board[1][i]+ board[2][i])==3:
			return (board[0][i]+ board[1][i]+ board[2][i])//3
	# for corner if sum=3 return 1 else if sum=-3 return -1
	if abs(board[0][0]+ board[1][1]+ board[2][2])==3:
		return (board[0][0]+ board[1][1]+ board[2][2])//3
	if  abs(board[0][2]+ board[1][1]+ board[2][0])==3:
		return (board[0][2]+ board[1][1]+ board[2][0])//3
	# is draw?
	for i in board:
		if 0 in i:
			return None
	return 0
def add_piece(board,place,piece):
	return unflatten(flatten(board)[:place]+[piece]+flatten(board)[place+1:])
#def getcombination
def get_combination(board):
	global first_player
	# next move == X or O 
	next_player = first_player if sum([sum(i) for i in board])==0 else first_player*(-1)
	# return for every move combination
	combinations = []
	for i in range(9):
		if flatten(board)[i]==0:
			combinations.append(add_piece(board,i,next_player))
	return combinations
#def result collect (recursive)
def collect_result(board):
	global first_player
	if result(board)!= None :
		match result(board):
			case 1:
				return (20,1)
			case 0:
				return (-1,1)
			case -1:
				return (-2,1)
	total = 0
	length = 0
	next_player = first_player if sum([sum(i) for i in board])==0 else first_player*(-1)
	for i in get_combination(board if next_player==1 else move(board)):
		next_combination = collect_result(i)
		total += next_combination[0]
		length += next_combination[1]
	if length==0:
		length = 1
	return (total,length)	
def win_rate(board):
	return collect_result(board)[0]/collect_result(board)[1]
#def get win probability
def move(board):
	if str(board) in memory:
		return memory[str(board)]
	# 1 collect result 
	combinations = get_combination(board)
	combinations.sort(key=win_rate)
	memory[str(board)] = combinations[0]
	return combinations[0]
def transform(n,default):
	match n :
		case 1:
			return "O"
		case -1:
			return "X"
	return f"{default}"
def display(board):
	print(
		f""" {transform(board[0][0],1)} | {transform(board[0][1],2)} | {transform(board[0][2],3)} 
---+---+---
 {transform(board[1][0],4)} | {transform(board[1][1],5)} | {transform(board[1][2],6)} 
---+---+---
 {transform(board[2][0],7)} | {transform(board[2][1],8)} | {transform(board[2][2],9)} """)
#header
print("+-----------------+\n| TIC TAC TOE bot |\n+-----------------+\n")
print("Your piece is O .\n")

current_player = 1
# #while loop(new game)
while True:
	board = [[0,0,0],[0,0,0],[0,0,0]]
	while result(board)==None:
		if current_player==-1:
			board = move(board)
		else:
			display(board)
			player_move = int(input())
			while player_move>9 or flatten(board)[player_move-1]!=0 :
				player_move = int(input())
			board = add_piece(board,player_move-1,1)
		
		current_player *= -1
	
	match result(board):
		case 1 :
			print("you won")
		case -1 :
			display(board)
			print("you lose")
		case 0 :
			print("draw")
	first_player *= -1 #alternate first player
	current_player = first_player