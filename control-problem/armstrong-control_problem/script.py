#!/usr/bin/env python

# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

# In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <http://unlicense.org>

import sys, copy
from PIL import Image

def assemble_image(n=1, m=1, co = ((0,0)), action = 0, name = 'image', ending = False):
	imsize = 194;
	images = map(Image.open, ['blank.png', 'box.png',	 'robot.png', 'camera_range.png', 'camera.png', 'exit.png', 'arrow.png'])
	img = Image.new('RGBA', ((n+1)*imsize, (m+1)*imsize), "white")

	view_ends = 0
	for k in co[1:]:
		if k[1] == 0 and k[0] > view_ends:
			view_ends = k[0]

	for i in range(n):
		for j in range(m):
			img.paste(images[0], (i*imsize, (m-j-1)*imsize))
			if j == 0 and i >= view_ends:
				img.paste(images[3], (i*imsize, (m-j-1)*imsize))
			if i == co[0][0] and j == co[0][1]:
				img.paste(images[2], (i*imsize, (m-j-1)*imsize), images[2])
			for k in co[1:]:
				if i == k[0] and j == k[1]:
					img.paste(images[1], (i*imsize, (m-j-1)*imsize))

	img.paste(images[4], (n*imsize, (m-1)*imsize))
	img.paste(images[5], (0, m*imsize))
	pixels = img.load() # create the pixel map
	if ending:
		for i in range(img.size[0]): # for every pixel:
			for j in range(img.size[1]):

				newR = min(pixels[i,j][0]+50, 255)
				newG = max(pixels[i,j][1]-50, 0)
				newB = max(pixels[i,j][2]-50, 0)
				newA = pixels[i,j][3]
				pixels[i,j] = (newR, newG, newB)
	elif action >= 0 and action <= 3:
		if action == 0:
			arrowimage = images[6]
		elif action == 1:
			arrowimage = images[6].rotate(180)
		elif action == 2:
			arrowimage = images[6].rotate(90)
		elif action == 3:
			arrowimage = images[6].rotate(-90)
		img.paste(arrowimage, (co[0][0]*imsize, (m - co[0][1] - 1)*imsize), arrowimage)
	img.save(name + '.png')


# Class State starts here

class State:
	def __init__(self, n = 1, m = 1, co = ((0,0),) ):
		self.setup(n, m, co)
		self.old_q = [0, 0, 0, 0]
		self.new_q = [0, 0, 0, 0]
	def setup(self, n = 1, m = 1, co = ((0,0),) ):
		self.x_size = n
		self.y_size = m
		self.coord = tuple(tuple(x) for x in co)

	def qval(self):
		return max(self.old_q)

	def best_action(self):
		action = 0
		for ac in range(len(self.old_q)):
			if self.old_q[ac] > self.old_q[action]:
				action = copy.copy(ac)
		return action

	def box_at(self, pos=(0,0)):
		for boxes in range(len(self.coord)):
			if pos == self.coord[boxes]:
				return boxes
		return 0

	def move_to(self, pos=[0,0], act=0):
	# 0 goes left, 1 goes right, 2 goes down, 3 goes up
		change = [[-1,0], [1,0], [0,-1], [0,1]]
		return [pos[0] + change[act][0], pos[1] + change[act][1]]

	def pos_in_range(self, pos=[0,0]):
		if pos[0] < 0 or pos[1] < 0:
			return False
		if pos[0] >= self.x_size or pos[1] >= self.y_size:
			return False
		return True

	def camera_blocked(self):
		for boxes in self.coord[1:]:
			if boxes[0] > 0 and boxes[1] == 0:
				return True
		return False

	def act(self, act=0):
		if act < 0 or act > 3:
			print ('Error: action out of range.')
		new_pos = self.move_to(self.coord[0], act)
		new_coord = list(list(x) for x in self.coord)
		finished = False
		rew = -0.001

		box = self.box_at(tuple(new_pos));
		new_coord[0] = new_pos

		if not self.pos_in_range(new_pos):
			finished = True
		elif box != 0:
			new_box_pos = self.move_to(self.coord[box], act)
			if not self.pos_in_range(new_box_pos) or self.box_at(tuple(new_box_pos)) != 0:
				del new_coord[box]
				if new_box_pos == [0,-1]:
					rew = 1
					if not self.camera_blocked():
						finished = True
			else:
				new_coord[box] = new_box_pos
		new_coord_tuple = tuple(tuple(x) for x in new_coord)
		return (self.x_size, self.y_size, new_coord_tuple, rew, finished)

	def printstate(self):
		print(self.x_size, self.y_size)
		print(self.coord)
		print(self.old_q, self.new_q)

	def check(self):
		for i in range(len(self.coord)):
			if not self.pos_in_range(self.coord[i]):
				return False
			for j in range(len(self.coord)):
				if i != j and self.coord[i] == self.coord[j]:
					return False
		return True

	def increment(self):
		incremented = False
		new_coord = list(list(x) for x in self.coord)
		k = 0;
		while not incremented:
			if k >= len(new_coord):
				incremented = True
			elif new_coord[k][0] < self.x_size-1:
				new_coord[k][0] = new_coord[k][0] + 1
				incremented = True
			elif new_coord[k][1] < self.y_size-1:
				new_coord[k][0] = 0
				new_coord[k][1] = new_coord[k][1] + 1
				incremented = True
			else:
				new_coord[k][0] = 0
				new_coord[k][1] = 0
			k = k + 1
		new_coord_tuple = tuple(tuple(x) for x in new_coord)
		return new_coord_tuple


# State-space class

class StateSpace:
	def __init__(self, n = 1, m = 1, boxes = 0 ):
		self.space = {}
		self.x_size = n
		self.y_size = m
		self.box_num = boxes
		self.dosomething(0)


	def dosomething(self, func = 0, filename = 'output'):
		if func == 3:
			file = open(filename + '.txt', 'w')
		for k in range(self.box_num + 1):
			for i in range(1000000):
				if i == 0:
					newer_state_tuple = tuple((0,0) for x in range(self.box_num + 1 - k))
					final_state_tuple = newer_state_tuple
				else:
					newer_state_tuple = self.space[newer_state_tuple].increment()

				if newer_state_tuple == final_state_tuple and i != 0:
					break

#here we list the various functions that can happen

				if func == 0:
					self.space[newer_state_tuple] = State(self.x_size, self.y_size, newer_state_tuple)
				elif func == 1:
					for ac in range(4):
						sprime = self.space[newer_state_tuple].act(ac)
						if sprime[4] == True:
							self.space[newer_state_tuple].new_q[ac] = copy.copy(sprime[3])
						else:
							self.space[newer_state_tuple].new_q[ac] = copy.copy(sprime[3] + self.space[sprime[2]].qval())
				elif func == 2:
					self.space[newer_state_tuple].old_q = copy.deepcopy(self.space[newer_state_tuple].new_q)
				elif func == 3:
					if i == 0 and k == 0:
						file.write(str(self.x_size))
						file.write('\n')
						file.write(str(self.y_size))
						file.write('\n')
					file.write(str(newer_state_tuple))
					file.write('\n')
					file.write(str(self.space[newer_state_tuple].old_q))
					file.write(' ')
					file.write(str(self.space[newer_state_tuple].new_q))
					file.write(' ')
					file.write(str(self.space[newer_state_tuple].qval()))
					file.write(' ')
					file.write(str(self.space[newer_state_tuple].best_action()))
					file.write('\n')

		if func == 3:
			file.close()

	def movement(self, start=((0,0),), name_root = 'test'):
		notfinished = True
		pos = start
		travel = 0
		while notfinished:
			action = self.space[pos].best_action()
			assemble_image(self.x_size, self.y_size, pos, action, name_root + '_' + str(travel).zfill(3), False)
			sprime = self.space[pos].act(action)
			if sprime[4]:
				notfinished = False
				assemble_image(self.x_size, self.y_size, pos, action, name_root + '_' + str(travel).zfill(3), False)
				pos = sprime[2]
				travel = travel + 1
				assemble_image(self.x_size, self.y_size, pos, 5, name_root + '_' + str(travel).zfill(3), False)
				assemble_image(self.x_size, self.y_size, pos, 5, name_root + '_' + str(travel).zfill(3) + '_end', True)
			pos = sprime[2]
			travel = travel + 1


# main body
xs = 5
ys = 4

new_state_tuple = ((0, 0), (0, 0), (0, 0), (0, 0))
start_state_tuple = ((2, 2), (2, 1), (1, 2), (3, 2))

#assemble_image(xs, ys, ((0, 1), (2, 1), (0, 0), (3, 2)), 5, "intro_0565", False)

spacial = StateSpace(xs, ys, 3)

for ki in range(47):
	spacial.dosomething(3, 'output/output_' + str(ki).zfill(2))
	spacial.movement(start_state_tuple, 'output/path_' + str(ki).zfill(2))

	spacial.dosomething(1)
	spacial.dosomething(2)
