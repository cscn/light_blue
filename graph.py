import chess as ch

# make the graph with the initial config, run before using other stuff
def initialize():
	global graph
	global startpos
	starting_game = ch.Game()
	starting_game.setup()
	startpos = str(starting_game.board)
	graph = {startpos:{}}

# helper function
def best(config, color):
	global graph
	moves = graph[config]

	if moves == {}:
		return []
	else:
		moves2 = {}

		# filters for correct color
		if color == 'b':
			color = 'w'
		else: color = 'b'
		for key in moves:
			if key[1] == color:
				moves2[key] = moves[key]

		# get list of popularities
		lst = []
		for key in moves:
			lst.append(moves[key][1][0])

		# finds most popular
		top = max(lst)

		# finds all moves with top popularity
		temp = []
		for key in moves:
			if moves[key][1][0] == top:
				temp.append((key,moves[key][0]))

		# formats list
		nextmoves = []
		for item in temp:
			nextmoves.append((item[0][0],item[1]))

		# returns recommended moves in the form (move, configuration)
		return nextmoves

'''
recommends the first move
returns moves in a list of (move, resulting configuration) tuples
'''
def firstrecommend():
	global graph
	global startpos
	return best(startpos, 'b')

'''
recommends a move
returns moves in a list of (move, resulting configuration) tuples
'''
def recommendold(before, move, color, after):
	global graph
	# finds initial config
	if before in graph:
		moves = graph[before]

		# move exists
		if (move, color) in moves:

			edge = moves[(move, color)]

			# verify resulting config
			if edge[0] == after:

				# adds to popularity
				graph[before][(move, color)] = (edge[0], edge[1]+1)

				# finds destination node
				if after in graph:

					#finds most popular move
					return best(after, color)

				# destination node missing
				else: print 'Error: could not find expected destination node'

			# resulting config incorrect
			else: print 'Error: resulting config different in graph'

		# move doesn't exist
		else: 

			# resulting configuration exists
			if after in graph:

				# new edge
				graph[before][(move,color)] = (after, 1)

				# finds most popular move
				return best(after, color)


			# resulting configuration doesn't exist
			else: 

				# new node
				graph[after] = {}

				# new edge
				moves[(move, color)] = (after, 1)

				return []

	# didn't find initial config
	else: print 'Error: could not find initial configuration'

# clears graph
def reset():
	global graph
	global startpos
	graph = {startpos:{}}

# load filename
def load(name):
	f = open(name,'r')
	global graph
	graph = f.read()
	graph = eval(graph)
	f.close()

# save filename
def save(name):
	f = open(name,'w') 
	f.write(str(graph))
	f.close()


''' Testing '''
'''
# building graph from scratch, super thorough testing
initialize()

# empty graph
assert firstrecommend() == []

# make first move, tests new node, new edge, first recommend
assert recommend('A', 'mv1', 'w', 'B') == []
assert 'B' in graph
assert graph['B'] == {}
assert graph['A'][('mv1','w')] == ('B',1)
assert firstrecommend() == [('mv1', 'B')]

# make second move
assert recommend('B', 'mv2', 'b', 'C') == []
assert recommend('A', 'mv1', 'w', 'B') == [('mv2','C')]

# make third move
assert recommend('B', 'mv3', 'b', 'D') == []
# note: this ordering is mandatory
assert recommend('A', 'mv1', 'w', 'B') == [('mv2', 'C'), ('mv3', 'D')]
assert recommend('B', 'mv3', 'b', 'D') == []
assert recommend('A', 'mv1', 'w', 'B') == [('mv3', 'D')]

# make fourth move, tests new edge with existing node
assert recommend('A', 'mv4', 'w', 'D') == []
assert firstrecommend() == [('mv1', 'B')]
assert recommend('A', 'mv4', 'w', 'D') == []
assert recommend('A', 'mv4', 'w', 'D') == []
assert recommend('A', 'mv4', 'w', 'D') == []
# note: this ordering is mandatory
assert firstrecommend() == [('mv1', 'B'), ('mv4', 'D')]
assert recommend('A', 'mv4', 'w', 'D') == []
assert firstrecommend() == [('mv4', 'D')]

# save graph
save('test')

# clear graph
reset() 
assert firstrecommend() == []

# load graph
load('test')
assert firstrecommend() == [('mv4', 'D')]
'''

# getting ready to implement elo and win/loss

class popularity(object):
	def alter(self, current):
		return (current + 1,)
	default = (1,)
'''
class elo(object):
	def __init__(self, new):
        self.new = new 
	def alter(current):
	default = 1

class winloss(object):
	def __init__(self, new):
        self.new = new 
	def alter(current):
	default = 1
'''

def recommend(weight, before, move, color, after):
	global graph
	# finds initial config
	if before in graph:
		moves = graph[before]

		# move exists
		if (move, color) in moves:

			edge = moves[(move, color)]

			# verify resulting config
			if edge[0] == after:

				# grabs current weight
				current = edge[1][0]

				# alters weight
				graph[before][(move, color)] = (edge[0], weight.alter(current))

				# finds destination node
				if after in graph:

					#finds most popular move
					return best(after, color)

				# destination node missing
				else: print 'Error: could not find expected destination node'

			# resulting config incorrect
			else: print 'Error: resulting config different in graph'

		# move doesn't exist
		else: 

			# resulting configuration exists
			if after in graph:

				# new edge
				graph[before][(move,color)] = (after, weight.default)

				# finds most popular move
				return best(after, color)

			# resulting configuration doesn't exist
			else: 

				# new node
				graph[after] = {}

				# new edge
				moves[(move, color)] = (after, weight.default)

				return []

	# didn't find initial config
	else: print 'Error: could not find initial configuration'