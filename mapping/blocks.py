import math

class Block:
	def __init__(self, depth, turn_angle, color, in_place=False):
		self.turn_angle = turn_angle
		self.depth = depth
		self.color = color
		self.in_place = in_place
		self.x = 0
		self.y = 0

	def __repr__(self):
		return f"Block(x={self.x}, y={self.y}, color='{self.color}', in_place={self.in_place})"
	
	def calculate_coordinates(self, h, k):
		theta = self.turn_angle
		theta = math.radians(theta)
		# Logically good method
		delta_x = math.sin(theta)
		delta_y = math.cos(theta)
		x = h + delta_x
		y = k + delta_y
		# Overkill or useless method I came up with being a huge DUMBASS
		# cot = (math.cos(theta)/math.sin(theta))
		# r = self.depth
		# a = 1 + 1/cot
		# b = (0-(2*k))/cot**2 + 2*h/cot - 2/cot
		# c = (k**2)/(cot**2) + 3*(h**2) - (2*k*h)/cot + k*k + 2*h + - 2*k/cot - r**2
		# discriminant = b**2 - 4*a*c
		# if discriminant < 0:
		# 	raise ValueError("No real roots")
		# y1 = (-b + math.sqrt(discriminant)) / (2*a)
		# y2 = (-b - math.sqrt(discriminant)) / (2*a)
		# y = y1 if y1 >= 0 else y2
		# x = (y -k + cot*h)/cot
		self.x = x
		self.y = y