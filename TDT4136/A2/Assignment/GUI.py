import pygame as pg;

from Astar import A_star_solver;
from Map import Map_Obj;

class GUI():
    def __init__(self, task, window_size):
        # Tuple containing window size in x and y
        self.task = int(task)
        # Set up our map object
        self.map = Map_Obj()
        self.map.fill_critical_positions(self.task)
        # Fill in start and goal pos
        self.map.set_cell_value(self.map.start_pos, 2, False)
        self.map.set_cell_value(self.map.goal_pos, 3, False)

        # Tuple containing the number of cells in the grid in x- and y-direction
        self.nOfCells = (len(self.map.get_maps()[0][0]), len(self.map.get_maps()[0]))

        #print("Map dimensions:", self.nOfCells)
        #print(self.map.get_maps()[0])
        #self.map.show_map(self.map.get_maps()[1])

        self.window_size = (self.closestNumber(window_size[0], self.nOfCells[0]), self.closestNumber(window_size[1], self.nOfCells[1]))

        # Pixel size of border around cells in the grid
        self.border_size = 0

        astar = A_star_solver(self.map)

    def run(self):
        pg.init()
        surface = pg.display.set_mode((self.window_size[0], self.window_size[1]))
        pg.display.set_caption("A*")
        clock = pg.time.Clock()
        horizontal_cell_size = self.window_size[0] // self.nOfCells[0]
        vertical_cell_size = self.window_size[1] // self.nOfCells[1]
        
        

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            # Draw black background
            background = pg.Rect(0, 0, self.window_size[0], self.window_size[1])
            pg.draw.rect(surface, (50, 50, 50), background)

            for x in range(self.nOfCells[0]):
                for y in range(self.nOfCells[1]):  
                    # Draw rectangles spaced apart by self.border_size
                    rect = pg.Rect(x*horizontal_cell_size+self.border_size, y*vertical_cell_size+self.border_size, horizontal_cell_size-2*self.border_size, vertical_cell_size-2*self.border_size)
                    
                    
                    rgb = (255,255,255)
                    cell_val = self.map.get_cell_value((y,x))
                   
                    if(cell_val == -1):
                        rgb = (211,33,45)
                    elif(cell_val == 1):
                        rgb = (215,215,215)
                    elif(cell_val == 2):
                        rgb = (255,0,255)
                    elif(cell_val == 3):
                        rgb = (0,128,255)
                    elif(cell_val == 4):
                        rgb = (255,255,0)

                    pg.draw.rect(surface, rgb, rect)

            pg.display.update()
            clock.tick(10)
    
    # Source: https://www.geeksforgeeks.org/find-number-closest-n-divisible-m/
    # It's purpose is to round the window size to the closest number to the user input which is divisible by the amount of cells in the map
    def closestNumber(self, n, m) :
        # Find the quotient
        q = int(n / m)
        
        # 1st possible closest number
        n1 = m * q
        
        # 2nd possible closest number
        if((n * m) > 0) :
            n2 = (m * (q + 1))
        else :
            n2 = (m * (q - 1))
        
        # if true, then n1 is the required closest number
        if (abs(n - n1) < abs(n - n2)) :
            return n1
        
        # else n2 is the required closest number
        return n2

if __name__ == '__main__':
    
    validTask = False
    while not validTask:
        task = input("What task are you solving?\n")
        if(task == "1" or task == "2" or task == "3"):
            validTask = True

    gui = GUI(task, (650,800))
    gui.run()

    
    


    
    





