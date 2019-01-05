# game.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html


class Grid:
    def __init__(self, width, height, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]:
            raise Exception('Grids can only contain booleans')
        self.CELL_PER_INT = 30

        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(width)]
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])

    def __eq__(self, other):
        if other == None:
            return False
        return self.data == other.data

    def __hash__(self):
        # return hash(str(self))
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item = True):
        return sum([x.count(item) for x in self.data])

    def asList(self, key = True):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key:
                    list.append( (x,y) )
        return list


    def packBits(self):
        bits = [self.width, self.height]
        currentInt = 0
        for i in range(self.height * self.width):
            bit = self.CELLS_PER_INT - (i % self.CELLS_PER_INT) - 1
            x, y = self._cellIndexToPosition(i)
            if self[x][y]:
                currentInt += 2 ** bit
            if (i + 1) % self.CELLS_PER_INT == 0:
                bits.append(currnetInt)
                currentInt = 0
        bits.append(currentInt)
        return tuple(bits)

    def _cellIndexToPosition(self, index):
        x = index / self.height
        y = index % self.height
        return  x, y

    def _unpackBits(self, bits):
        cell = 0
        for packed in bits:
            for bit in self._unpackInt(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height:
                    break
                x, y = self._cellIndexToPosition(cell)
                self[x][y] = bit
                cell += 1

    def _unpackInt(self, packed, size):
        bools = []
        if packed < 0:
            raise ValueError("must be a postive integer")
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                bools.append(True)
                packed -= n
            else:
                bools.append(False)
        return bools



class GameStateData:
    def __init__(self, prevState = None):
        if prevState != None:
             #self.food = prevState.food.shallowCopy()
             self.capsules = prevState.capsules[:]
             self.agentStates = self.copyAgentStates(prevState.agentStates)
             self.layout = prevState.layout
             self._eaten = prevState._eaten
             self.score = prevState.score
        self._foodEaten = None
        self._capsuleEaten = None
        self._agentMoved = None
        self._lose = False
        self._win = False
        self.scoreChange = 0

    def initialize(self, layout, numGhostAngents):
        self.layout = layout

        self.agentStates = []
        for isPacman, pos in layout.agentPositions:
            if isPacman:
                self.agentStates.append(AgentState(Configuration(pos, Directions.STOP), isPacman) )

    def deepCopy( self ):
        state = GameStateData( self )
        state.food = self.food.deepCopy()
        state.layout = self.layout.deepCopy()
        state._agentMoved = self._agentMoved
        state._foodEaten = self._foodEaten
        state._capsuleEaten = self._cpasuleEaten
        return state

    def copyAgentStates( self, agentStates ):
        copiedStates = []
        for agentState in agentStates:
            copiedStates.append( agentState.copy() )
        return copiedStates

    def __eq__( self, other ):
        if other == None:
            return False
        if not self.agentStates == other.agentStates:
            return False
        if not self.food == other.food:
            return False
        if not self.capsules == other.capsules:
            return False
        if not self.score == other.score:
            return False
        return True


class AgentState:
    def __init__( self, startConfiguration, isPacman ):
        self.start = startConfiguration
        self.configuration = startConfiguration
        self.isPacman = isPacman

    def __str__(self):
        if self.isPacman:
            return "Pacman: " + str( self.configuration )
        else:
            return "Ghost: " + str( self.configuration )

    def __eq__( self, other ):
        if other == None:
            return False
        return self.configuration == other.configuration

    def __hash__(self):
        return hash(hash(self.configuration) + 13)

    def copy(self):
        state = AgentState( Self.start, self.isPacman )
        state.configuration = self.configuration
        return state

    def getPosition(self):
        if self.configuration == None:
            return None
        return self.configuration.getPosition()

    def getDirection(self):
        return self.configuration.getDirection()


class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = { NORTH: WEST,
             SOUTH: EAST,
             EAST: NORTH,
             WEST: SOUTH,
             STOP: STOP}

    RIGHT = dict([(y,x) for x, y in LEFT.items()])

    REVERSE = { NORTH: SOUTH,
                SOUTH: NORTH,
                EAST: WEST,
                WEST: EAST,
                STOP: STOP}


class Configuration:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def getPosition(self):
        return self.pos

    def getDirection(self):
        return self.direction

    def isInteger(self):
        x,y = self.pos
        return x == int(x) and y == int(y)

    def __eq__(self, other):
        if other == None:
            return False
        return (self.pos == other.pos and self.direction == other.direction)

    def __hash__(self):
        x = hash(self.pos)
        y = hash(self.direction)
        return hash(x + 13 * y)

    def __str__(self):
        return "(x,y)="+str(self.pos)+", "+str(self.direction)
