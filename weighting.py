# getting ready to implement elo and win/loss

from __future__ import division
import math

class popularity(object):

	# iterates popularity by one
	def alter(self, current):
		pop = current[0]
		return (pop + 1,)
	default = (1,)

class elo(object):
	def __init__(self, new):
		if new == 0:
			new = 2000
		self.new = new 
		self.default = (new,)

    # overrides with higher elo
	def alter(self, current):
		rating = current[0]
		if self.new > rating:
			return (self.new,)
		else: return current

class winloss(object):
	def __init__(self, new):
		self.new = new 

		# tie
		if self.new == "t":
			self.default = (1,1,1)
		# win
		elif self.new == "w":
			self.default = (2,2,1)
		# loss
		else:
			self.default = (0,0,1)

	def alter(self, current):
		(weight,win,loss) = current

		#tie
		if self.new == "t":
			return current
		# win
		elif self.new == "w":
			win += 1
			return ((win/loss),win,loss)
		# loss
		else:
			loss += 1
			return ((win/loss),win,loss)

class lightblue(object):
	def __init__(self, elo, wlt):
		if elo == 0:
			elo = 2000
		self.elo = elo
		self.wlt = wlt 

		# tie
		if self.wlt == "t":
			self.default = (math.exp(self.elo/1000)/10,)
		# win
		elif self.wlt == "w":
			self.default = (math.exp(self.elo/1000),)
		# loss
		else:
			self.default = (-1/(math.exp(self.elo/1000)),)

	def alter(self, current):
		value = current[0]
		change = self.default[0]
		return (value + change,)
		


