# graphicsDisplay.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from pacman import GameState
from graphicsUtils import *
from game import *
from layout import *
import math
import time

DEFAULT_GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = formatColor(0, 0, 0)
WALL_COLOR = formatColor(0.0/255.0, 51.0/255.0, 255.0/255.0)
INFO_PANE_COLOR = formatColor(.4, .4, 0)
SCORE_COLOR = formatColor(.9, .9, .9)
PACMAN_OUTLINE_WIDTH = 2
PACMAN_CAPTURE_OUTLINE_WIDTH = 4

PACMAN_COLOR = formatColor(255.0/255.0, 255.0/255.0, 61.0/255)
PACMAN_SCALE = 0.5


WALL_RADIUS = 0.15

class InfoPane:
    def __init__(self, layout, gridSize):
         self.gridSize = gridSize
         self.width = (layout.width) * gridSize
         self.base = (layout.height + 1) * gridSize
         self.height = INFO_PANE_HEIGHT
         self.fontSize = 24
         self.textColor = PACMAN_COLOR

    def toScreen(self, pos, y = None):
         if y == None:
             x,y = pos
         else:
             x = pos

         x = self.gridSize + x
         y = self.base + y
         return x,y


class PacmanGraphics:
    def __init__(self, zoom=1.0, frameTime=0.0, capture=False):
        self.have_window = 0
        self.currentGhostImages = {}
        self.pacmanImage = None
        self.zoom = zoom
        self.gridSize = DEFAULT_GRID_SIZE * zoom
        self.capture = capture
        self.frameTime = frameTime

    def initialize(self, state, isBlue = False):
        self.isBlue = isBlue
        self.startGraphics(state)
        self.distributionImages = None
        self.drawStaticObjects(state)
        self.drawAgentObjects(state)

        self.previousState = state

    def startGraphics(self, state):
        self.layout = state.data.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.infoPane = InfoPane(layout, self.gridSize)
        self.currentState = layout

    def make_window(self, width, height):
        grid_width = (width-1) * self.gridSize
        grid_height = (height-1) * self.gridSize
        screen_width = 2*self.gridSize + grid_width
        screen_height = 2*self.gridSize + grid_height + INFO_PANE_HEIGHT

        begin_graphics(screen_width,
                       screen_height,
                       BACKGROUND_COLOR,
                       "CS188 Pacman")

    def drawStaticObjects(self, state):
        layout = self.layout
        self.drawWalls(layout.walls)
        refresh()

    def drawAgentObjects(self, state):
        #self.agentImages = [] # (agentState, image)
        for index, agent in enumerate(state.data.agentStates):
            if agent.isPacman:
                image = self.drawPacman(agent, index)
                #self.agentImages.append( (agent, image) )
        refresh()

    def drawWalls(self, wallMatrix):
        wallColor = WALL_COLOR
        for xNum, x in enumerate(wallMatrix):
            for yNum, cell in enumerate(x):
                if cell: # There is a wall here
                    pos = (xNum, yNum)
                    screen = self.to_screen(pos)
                    screen2 = self.to_screen2(pos)

                    # draw each quadrant of the square based on adjacent walls
                    wIsWall = self.isWall(xNum-1, yNum, wallMatrix)
                    eIsWall = self.isWall(xNum+1, yNum, wallMatrix)
                    nIsWall = self.isWall(xNum, yNum+1, wallMatrix)
                    sIsWall = self.isWall(xNum, yNum-1, wallMatrix)
                    nwIsWall = self.isWall(xNum-1, yNum+1, wallMatrix)
                    swIsWall = self.isWall(xNum-1, yNum-1, wallMatrix)
                    neIsWall = self.isWall(xNum+1, yNum+1, wallMatrix)
                    seIsWall = self.isWall(xNum+1, yNum-1, wallMatrix)

                    # NE quadrant
                    if (not nIsWall) and (not eIsWall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.gridSize, wallColor, wallColor, (0,91), 'arc')
                    if (nIsWall) and (not eIsWall):
                        # vertical line
                        line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5)-1)), wallColor)
                    if (not nIsWall) and (eIsWall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
                    if (nIsWall) and (eIsWall) and (not neIsWall):
                        # outer circle
                        circle(add(screen2, (self.gridSize*2*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (180, 271), 'arc')
                        line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
                        line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5))), wallColor)

                    # NW quadrant
                    if (not nIsWall) and (not wIsWall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.gridSize, wallColor, wallColor, (90, 181), 'arc')
                    if (nIsWall) and (not wIsWall):
                        # vertical line
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5)-1)), wallColor)
                    if (not nIsWall) and (wIsWall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
                    if (nIsWall) and (wIsWall) and (not nwIsWall):
                        # outer circle
                        circle(add(screen2, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize - 1, wallColor, wallColor, (270, 361), 'arc')
                        line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(-1)*WALL_RADIUS)), wallColor)
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5))), wallColor)

                    # SE quadrant
                    if (not sIsWall) and (not eIsWall):
                            # inner circle
                            circle(screen2, WALL_RADIUS * self.gridSize, wallColor, wallColor, (270, 361), 'arc')
                    if (sIsWall) and (not eIsWall):
                            # vertical line
                            line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5)+1)), wallColor)
                    if (not sIsWall) and (eIsWall):
                            # horizontal line
                            line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(1)*WALL_RADIUS)), wallColor)
                    if (sIsWall) and (eIsWall) and (not seIsWall):
                            # outer circle
                            circle(add(screen2, (self.gridSize*2*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize - 1, wallColor, wallColor, (90, 181), 'arc')
                            line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5, self.gridSize*(1)*WALL_RADIUS)), wallColor)
                            line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5))), wallColor)

                    # SW quadrant
                    if (not sIsWall) and (not wIsWall):
                            #inner circle
                            circle(screen2, WALL_RADIUS * self.gridSize, wallColor, wallColor, (180, 271), 'arc')
                    if (sIsWall) and (not wIsWall):
                            # vertical line
                            line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5)+1)), wallColor)
                    if (not sIsWall) and (wIsWall):
                            # horizontal line
                            line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(1)*WALL_RADIUS)), wallColor)
                    if (sIsWall) and (wIsWall) and (not swIsWall):
                            # outer circle
                            circle(add(screen2, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (0, 91), 'arc')
                            line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(1)*WALL_RADIUS)), wallColor)
                            line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5))), wallColor)

    def isWall(self, x, y, walls):
        if x < 0 or y < 0:
            return False
        if x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    def to_screen(self, point):
        (x, y) = point
        # y = self.height - y
        x = (x + 1)*self.gridSize
        y = (self.height - y)*self.gridSize
        return (x,y)

    # Fixes some TK issue with off-center circles
    def to_screen2(self, point):
        (x,y) = point
        # y = self.height - y
        x = (x + 1)*self.gridSize
        y = (self.height - y)*self.gridSize
        return (x,y)

    def drawPacman(self, pacman, index):
         position = self.getPosition(pacman)
         #print("drawPacman: position: %s" % str(position))
         screen_point = self.to_screen(position)
         endpoints = self.getEndpoints(self.getDirection(pacman))

         width = PACMAN_OUTLINE_WIDTH
         outlineColor = PACMAN_COLOR
         fillColor = PACMAN_COLOR

         return [circle(screen_point, PACMAN_SCALE * self.gridSize,
                        fillColor = fillColor, outlineColor = outlineColor,
                        endpoints = endpoints,
                        width = width)]

    def getEndpoints(self, direction, position=(0,0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi * pos)

        delta = width / 2
        if (direction == 'West'):
            endpoints = (180+delta, 180-delta)
        elif (direction == 'North'):
            endpoints = (90 + delta, 90 - delta)
        elif (direction == 'South'):
            endpoints = (270+delta, 270-delta)
        else:
            endpoints = (0+delta, 0-delta)
        return endpoints

    #def drawGhost(self, ghost, agentIndex):
        #pos = self.getPosition(ghost)

    def getPosition(self, agentState):
        if agentState.configuration == None:
            return (-1000, -1000)
        return agentState.getPosition()

    def getDirection(self, agentState):
        if agentState.configuration == None:
            return Directions.STOP
        return agentState.configuration.getDirection()

def add(x, y):
    return (x[0] + y[0], x[1] + y[1])

if __name__ == '__main__':
	layout = getLayout('tinyMaze')
	state = GameState()
	state.initialize(layout, 0)
	display = PacmanGraphics()
	display.initialize(state)
	sleep(2)
