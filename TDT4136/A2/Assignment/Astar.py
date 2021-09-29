import math
#f(n) = g(n) + h(n) where g(n) is the path cost from intial state to node n, and h(n) is the estimated cost to the goal

def heuristic_func(curr_pos, goal_pos):
    # Ty Pythagoras
    return math.sqrt(abs(curr_pos[0] - goal_pos[0])**2 + abs(curr_pos[1] - goal_pos[1])**2)

class Node():
    def __init__(self, pos, edges = [], g_cost=0):
        self.pos = pos
        self.edges = edges
        self.prev_node = None
        self.g_cost = g_cost
    
    def add_edge(self, edge_to_add, weight):
        #print("Adding edge")
        self.edges.append(Edge(edge_to_add, weight))

    # pos is a tuple of x,y coordinates
    # returns a tuple with a boolean and weight of edge between nodes
    def node_is_neighbour(self, pos_of_node):
        # Node is below or above self
        if(self.pos[0] == pos_of_node[0] and (self.pos[1] + 1 == pos_of_node[1] or self.pos[1] - 1 == pos_of_node[1])):
            return (True, 1)
        # Node is left or right of self
        elif(self.pos[1] == pos_of_node[1] and (self.pos[0] + 1 == pos_of_node[0] or self.pos[0] - 1 == pos_of_node[0])):
            return (True, 1)
        
        return (False, -1)

    def to_string(self):
        return "Node at pos (%d, %d) with g-cost %d" % (self.pos[0], self.pos[1], self.g_cost)

    def print_all_edges(self):
        for edge in self.edges:
            print(self.to_string(), " || ", edge.to_string())

class Edge():
    def __init__(self, target_node, weight):
        self.target = target_node
        self.weight = weight
    def to_string(self):
        return self.target.to_string(), "with weight", self.weight

class PriorityQueue():
    def __init__(self, eval_func):
        self.queue = []
        self.eval = eval_func

    def add_element(self, element_to_add):
        # Insert element such that the queue stays in prioritized order
        if(len(self.queue) > 0):
            for i, node in enumerate(self.queue):
                if(node.g_cost + self.eval(node) > element_to_add.g_cost + self.eval(element_to_add)):
                    self.queue.insert(i, element_to_add)
            
        else:
            self.queue.append(element_to_add)

    def remove_element(self, element_to_remove):
        # Find element and remove it
        if(len(self.queue) > 0):
            print("Cannot remove element since queue is empty")
            return False
        else:
            for i, node in enumerate(self.queue):
                elements_are_identical = True
                for key in node.keys():
                    if(node[key] != element_to_remove[key]):
                        elements_are_identical = False
                if(elements_are_identical):
                    self.queue.pop(i)
                    return True
        print("Couldn't find element to remove")
        return False
        
    def to_string(self):
        output = "Queue:\n"
        for node in self.queue:
            output += "Node at pos: (%d, %d) with %d edges.\n" % (node.pos[0],node.pos[1], len(node.edges))
        return output

class A_star_solver():
    # -1 in map is non-traversable tile, 1 is traversable tile, 2 is start pos, 3 is end pos
    def __init__(self, map):
        self.prio_queue = PriorityQueue(heuristic_func)
        self.map_obj = map
        self.map = map.get_maps()[0]
        map.print_map(map.get_maps()[0])

        self.nodes = []
        # Create every valid node in map and store it in self.nodes
        for i in range(len(self.map[0])):
            for j in range(len(self.map)):
                if(self.map[j][i] != -1):
                    node = Node((i,j))
                    self.nodes.append(node)
                    if (self.map[j][i] == 2):
                        self.start_node = node
                    elif (self.map[j][i] == 3):
                        self.end_node = node
        #print(len(self.nodes))

        # Fill in edges for each node
        for node in self.nodes:
            for potential_neighbour in self.nodes:
                is_neighbour, weight = node.node_is_neighbour(potential_neighbour.pos)
                if(is_neighbour):
                    print(node.to_string(), " is adding ", potential_neighbour.to_string(), "as a neighbour")
                    node.add_edge(potential_neighbour, weight)
            print(node.edges[0].to_string(), len(node.edges))
        #print(type(self.start_node))
        #self.start_node.print_all_edges()
        self.prio_queue.add_element(self.start_node)
        print(self.prio_queue.to_string())





