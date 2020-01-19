""" Snakey Snake, April 2019 for Marge-parge
	Preston Huft
	
	Version notes:
	- the game works
	- finite state machine structure
	
	Bugs: 
	- new snake section appears initially appears in unexpected location
"""

## LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math as m
import time

## CONSTANTS
GRID_SIZE = 20
SNAKES = 1
LEN = 5
DIRS = np.array([1,-1,1,-1]) # directional increments [1=u,-1=d,1=r,-1=l]
START_TITLE = "SNAKEY SNAKES | HIGH SCORE: %s \n Enter to Play, Ctrl+C to Quit"
GAME_TITLE = "SNAKE LENGTH: %s | HIGH SCORE: %s \n Ctrl+C to Quit"
OVER_TITLE = "GAME OVER \n SNAKE LENGTH: %s | HIGH SCORE: %s" \
			"\n Enter: Title Screen, Ctrl+C: Quit"

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
	snake = np.zeros((2,GRID_SIZE*GRID_SIZE)) 

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
	
	# print('key pressed: ', event.key)
	key = event.key
	
	# check for direction changes
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
			
	# check for state changes
	elif state == 1:
		if key == 'enter':
			state = 2 # change to game running
	elif state == 3:
		if key == 'enter':
			state = 1 # change to title screen
	elif key == 'ctrl+c':
		fig.canvas.mpl_disconnect(cid)
		state = 0 # quit the game
		
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
	
	if state == 0: ## QUIT THE GAME
		break