import math
#f(n) = g(n) + h(n) where g(n) is the path cost from intial state to node n, and h(n) is the estimated cost to the goal

def heuristic_func(curr_pos, goal_pos):
    # Ty Pythagoras
    return math.sqrt(abs(curr_pos[0] - goal_pos[0])**2 + abs(curr_pos[1] - goal_pos[1])**2)

class Node():
    def __init__(self, pos, edges, g_cost=0):
        self.pos = pos
        self.edges = edges
        self.prev_node = None
        self.g_cost = g_cost

class PriorityQueue():
    def __init__(self, eval_func):
        self.queue = []
        self.eval = eval_func
    
    def add_element(self, element_to_add):
        if(len(self.queue) > 0):
            #check and sort by prio
            pass
        else:
            self.queue.append(element_to_add)
