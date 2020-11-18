
import numpy as np
import cv2
import time


TILE_SIZE = 32
OFS = 50

MARKET = """
##################
##..............##
#D..jd..on..sb..m#
#j..Do..dn..sp..b#
#D..jd..on..se..t#
#j..Do..dn..se..r#
#D..jd..on..sf..a#
##...............#
##..Cg..Cg..Cg...#
##..##..##..##...#
##...............#
##############GG##
""".strip()


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tile   : a numpy array containing the tile image
        """
        self.tiles = tiles
        self.contents = [list(row) for row in layout.split('\n')]
        self.xsize =  len(self.contents[0])
        self.ysize = len(self.contents)
        self.image = np.zeros((self.ysize * TILE_SIZE, self.xsize * TILE_SIZE, 3), dtype=np.uint8)
        self.prepare_map()
    

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == '#':
            return self.tiles[0:32, 0:32]
        elif char == 'G':
            return self.tiles[7*32:8*32, 3*32:4*32]
        elif char == 'C':
            return self.tiles[2*32:3*32, 8*32:9*32]
        elif char == 'b':
            return self.tiles[1*32-32:1*32, 5*32-32:5*32]
        elif char == 'm': # melon
            return self.tiles[4*32-32:4*32, 5*32-32:5*32]
        elif char == 't': #grapes
            return self.tiles[5*32-32:5*32, 5*32-32:5*32]
        elif char == 'r': #strawberry
            return self.tiles[2*32-32:2*32, 6*32-32:6*32]
        elif char == 'a': #apple
            return self.tiles[2*32-32:2*32, 5*32-32:5*32]
        elif char == 'p': #pineapple
            return self.tiles[6*32-32:6*32, 5*32-32:5*32]
        elif char == 'e': #cherry
            return self.tiles[8*32-32:8*32, 5*32-32:5*32]
        elif char == 'f': #peach
            return self.tiles[3*32-32:3*32, 5*32-32:5*32]
        elif char == 'd':    #dairy
            return self.tiles[7*32-32:7*32, 13*32-32:13*32]
        elif char == 'D': #drinks
            return self.tiles[7*32-32:7*32, 14*32-32:14*32]
        elif char == 'j': #cocktail
            return self.tiles[4*32-32:4*32, 14*32-32:14*32]
        elif char == 's': #spices
            return self.tiles[2*32-32:2*32, 4*32-32:4*32]
        elif char == 'n': #basil
            return self.tiles[3*32-32:3*32, 4*32-32:4*32]
        elif char == 'g': #cashier
            return self.tiles[8*32-32:8*32, 1*32-32:1*32]
        elif char == 'o': #cake
            return self.tiles[6*32-32:6*32, 7*32-32:7*32]
        else:
            return self.tiles[32:64, 64:96]

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                bm = self.get_tile(tile)
                self.image[y * TILE_SIZE:(y+1)*TILE_SIZE,
                      x * TILE_SIZE:(x+1)*TILE_SIZE] = bm

    def draw(self, frame, offset=OFS):
        """
        draws the image into a frame
        offset pixels from the top left corner
        """
        frame[OFS:OFS+self.image.shape[0], OFS:OFS+self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)



class Customer:

    def __init__(self, supermarketmap, image, dead, x, y, alive):
        """
        supermarketmap : an instance of the SupermarketMap class
        image : a numpy array containing the customer's image
        dead: a numpy array containing the background of the supermarket image
        x: the start x coordinate of the customer on the map
        y: the start y coordinate of the customer on the map
        alive: true if the customer is in the supermarket 
        """
        self.supermarketmap = supermarketmap
        self.image = image
        self.x = x
        self.y = y
        self.alive = alive 
        self.dead = dead

    def draw(self, frame):
        """draws the customer on the map"""

        xpos = OFS + self.x * TILE_SIZE
        ypos = OFS + self.y * TILE_SIZE
    
        if self.alive == True:
            frame[ypos:ypos+self.image.shape[0], xpos:xpos + self.image.shape[1]] = self.image
        else:
            frame[ypos:ypos+self.image.shape[0], xpos:xpos + self.image.shape[1]] = self.dead 

    def move(self, direction):
        """moves the customer on the map one step at a time depending on direction
        direction: up, down, left, or right
        """
        newx = self.x
        newy = self.y
        if direction == 'up':
            newy -= 1
        
        if direction == 'down':
            newy += 1
            
        if direction == 'right':
            newx += 1
        
        if direction == 'left':
            newx -= 1
            
        if self.supermarketmap.contents[newy][newx] == '.':
            #avoids the costumer to walk on walls or shelves
            self.x = newx
            self.y = newy
    
    def next_step(self):
        newx =  self.x      # global variables are dirty programming
        newy = self.y      # but its a prototype
        global path
        global target
        dx, dy = path.pop(0)
        newx += dx
        newy += dy
        time.sleep(0.2)

        if len(path) == 0:
            time.sleep(1)
            # set new target
            if target == 'spices':
                path = PATH_SP_EXIT[:]
                target = 'exit'
            else:
                path = PATH_DR_SP[:]
                target = 'spices'
        
        if self.supermarketmap.contents[newy][newx] == '.':
            self.x = newx
            self.y = newy
        
        
    
    def next_step_paths(self):
        ''' 
        This function gets a list of targets from the MCMC
        Then, we find the path to the first target, move to the path, and continue like this
        ''' 
        global path
        global target_list 

        newx =  self.x      # global variables are dirty programming
        newy = self.y      # but its a prototype
        # target = target_list.pop(0)
        # path = getpath from the A* algorithm for the target 
        # the path_list is useless once we have the A* stuff
        if len(path) != 0: 
            coord_now = path.pop(0)
            if len(path) != 0:

                # # set new target
                # target_list.pop(0)

                # if len(target_list) == 0:
                #     time.sleep(3)
                #     # a path that goes to the exit with A* 
                if len(path) == 1:
                    time.sleep(0.2)

                else: 
                    coord_next = path[0]
                    dx = coord_next[1] - coord_now[1]
                    dy = coord_next[0] - coord_now[0]
                    newx += dx
                    self.x = newx
                    newy += dy
                    self.y = newy 
                    time.sleep(0.2)


            # path = new path for this target with the A* algorithm 
            # else: 
            #     path = path_list.pop(0)[:]

        
        if self.supermarketmap.contents[newy][newx] == '.':
            self.x = newx
            self.y = newy


    def move_location(self, path):
        newx = self.x
        newy = self.y

        if path == 'PATH_DR_SP':
            for _ in range(3):
                newy -= 1
                self.y = newy
                time.sleep(0.2)
                market.draw(frame)
                self.draw(frame) 
                cv2.imshow('frame', frame)
            
            for _ in range(8):
                newx += 1
                self.x = newx  
                time.sleep(0.2)
                market.draw(frame)
                self.draw(frame) 
                cv2.imshow('frame', frame)
            
            for _ in range (3):
                newy += 1
                self.y = newy
                time.sleep(0.2)
                market.draw(frame)
                self.draw(frame) 
                cv2.imshow('frame', frame)
    
    
    #def __repr__(self):
        #return f'Customer is on the map {self.supermarketmap} and looks like the image {self.image} is on position x = {self.x} and y = {self.y}'


background = np.zeros((700, 1000, 3), np.uint8)
tiles = cv2.imread('pictures/tiles.png')

market = SupermarketMap(MARKET, tiles)

pacman = tiles[96:96+32, 0:32]
dead = tiles[0:32, 4:36]

cust1 = Customer(market, pacman, dead , 15, 10, True)


path_list = [[(10, 15),
   (9, 15),
   (8, 15),
   (7, 15),
   (7, 14),
   (7, 13),
   (7, 12),
   (7, 11),
   (7, 10),
   (7, 9),
   (7, 8),
   (7, 7),
   (6, 7),
   (5, 7),
   (4, 7),
   (4, 6)],
  [(4, 6)],
  [(4, 6), (4, 7)],
  [(4, 7), (4, 6)],
  [(4, 6), (4, 7)],
  [(4, 7)],
  [(4, 7), (4, 6)],
  [(4, 6), (4, 7)],
  [(4, 7), (4, 6)],
  [(4, 6)],
  [(4, 6), (4, 7)],
  [(4, 7), (4, 6)],
  [(4, 6), (4, 7)],
  [(4, 7), (4, 6)],
  [(4, 6)],
  [(4, 6)],
  [(4, 6)],
  [(4, 6)],
  [(4, 6)],
  [(4, 6), (4, 7)],
  [(4, 7)],
  [(4, 7), (4, 6)],
  [(4, 6), (4, 7)],
  [(4, 7), (4, 6)],
  [(4, 6), (4, 7)],
  [(4, 7)],
  [(4, 7), (4, 6)],
  [(4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (8, 7)],
  [(8, 7),
   (9, 7),
   (10, 7),
   (10, 8),
   (10, 9),
   (10, 10),
   (10, 11),
   (10, 12),
   (10, 13),
   (10, 14),
   (10, 15)]]



while True:

    while len(path_list) != 0:

        path = path_list[0][:]
            
        while len(path) != 0:
            frame = background.copy()
            market.draw(frame)

            cust1.draw(frame) 

            cv2.imshow('frame', frame)

            key = chr(cv2.waitKey(1) & 0xFF)
            
            if key == 'q':
                break

            cust1.next_step_paths()
            time.sleep(0.1)

        path_list.pop(0)

    if len(path_list) == 0: 
            
        cust1.alive = False
        frame = background.copy()
        market.draw(frame)

        cv2.imshow('frame', frame)

        key = chr(cv2.waitKey(1) & 0xFF)
            
        if key == 'q':
            break



        

cv2.destroyAllWindows()





















