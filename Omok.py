#IMPORTANT COMMENT AT THE END OF THE LINE
#Please make sure you type in python3 -i FinalProjectDone.py We need to have the Turtle Graphics window open the whole time.


import turtle
t = turtle.Turtle()
n = 420
in_progress = True

#board allows the computer to see the go-board. I assined 0 to all the empty spots. Once a stone is placed in an empty slot, the slot value changes to a different value depending on the color of the stone.


board = {(x , y):0 for x in range(-1,16) for y in range(-1,16)} #I created a dictionary instead of a list. The range of x and y were set to -1 and 16 to give me "invisible" buffer area. This extra slots made it easier for me to check winning conditions on the boundaries of the board.
black_stone = 1
white_stone = 2
player = "black"

#The add_stone function "adds" stones to the virtual board so that the computer can see. It also checks if a slot is already occupied or not. If it is occupied, then it asks for different x and y inputs
def add_stone(player, x, y): 
	if board[(x,y)] == black_stone:
		print("That spot already has a black stone. Pick again.")
		x = eval(input("{0}, choose your x - coordinate.".format(player)))
		y = eval(input("{0}, choose your y - coordinate.".format(player)))
		add_stone(player,x,y)
	elif board[(x,y)] == white_stone:
		print("That spot already has a white stone. Pick again")
		x = eval(input("{0}, choose your x - coordinate.".format(player)))
		y = eval(input("{0}, choose your y - coordinate.".format(player)))
		add_stone(player,x,y)
	else:
		if player == "black":
			board[(x,y)] = black_stone
		elif player == "white":
			board[(x,y)] = white_stone

# drawboard(n) uses turtle function to draw a physical board.
def drawboard(n):
	t.up()
	t.goto((- n / 2),(n / 2))
	t.seth(270)
	t.down()
	for _ in range (7):
		t.forward(n)
		t.up()
		t.left(90)
		t.forward(n / 14)
		t.down()
		t.left(90)
		t.forward(n)
		t.right(90)
		t.up()
		t.forward(n / 14)
		t.right(90)
		t.down()
	t.forward(n)
	t.up()
	t.left(90)
	t.goto((- n / 2),(- n / 2))	
	t.down()
	for _ in range (7):
		t.forward(n)
		t.up()
		t.left(90)
		t.forward(n / 14)
		t.down()
		t.left(90)
		t.forward(n)
		t.right(90)
		t.up()
		t.forward(n / 14)
		t.right(90)
		t.down()
	t.forward(n)
	t.goto((- n / 2),(n / 2))
	t.up()
	t.seth(0)
	for i in range (15):
		t.write(str(i))
		t.forward(n / 14)
	t.up()
	t.goto((- n / 2) - 10,(n / 2) - 5)
	t.right(90)
	for i in range (15):
		t.write(str(i))
		t.forward(n / 14)
	
# Since the board coordinates are different from actual x-y plane, go_stone_placer converts x and y inputs from a player to "actual" x and y values in the x-y plane.
# After the conversion, go_stone_placer then places a stone on the board.

def go_stone_placer(player, x,y):
	t.goto(0,0)
	t.seth(270)
	#Converting coordinates into conventional x-y plane coordinates
	if x < 7:
		x = (7 - x) * (- n / 14)
	elif x > 7:
		x = (x - 7) * (n / 14)
	if x == 7:
		x = 0
	if y < 7:
		y = (7 - y) * (n / 14)
	elif y > 7:
		y = (y - 7) * (- n / 14)
	if y == 7:
		y = 0
	#placing a stone
	t.goto((x - 15),y)
	t.down()
	if player == "white":
		#Changing color to white
		t.color("white")
		t.begin_fill()
		t.circle(15)
		t.end_fill()
		t.color("black")	
		t.circle(15)	
	elif player == "black":
		t.color("black")		
		t.begin_fill()
		t.circle(15)
		t.end_fill()
	t.up()



def move_converter_x_to_n(x):
	if x < 7:
		x = (7 - x) * (- n / 14)
	elif x > 7:
		x = (x - 7) * (n / 14)
	if x == 7:
		x = 0
	return x

def move_converter_y_to_n(y):
	if y < 7:
		y = (7 - y) * (n / 14)
	elif y > 7:
		y = (y - 7) * (- n / 14)
	if y == 7:
		y = 0
	return y


#I divided the winning condition into four parts. Horizontal, vertical, diagonal with a slope of 1 and another digonal with a slope of -1
def horizontal_win(player,move):
	if player == "black":
		player = 1
	elif player == "white":
		player = 2
#I defined two helper functions within the horizonta_win function. These two functions allow me to change my current position to left and right very easily.
	def one_left_current_move(move):
		return (move[0] - 1, move[1])
	def one_right_current_move(move):
		return (move[0] + 1, move[1])
	
	current_position = move

#First, horizontal_win checks if there are stones horizontally next to the most recent move. If both spots are empty then there is no possibility of winnning. So returns false.
	if board[one_left_current_move(current_position)] != player and board[one_right_current_move(current_position)] != player:
		return False

#Checks if the most recent move is on the left most boundary. If it is on the boundary, it starts counting to the right to see if there are 4 more stones with same color next to it.
	if move_converter_x_to_n(move[0]) == (- n / 2):
		counter = 0
		while board[current_position] == player:
			current_position = one_right_current_move(current_position)
			counter += 1
		if counter == 5:
			return True

#Chekcs if the most recent move in on right most boundary. If it is on the boundary, it starts counting to the left to see if there are 4 more stones with same color next to it	
	if move_converter_x_to_n(move[0]) == (n / 2):
		counter = 0 
		while board[current_position] == player:
			current_position = one_left_current_move(current_position)
			counter += 1
		if counter == 5:
			return True

#if the recenot move is not on the boundaries, then it sets the most recent move to the left stone. Checks if the stone is the same color or not. Then changes the most recent move to the left stone again.
#This process continues untill the left most stone either doesn't exist or is in different color. Then we start counting to the right. If there are five stones, returns true. Else, returns false.
	while board[current_position] == player:
		current_position = one_left_current_move(current_position)
		if move_converter_x_to_n(current_position[0]) == (- n / 2):
			counter = 0
			while board[current_position] == player:
				current_position = one_right_current_move(current_position)
				counter += 1
			if counter == 5:
				return True

	current_position = one_right_current_move(current_position)
	counter = 0
	while board[current_position] == player:
		counter += 1
		current_position = one_right_current_move(current_position)

	if counter == 5:
		return True
		
	return False


#Vertical_win is similar to how horizontal_win works. We first work our way downard, then start counting how many same colored stones appear in a row. If there are five stones consecutively, then it returns true.
#if not, it returns false.

def vertical_win(player, move):
	if player == "black":
		player = 1
	elif player == "white":
		player = 2

	def one_above_current_move(move):
		return (move[0], move[1] - 1)
	def one_below_current_move(move):
		return (move[0], move[1] + 1)

	current_position = move

	if board[one_above_current_move(current_position)] != player and board[one_below_current_move(current_position)] != player:
		return False

	if move_converter_y_to_n(move[1]) == (n / 2):
		counter = 0
		while board[current_position] == player:
			current_position = one_below_current_move(current_position)
			counter += 1
		if counter == 5:
			return True
	
				
	if move_converter_y_to_n(move[1]) == (-n / 2):
		counter = 0
		while board[current_position] == player:
			current_position = one_above_current_move(current_position)
			counter += 1
		if counter == 5:
			return True

	while board[current_position] == player:
		current_position = one_below_current_move(current_position)
		if move_converter_y_to_n(current_position[1]) == (-n / 2):
			counter = 0
			while board[current_position] == player:
				current_position = one_above_current_move(current_position)
				counter += 1
			if counter == 5:
				return True
	current_position = one_above_current_move(current_position)
	counter = 0

	while board[current_position] == player:
		counter += 1
		current_position = one_above_current_move(current_position)

	if counter == 5:
		return True
		
	return False

#As mentioned above, I divided the diagonal win into two parts. The idea is that I want to count down then up. 
def diagonal_win_positive_slope(player, move):
	if player == "black":
		player = 1
	elif player == "white":
		player = 2
		
	def one_above_postive(move):
		return (move[0] + 1, move[1] - 1)
	def one_below_postive(move):
		return (move[0] - 1, move[1] + 1)

	current_position = move

	if board[one_above_postive(current_position)] != player and board[one_below_postive(current_position)] != player:
		return False

	if move_converter_x_to_n(current_position[0]) == (n / 2) or move_converter_y_to_n(current_position[1]) == (n / 2):
		counter = 0
		while board[current_position] == player:
			current_position = one_below_postive(current_position)
			counter += 1
		if counter == 5:
			return True

	if move_converter_x_to_n(current_position[0]) == (- n / 2) or move_converter_y_to_n(current_position[1]) == (- n / 2):
		counter = 0
		while board[current_position] == player:
			current_position = one_above_postive(current_position)
			counter += 1
		if counter == 5:
			return True

	while board[current_position] == player:
		current_position = one_below_postive(current_position)
		

	current_position = one_above_postive(current_position)
	counter = 0
	while board[current_position] == player:
		counter += 1
		current_position = one_above_postive(current_position)
	if counter == 5:
		return True
	return False
	

def diagonal_win_negative_slope(player, move):
	if player == "black":
		player = 1
	elif player == "white":
		player = 2
	def one_above_negative(move):
		return (move[0] - 1, move[1] - 1)
	def one_below_negative(move):
		return (move[0] + 1, move[1] + 1)
	
	current_position = move

	if board[one_above_negative(current_position)] != player and board[one_below_negative(current_position)] != player:
		return False

	if move_converter_x_to_n(current_position[0]) == (- n / 2) or move_converter_y_to_n(current_position[1]) == (n / 2):
		counter = 0
		while board[current_position] == player:
			current_position = one_below_negative(current_position)
			counter += 1
		if counter == 5:
			return True

	if move_converter_x_to_n(current_position[0]) == (n / 2) or move_converter_y_to_n(current_position[1]) == (- n / 2 ):
		counter = 0
		while board[current_position] == player:
			current_position = one_above_negative(current_position)
			counter += 1
		if counter == 5:
			return True

	while board[current_position] == player:
		current_position = one_below_negative(current_position)

	current_position = one_above_negative(current_position)
	counter = 0
	while board[current_position] == player:
		counter += 1
		current_position = one_above_negative(current_position)
	if counter == 5:
		return True
		
	return False
	

def check_for_wins(player, move):
	return horizontal_win(player, move) or vertical_win(player, move) or diagonal_win_positive_slope(player, move) or diagonal_win_negative_slope(player, move)



#NOW LET'S START THE GAME
#The dirction of the game is that game ends if and only if there are 5 stones with the same color are in a row. No less than 5 and no more than 5.

print("How to Play: The goal of this game is to place EXACTLY 5 of your stones before your opponent does. The game will ask you to select x and y coordinates.")
print("You can win by placing five stones HORIZONTALLY, VERTICALLY, and DIAGONALLY.")
print("You will be able to see the coordinate numbers on the x and y axes")
print("It's a simple but fun game that requires clever strategies and attention to details.")
print("There will be a go-board drawn to you soon. Check out the Python Turtle Graphics window!")
print("Have fun, and crush your opponent!")

t.hideturtle()
t.speed(0) #This speeds up the turtle drawing.
drawboard(n)
available_space = 225

while in_progress:
	validinput = False
	flag = 0
	while not validinput:
		try: 
			x = eval(input("{0}, choose your x - coordinate.".format(player)))
			y = eval(input("{0}, choose your y - coordinate.".format(player)))

			if (x <= 14 and x >=0) or (y <= 14 and y >= 0):
				validinput = True
				move = (x,y)
				if board[move] == black_stone or board[move] == white_stone:
					print("That spot is already occupied. Pick again")
					validinput = False
			else: 
				print("Your coordinate is out of boundary. Please, pick again.")
		except TypeError:
			print("wrong type x or y")
		except NameError: 
			print("invalid value")
		except SyntaxError: 
			print("No input value")
		except KeyError: 
			print("stop trying to break this")

	if player == "black":
		board[move] = black_stone
		go_stone_placer(player,x,y)
		available_space -= 1
		if check_for_wins(player, move):
			print("Black wins!")
			in_progress = False
		player = "white"
	else:	
		board[move] = white_stone
		go_stone_placer(player,x,y)
		available_space -= 1
		if check_for_wins(player, move):
			print("White wins!")
			in_progress = False
		player = "black"
	if available_space == 0: 
		print('Game has ended in a draw')
		break 

	


	#Add code for AI


#IMPORTANT!!!!!!!!!!
# Please when you are running the game, make sure you input x and y values when it asks you to. The code breaks if you input nothing. I did not know how to continuously ask for a player to input a value if he or she hasn't inputed anything.
#Also, instead of using lists, I used the dictionary function in python. Personally, it just made more sense to use dictionary than list to represent board coordinates.








