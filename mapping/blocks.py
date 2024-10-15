import math

class Block:
	def __init__(self, depth, turn_angle, color, in_place=False):
		self.turn_angle = turn_angle
		self.depth = depth
		self.color = color
		self.in_place = in_place
		self.x = 0
		self.y = 0
		self.width = 3
		self.height = 5

	def __repr__(self):
		return f"Block(x={self.x}, y={self.y}, color='{self.color}', in_place={self.in_place})"