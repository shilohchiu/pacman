"""Contains constant definitions"""
# from constants.wall_constants import MAZE_WIDTH

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720

MAZE_WIDTH = 530 # includes the 20 pixels of tiles
MAZE_HEIGHT = 580 # includes the 20 pixels of tiles

PLAYER_MOVEMENT_SPEED = 2
PACMAN_SPAWN_COORD = (355, 210)

GHOST_CENTER_X, GHOST_CENTER_Y = (355, 385)
GHOST_WIDTH = 30
GHOST_SCALE = 1.5

FRUIT_POSITION = (WINDOW_WIDTH/2, 330)

FRUIT_DATA ={
    "error":{
        "levels":[0],
        "point": 100,
        "image": 'images/fruit/error.jpg'
    },
    "cherry":{
        "levels":[1],
        "point": 100,
        "image": 'images/fruit/cherry.png'
    },
    "strawberry":{
        "levels":[2],
        "point": 300,
        "image": 'images/fruit/strawberry.png'
    },
    "peach":{
        "levels":[3,4],
        "point": 500,
        "image": 'images/fruit/peach.png'
    },
    "apple":{
        "levels":[5,6],
        "point": 700,
        "image": 'images/fruit/apple.png'
    },
    "grape":{
        "levels":[7,8],
        "point": 1000,
        "image": 'images/fruit/grape.png'
    },
    "galaxian":{
        "levels":[9,10],
        "point": 2000,
        "image": 'images/fruit/galaxian.png'
    },
    "bell":{
        "levels":[11,12],
        "point": 3000,
        "image": 'images/fruit/bell.png'
    },
    "key":{
        "levels":[list(range(13,257))],
        "point": 5000,
        "image": 'images/fruit/key.png'
    }
}

H_DISTANCE_BETWEEN_EDGE_AND_MAZE = int((WINDOW_WIDTH - MAZE_WIDTH) / 2)



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

BLACK_BOX_Y_POSITION = int(WINDOW_HEIGHT / 2) + 30
COLLISION_BLACK_BOX_X_OFFSET_VAL = 1

SCREENWRAP_RIGHT_SIDE = 650
SCREENWRAP_LEFT_SIDE = 100

ONE_UP = 10000

PACMAN_NORMAL = "normal"
PACMAN_ATTACK = "attack"

GHOST_CHASE = "chase"
GHOST_FLEE = "flee"
GHOST_EATEN = "eaten"
GHOST_BLINK = "blink"

#TODO do we need both of the PIVOT_COL lists
PIVOT_COL = [115, 160, 165, 225, 285, 325, 355, 385, 425, 485, 545, 595]


# TOP HALF COL: 115, 225, 325, 385, 485, 595
# TOP HALF SPEC: 285, 425
# BOT HALF COL: 165, 545
# BOT HALF SPEC: 165, 545, 285, 425
PIVOT_ROW = [650, 580, 520, 460, 385, 330, 270, 210, 150, 90]

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
                    460: [(285, ("S", "E")),
                        (325, ("N", "E")),
                        (355, ("E", "W")),
                        (385, ("N", "W")),
                        (425, ("S", "W"))],
                    385: [(225, ("N", "S", "E", "W")),
                        (285, ("N", "S", "W")),
                        (325, ("N", "S", "W")),
                        (425, ("N", "S", "E")),
                        (485, ("N", "S", "E", "W"))],
                    330: [(285, ("N", "S", "E")),
                        (425, ("N", "S", "W"))],
                    270: [(115,("S", "E")), 
                        (225, ("N", "S", "E", "W")), 
                        (285, ("N", "E", "W")),
                        (325, ("S", "W")),
                        (385, ("S", "E")),
                        (425, ("N", "E", "W")),
                        (485, ("N", "S", "E", "W")),
                        (595, ("S", "W"))],
                    210: [(115,("N", "E")),
                        (165, ("S", "W")),
                        (225, ("N", "S", "E")), 
                        (285, ("S", "E", "W")),
                        (325, ("N", "E", "W")),
                        (355, ("E", "W")),
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

PACMAN_LIVES_SCALE = .4
PACMAN_LIVES_Y_POSITION = 40
PACMAN_FIRST_LIFE_X_POSITION = 110
PACMAN_FOURTH_LIFE_X_POSITION = 230
PACMAN_LIFE_X_POSITION_STRIDE = 40

PELLET_COL = [115,140,165,185,205,225,245,265,285,298,311,325,345,
              365,385,399,412,425,445,465,485,505,525,545,570,595]

PELLET_ROW = [87,107,127,147,167,187,207,227,247,267,290,312,335,358,
              381,403,426,449,471,494,517,537,557,577,595,612,630,647]

PELLET_SCALE = 0.75
