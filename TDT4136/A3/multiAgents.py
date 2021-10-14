# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    n_ghosts = 0

    def getAction(self, gameState):

        self.n_ghosts = gameState.getNumAgents() - 1
        
        def minimax(state, depth, is_maximizer):
            # Because these guys apparently like fake depth, self.depth is not the amount of layers
            # But the amount of times we need to do n layers
            if(depth == self.depth*(self.n_ghosts+1) or state.isWin() or state.isLose()):
                return [self.evaluationFunction(state), None]
            
            if(is_maximizer):
                #print("pacman can do", state.getLegalActions(0))
                curr_val = -9999999
                best_move = None
                # Maximizing layer, so we know we're pacman
                agent_num = 0
                for possible_move in state.getLegalActions(0):
                    move_val = minimax(state.generateSuccessor(0, possible_move), depth+1, False)[0]
                    
                    if(move_val > curr_val):
                        curr_val = move_val
                        best_move = possible_move

                return [curr_val, best_move]
            # Minimizing layer, ghost
            else:
                curr_val = 9999999
                best_move = None
                # Figure out which ghost we are
                agent_num = (self.depth-(self.depth-depth)) % (self.n_ghosts+1)
                legal_moves = state.getLegalActions(agent_num)
                for possible_move in legal_moves:
                    if(agent_num == self.n_ghosts):
                        # Next layer is maximizing (pacman)
                        move_val = minimax(state.generateSuccessor(agent_num, possible_move), depth+1, True)[0]
                        if(move_val < curr_val):
                            curr_val = move_val
                            best_move = possible_move

                    else:
                        # Next layer is still minimizing (another ghost)
                        move_val = minimax(state.generateSuccessor(agent_num, possible_move), depth+1, False)[0]
                        if(move_val < curr_val):
                            curr_val = move_val
                            best_move = possible_move
                        
                return [curr_val, best_move]

        best_score, best_move = minimax(gameState, 0, True)
        return best_move
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    n_ghosts = 0

    def getAction(self, gameState):
        self.n_ghosts = gameState.getNumAgents() - 1

        def minimax_ab(state, depth, is_maximizer, alpha, beta):
            if(depth == self.depth*(self.n_ghosts+1) or state.isWin() or state.isLose()):
                return [scoreEvaluationFunction(state), None]
            
            if(is_maximizer):
                #print("pacman can do", state.getLegalActions(0))
                curr_val = -9999999
                best_move = None
                # Maximizing layer, so we know we're pacman
                agent_num = 0
                for possible_move in state.getLegalActions(0):
                    move_val = minimax_ab(state.generateSuccessor(0, possible_move), depth+1, False, alpha, beta)[0]
                    
                    if(move_val > curr_val):
                        curr_val = move_val
                        best_move = possible_move

                    alpha = max(alpha, move_val)
                    if(beta < alpha):
                        break

                return [curr_val, best_move]
            # Minimizing layer, ghost
            else:
                curr_val = 9999999
                best_move = None
                # Figure out which ghost we are
                agent_num = (self.depth-(self.depth-depth)) % (self.n_ghosts+1)
                legal_moves = state.getLegalActions(agent_num)
                for possible_move in legal_moves:
                    if(agent_num == self.n_ghosts):
                        # Next layer is maximizing (pacman)
                        move_val = minimax_ab(state.generateSuccessor(agent_num, possible_move), depth+1, True, alpha, beta)[0]
                        if(move_val < curr_val):
                            curr_val = move_val
                            best_move = possible_move

                        beta = min(beta, move_val)
                        if(beta < alpha):
                            break
                    else:
                        # Next layer is still minimizing (another ghost)
                        move_val = minimax_ab(state.generateSuccessor(agent_num, possible_move), depth+1, False, alpha, beta)[0]
                        if(move_val < curr_val):
                            curr_val = move_val
                            best_move = possible_move

                        beta = min(beta, move_val)
                        if(beta < alpha):
                            break
                           
                return [curr_val, best_move]

        best_score, best_move = minimax_ab(gameState, 0, True, -9999999, 9999999)
        return best_move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
