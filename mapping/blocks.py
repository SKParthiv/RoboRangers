class Block:
	def __init__(self, depth, turn_angle, color, in_place=False):
		self.turn_angle = turn_angle
		self.depth = depth
		self.color = color
		self.in_place = in_place

	def __repr__(self):
		return f"Block(x={self.x}, y={self.y}, color='{self.color}', in_place={self.in_place})"