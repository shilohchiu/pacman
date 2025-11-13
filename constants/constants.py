"""Contains constant definitions"""
# from constants.wall_constants import MAZE_WIDTH

PLAYER_MOVEMENT_SPEED = 2

CHARACTER_SCALE = 1.0

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720

MAZE_WIDTH = 530 # includes the 20 pixels of tiles
MAZE_HEIGHT = 580 # includes the 20 pixels of tiles

H_DISTANCE_BETWEEN_EDGE_AND_MAZE = int((WINDOW_WIDTH - MAZE_WIDTH) / 2)

PIVOT_COL = [115, 160, 165, 225, 285, 325, 385, 425, 485, 545, 595]
PIVOT_ROW = [645, 575, 515, 385, 270, 210, 150, 90]

BLACK_BOX_WIDTH = 50
# BLACK_BOX_RATIO = 0.75 # ratio describes collision box / actual box size 
# BLACK_BOX_SIZE = BLACK_BOX_RATIO // 1
# COLLISION_BLACK_BOX_SIZE = (BLACK_BOX_RATIO * BLACK_BOX_SIZE) // 1
BLACK_BOX_DISTANCE = MAZE_WIDTH + BLACK_BOX_WIDTH 
BLACK_BOX_X_POSITION_1 = int(H_DISTANCE_BETWEEN_EDGE_AND_MAZE / 2)
COLLISION_BLACK_BOX_X_POSITIONS =[BLACK_BOX_X_POSITION_1 - int(BLACK_BOX_WIDTH / 2),
                        BLACK_BOX_X_POSITION_1 + BLACK_BOX_DISTANCE + 10 + BLACK_BOX_WIDTH]
LARGE_BLACK_BOX_X_POSITIONS =[BLACK_BOX_X_POSITION_1 - 6,
                        BLACK_BOX_X_POSITION_1 + BLACK_BOX_DISTANCE + int(BLACK_BOX_WIDTH / 2) + 18]

# COLLISION_BLACK_BOX_X_POSITIONS =[]
BLACK_BOX_Y_POSITION = int(WINDOW_HEIGHT / 2) + 30
COLLISION_BLACK_BOX_X_OFFSET_VAL = 1

SCREENWRAP_RIGHT_SIDE = 650
SCREENWRAP_LEFT_SIDE = 100

# BLACK_BOX_X_POS_RIGHT = 
# BLACK_BOX_X_POS_LEFT =
# BLACK_BOX_Y_POS = 


PACMAN_NORMAL = "normal"
PACMAN_ATTACK = "attack"

GHOST_CHASE = "chase"
GHOST_FLEE = "flee"
GHOST_EATEN = "eaten"

PIVOT_COL = [115, 165, 225, 285, 325, 385, 425, 485, 545, 595]
# TOP HALF COL: 115, 225, 325, 385, 485, 595
# TOP HALF SPEC: 285, 425
# BOT HALF COL: 165, 545
# BOT HALF SPEC: 165, 545, 285, 425
PIVOT_ROW = [650, 580, 520, 385, 270, 210, 150, 90]
PIVOT_GRAPH = {650: [(115,("S", "E")), 
                        (225, ("S", "E", "W")), 
                        (325, ("S", "W")),
                        (385, ("S", "E")),
                        (485, ("S", "E", "W")),
                        (595, ("S", "W"))
                     ],
                    580: [(115,("N", "S", "E")), 
                        (225, ("N", "S", "E", "W")), 
                        (285, ("S", "E", "W")),
                        (325, ("N", "E", "W")),
                        (385, ("N", "E", "W")),
                        (425, ("S", "E", "W")),
                        (485, ("N", "S", "E", "W")),
                        (595, ("N", "S", "W"))],
                    520: [(115,("N", "E")), 
                        (225, ("N", "S", "W")), 
                        (285, ("N", "E")),
                        (325, ("S", "W")),
                        (385, ("S", "E")),
                        (425, ("N", "W")),
                        (485, ("N", "S", "E")),
                        (595, ("N", "W"))],
                    385: [(225, ("N", "S", "E", "W")),
                        (325, ("N", "S", "W")),
                        # PLACEHOLDER FOR TESTING START POSITION
                        (385, ("N", "S", "E", "W")),
                        (425, ("N", "S", "E")),
                        (485, ("N", "S", "E", "W"))],
                    270: [(115,("N", "E")), 
                        (225, ("N", "S", "E", "W")), 
                        (285, ("N", "E", "W")),
                        (325, ("S", "W")),
                        (385, ("S", "E")),
                        (425, ("N", "E", "W")),
                        (485, ("N", "S", "E", "W")),
                        (595, ("S", "W"))],
                    210: [(115,("N", "E")), 
                        (165, ("S", "W")),
                        (225, ("N", "S", "W")), 
                        (285, ("S", "E", "W")),
                        (325, ("N", "E", "W")),
                        (385, ("N", "E", "W")),
                        (425, ("S", "E", "W")),
                        (485, ("N", "S", "W")),
                        (545, ("S", "E")),
                        (595, ("N", "W"))],
                    150: [(115,("S", "E")), 
                        (165, ("N", "E", "W")),
                        (225, ("N", "W")), 
                        (285, ("N", "E")),
                        (325, ("S", "W")),
                        (385, ("S", "E")),
                        (425, ("N", "W")),
                        (485, ("N", "E")),
                        (545, ("N", "E", "W")),
                        (595, ("S", "W"))],
                    90: [(115,("N", "E")), 
                        (325, ("N", "E", "W")),
                        (385, ("N", "E", "W")),
                        (595, ("N", "W"))],
                }