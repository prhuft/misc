""" Snakey Snake, attempted April 2019 for Marge-parge
	Preston Huft
	
	Notes:
	- trying to read keypresses everytime the update is called does not work. 
	it waits for an asynchronous key press rather than proceeding. for now,
	abandon keypresses. if time in future, look at io_events.py and try to 
	raise keypress events. 
	- there is an error in updating the snake when the direction is changed.
	- for now, just make the game automated. ai, i guess. train it snake v
	snake, or snake v many snakes. The former is computationally much faster,
	and the training epochs will probably need to be fewer as well. 
"""

## LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math as m
from random import random as rand
#from msvcrt import getch # for reading keypresses

## GLOBAL PARAMS
GRID_SIZE = 20
SNAKES = 1

## METHODS
def snake_init(n):
	"""n units long snake"""
	snake = np.zeros((2,n))

	# build a vertical snake in lower left
	# the array is built so the first element of the list is the head of the
	# snake
	for i in range(0,n):
		snake[0,i],snake[1,i] = 0,n-i

	return snake
	
## MAIN 

#TODO: MAKE SNAKES A CLASS, so that each snake is bound to it's previous 
#directions

###############################################################################
## BUILD THE SNAKES
###############################################################################

# the initial snake
snake_len = 5
snake_arr=snake_init(snake_len)

# array of the last four directions used; [1=u, -1=d, 1=r, -1=l]
DIRS = np.array([-1,1,-1,1])

# last direction changes. first element is most recent; 0=u,1=d,2=r,3=l
dirs = np.array([0,0,0,0])

###############################################################################
## BUILD THE FIGURE
###############################################################################

fig = plt.figure()

ax = fig.add_subplot(111)
ax.set_ylim(0,GRID_SIZE)
ax.set_xlim(0,GRID_SIZE)
ax.set_axis_off()
ax.set_aspect(aspect='equal')
ax.set_facecolor('black')

fig.patch.set_facecolor('black')
fig.add_axes(ax)

snake, = ax.plot(snake_arr[0],snake_arr[1],color='red',lw=3)

###############################################################################
## RUN THE INTERACTIVE ANIMATION
###############################################################################

# use fig.canvas.draw() instead of animate
def update(frames):
	"""update snake position(s) on grid"""	
	xpts,ypts = snake_arr[0],snake_arr[1]
	
	# eventually put in keypresses maybe....
	
	# print the coords
	# print("i=",i)
	# z=zip(xpts,ypts)
	# for c in z:
		# print("x,y:",c)
		# print("-----------")
	
	# programmatic direction changes
	last = np.copy(dirs)
	if (i) % 5 == 0:		
		dirs[0]+=1
		dirs[1]=last[0]
		dirs[2]=last[1]
		dirs[3]=last[2]
		
	print("dirs:",dirs)

	i = 0 # overall snake index
	for d in dirs:
		if d==0 | d==1: # up or down 
			dy = DIRS[d]
			for s in range(i,snake_len):
				ypts[s]+=dy
				i+=1
				if xpts[s-1]!=xpts[s]:
					break
		elif d==2 | d==3:
			dx = DIRS[d]
			for s in range(i,snake_len):
				xpts[i]+=dx
				i+=1
				if ypts[s-1]!=ypts[s]:
					break
		if i==snake_len:
			break
				


	# simulate key presses until i use actual keys
	
	# update the snake!
	
	
	
	snake.set_data(snake_arr[0],snake_arr[1])

	return snake,

anim = animation.FuncAnimation(fig, update,frames=16,blit=True)#,repeat=True)

plt.show()