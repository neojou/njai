# pacman.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import GameStateData

class GameState:

    def __init__(self, prevState = None):
         if prevState != None:
             self.data = GameStateData(prevState.data)
         else:
             self.data = GameStateData()

    def initialize(self, layout, numGhostAgents=100):
        self.data.initialize(layout, numGhostAgents)
