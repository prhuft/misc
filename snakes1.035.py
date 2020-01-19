""" Snakey Snake, April 2019
	Preston Huft
	
	Version notes:
	- the game works
	- finite state machine structure
	- added in 4th mode: "CP Train" 

	
	Bugs: 
	- new snake section appears initially appears in unexpected location
	
	Todo:
	- add NN training structure and effective cost
	- need to make snake a class with reset method
	- ditto but about food, or maybe just the instance of a game itself
	- should also put everything in a main() function
"""

## LIBRARIES
import math as m
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random as rand
import time

## LOCAL FILES
import snakenet as snet

## "CONSTANTS"
GRID_SIZE = 20
SNAKES = 1
LEN = 5
DIRS = np.array([1,-1,1,-1,0]) # directional increments [1=u,-1=d,1=r,-1=l,0=None]
START_TITLE = "SNAKEY SNAKES | HIGH SCORE: %s \n Enter to Play, Q to Quit"
GAME_TITLE = "SNAKE LENGTH: %s | HIGH SCORE: %s \n Q to Quit"
OVER_TITLE = "GAME OVER \n SNAKE LENGTH: %s | HIGH SCORE: %s" \
			"\n Enter: Title Screen, Q: Quit"
HIDDEN_TITLE = "WOAH, WELCOME TO HIDDEN CP MODE!!" \
			"\n P: Title Screen" \
			"\n SNAKE LENGTH: %s | HIGH SCORE: %s"
			

## VARS
state = 1 # 1 = title screen, 2 = running, 3 = game over, 0 = quit
dir = 0 # the most recent direction of movement
snake_len = LEN # the initial snake length
title = GAME_TITLE
highscr = snake_len

## METHODS
def snake_init(n):
	""" snake oriented vertically in the lower left of the grid, with the
		max length acheiveable in the game, which is more efficient than
		appending to the array later.
		
		n is the starting length of the snake.
	"""
	length = GRID_SIZE*GRID_SIZE
	snake = np.zeros((2,length)) 

	for i in range(0,n):
		snake[0,i],snake[1,i] = 5,n-i # x, y

	return snake
	
def snake_food(n):
	""" n morcels of food, returned with random coordinates."""
	global GRID_SIZE
	x,y = np.random.randint(0,high=GRID_SIZE,size=(2,n))
	return x,y
			
def onkeypress(event):
	""" Get keypress and set direction of snake movement if an arrowkey is 
		pressed. dir is set to the index of DIR corresponding to the correct
		increment. Numbers 0-3 are used to distinguish directionaliy. Disallow
		antiparallel direction changes, e.g. right to left. 
	"""
	key = event.key
	global dir 
	global state 
	
	print('key pressed: ', event.key)
	key = event.key
	
	# check for direction changes

	# if state != 4: # disallow directionals in cp training
	if key == 'right':
		if dir != 3:
			dir = 2 
	elif key == 'left':
		if dir != 2:
			dir = 3
	elif key == 'up':
		if dir != 1:
			dir = 0
	elif key == 'down':
		if dir != 0:
			dir = 1
	elif key == 'q':
		fig.canvas.mpl_disconnect(cid)
		state = 0 # quit the game
			
	# check for state changes
	elif state == 1:
		if key == 'enter':
			state = 2 # change to game running
		elif key == 'p':
			state = 4 # train the cp!
	elif state == 3:
		if key == 'enter':
			state = 1 # change to title screen
	elif state == 4:
		if key == 'p':
			state = 1 # change to title screen
			
def sigmoid(z):
	return 1/(1+np.exp(-z))
	
def bingrid(xarr,yarr):
	""" convert snake coords to a binary grid to pass to the nn
	"""
	grid = zeros(GRID_SIZE*GRID_SIZE)
	
	for x,y in zip(xarr,yarr):
		grid[int(x+y*GRID_SIZE)]=1
	return grid
		
## MAIN 

###############################################################################
## BUILD THE SNAKE AND FIGURE
###############################################################################

# the initial snake
snake_arr=snake_init(snake_len)

# store the most recent direction. 0=u,1=d,2=r,3=l
dir = 0

fig = plt.figure()
fig.patch.set_facecolor('black')

ax = fig.add_subplot(111)
ax.set_ylim(0,GRID_SIZE)
ax.set_xlim(0,GRID_SIZE)
ax.set_axis_off()
ax.set_aspect(aspect='equal')
ax.set_title(START_TITLE,color='g')
fig.add_axes(ax)

# Start event handler. This must come after the figure is built, and before the
# plot is shown. 
cid = fig.canvas.mpl_connect('key_press_event',onkeypress)

plt.ion()
plt.show()

# initialize the snake points to plot 
snake_line, =ax.plot(snake_arr[0][:snake_len],snake_arr[1][:snake_len],
				color='red',lw=3,marker='s',linestyle='',markersize=12)
xpts,ypts = snake_arr[0],snake_arr[1]

###############################################################################
## RUN THE GAME
###############################################################################

while True:
	if state == 1: ## TITLE SCREEN
	
		ax.set_title(START_TITLE % highscr,color='g')
		while True:
			time.sleep(.100)
			
			# the snake coordinates
			xpts_old = np.copy(xpts)
			ypts_old = np.copy(ypts)
			
			# update the snake position
			if (dir==0) | (dir==1): # up or down
				ypts[0]=(ypts[0]+DIRS[dir]) % GRID_SIZE
			elif (dir==2) | (dir==3): # left or right
				xpts[0]=(xpts[0]+DIRS[dir]) % GRID_SIZE
			
			for i in range(1,snake_len):
				xpts[i]=xpts_old[i-1]
				ypts[i]=ypts_old[i-1]
			
			if state != 1:
				break
				
			snake_line.set_data(xpts[:snake_len],ypts[:snake_len])
			fig.canvas.draw()
			fig.canvas.flush_events()
	
	elif state == 2: ## PLAYING THE GAME
			
		# reset the snake length and update the plot
		snake_len = LEN
		snake_line.set_data(xpts[:snake_len],ypts[:snake_len])
		ax.set_title(GAME_TITLE % (snake_len,highscr),color='r')

		# add some food; should update the food array
		# foodx,foody = snake_food(5)
		foodx,foody = snake_food(LEN)
		food_pts, = ax.plot(foodx,foody,linestyle='',marker='o')

		while True: ## THE GAME RUNNING LOOP
			time.sleep(.100)
				
			# the snake coordinates
			xpts_old = np.copy(xpts)
			ypts_old = np.copy(ypts)
			
			# update the snake position
			if (dir==0) | (dir==1): # up or down
				ypts[0]=(ypts[0]+DIRS[dir]) % GRID_SIZE
			elif (dir==2) | (dir==3): # left or right
				xpts[0]=(xpts[0]+DIRS[dir]) % GRID_SIZE
			
			## everything after this can be wrapped in a function i think..
			for i in range(1,snake_len):
				xpts[i]=xpts_old[i-1]
				ypts[i]=ypts_old[i-1]
				
			# check if the snake hit itself
			for i in range(1,snake_len):
				if (xpts[0]==xpts[i]) & (ypts[0]==ypts[i]):
					state = 3
					break
			
			# check if the snake head hits any of the food; respond accordingly
			for i in range(0,len(foodx)):
				if xpts[0]==foodx[i]:
					if ypts[0]==foody[i]:
						foodx = np.delete(foodx,i)
						foody = np.delete(foody,i)
						
						# regenerate the food if it is all gone
						if len(foodx)==0:
							foodx,foody = snake_food(snake_len)
						# if snake_len<GRID_SIZE*GRID_SIZE: <-- too unlikely
						snake_len+=1
						
						# spawn new food 
						if np.random.rand() > 0.1:
							x,y = snake_food(1)
							foodx = np.append(foodx,x)
							foody = np.append(foody,y)
							
						# update the title
						if snake_len > highscr:
							highscr = snake_len
						ax.set_title(GAME_TITLE % (snake_len,highscr),
									color='r')
						break
			
			if state != 2: #QUIT:
				break
			
			# update the plot
			snake_line.set_data(xpts[:snake_len],ypts[:snake_len])
			food_pts.set_data(foodx,foody)
			fig.canvas.draw()
			fig.canvas.flush_events()
			
			
	elif state == 3: ## THE GAME OVER SCREEN
		ax.set_title(OVER_TITLE % (snake_len,highscr),color='w')
		food_pts.set_data([],[]) # clear the food from the plot
		
		while True:
			time.sleep(.100)
				
			# the snake coordinates
			xpts_old = np.copy(xpts)
			ypts_old = np.copy(ypts)
			
			# update the snake position
			if (dir==0) | (dir==1): # up or down
				ypts[0]=(ypts[0]+DIRS[dir]) % GRID_SIZE
			elif (dir==2) | (dir==3): # left or right
				xpts[0]=(xpts[0]+DIRS[dir]) % GRID_SIZE
			
			for i in range(1,snake_len):
				xpts[i]=xpts_old[i-1]
				ypts[i]=ypts_old[i-1]
			
			if state != 3: # quit or go to title screen
				break
			
			# update the plot
			snake_line.set_data(xpts[:snake_len],ypts[:snake_len])
			fig.canvas.draw()
			fig.canvas.flush_events()
			
	elif state == 4: ## THE HIDDEN CP mode!
	
		## everything below based on state == 2
		
		# reset the snake length and update the plot
		snake_len = LEN
		snake_line.set_data(xpts[:snake_len],ypts[:snake_len])
		ax.set_title(HIDDEN_TITLE % (snake_len,highscr),color='purple')
		
		# add some food; should update the food array
		foodx,foody = snake_food(LEN)
		food_pts, = ax.plot(foodx,foody,linestyle='',marker='o')
		
		##  stuff for neural net initialized here
		lifepts = snake_len

		while True: ## THE GAME RUNNING LOOP
			time.sleep(.100)
				
			# to pass to the nn later
			snake_in = bingrid(xpts[:snake_len],ypts[:snake_len])
			
			## COMPUTER 'chooses' dir:
			# todo: disallow external dpad presses
			dir = int(3*rand()) # use nn output 
			
			# the snake coordinates
			xpts_old = np.copy(xpts)
			ypts_old = np.copy(ypts)
			
			# update the snake position
			if (dir==0) | (dir==1): # up or down
				ypts[0]=(ypts[0]+DIRS[dir]) % GRID_SIZE
			elif (dir==2) | (dir==3): # left or right
				xpts[0]=(xpts[0]+DIRS[dir]) % GRID_SIZE
			
			## everything after this can be wrapped in a function
			for i in range(1,snake_len):
				xpts[i]=xpts_old[i-1]
				ypts[i]=ypts_old[i-1]
				
			# check if the snake hit itself
			for i in range(1,snake_len):
				if (xpts[0]==xpts[i]) & (ypts[0]==ypts[i]):
					state = 4 # important! stay in this mode!
					
					# reset the snake length and update the plot
					snake_len = LEN
					snake_line.set_data(xpts[:snake_len],ypts[:snake_len])
					ax.set_title(HIDDEN_TITLE % (snake_len,highscr),color='purple')
					
					# add some food; should update the food array
					foodx,foody = snake_food(LEN)
					food_pts.set_data([],[])
					food_pts, = ax.plot(foodx,foody,linestyle='',marker='o')
					
					lifepts = 0 # lifepts immediately floors if we lose
					
					break
				else:
					lifepts += 1
			
			# check if the snake head hits any of the food; respond accordingly
			for i in range(0,len(foodx)):
				if xpts[0]==foodx[i]:
					if ypts[0]==foody[i]:
						foodx = np.delete(foodx,i)
						foody = np.delete(foody,i)
						
						# regenerate the food if it is all gone
						if len(foodx)==0:
							foodx,foody = snake_food(snake_len)
						# if snake_len<GRID_SIZE*GRID_SIZE: <-- too unlikely
						snake_len+=1
						
						# spawn new food 
						if np.random.rand() > 0.1:
							x,y = snake_food(1)
							foodx = np.append(foodx,x)
							foody = np.append(foody,y)
							
						# update the title
						if snake_len > highscr:
							highscr = snake_len
						ax.set_title(HIDDEN_TITLE % (snake_len,highscr),
									color='purple')
						break
			
			if state != 4: #QUIT:
				food_pts.set_data([],[]) # clear the food from the plot
				break
			
			# update the plot
			snake_line.set_data(xpts[:snake_len],ypts[:snake_len])
			food_pts.set_data(foodx,foody)
			fig.canvas.draw()
			fig.canvas.flush_events()
			
			# run the neural net:
			# dir = (snakes_in,lifepts,dir)
	
	if state == 0: ## QUIT THE GAME
		break # exits the outermost loop, ending the program entirely
		

## DEFINING A COST FUNCTION FOR A NN

# option 1: output_j = net(frame_i) 
#			C(buttons out,resulting frame) -> 0 (didn't die) or 1 (died)
# option 1.5: C also func of the snake length
# option 2:  a whole set of frames and corresponding button presses is the net input
# 			C(length of snake,head hit body?) -> tends toward 0 for max snake length,
# 			blows up for head hit body? which is 0 or 1
# 	problem: this would mean the input vector isn't a fixed length. hmm.

## converting the input array elements from analog values to "useful" inputs
# scale each coord to be between 0 and 1... just use a sigmoid. mmm, but should take grid
# scale into acct. so x -> x/gridsize? yeah sure. but then have a scaling in sigmd too
