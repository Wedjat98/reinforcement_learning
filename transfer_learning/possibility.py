
START = 0
GOAL = 1
ROAD = 2
WALL = 3
ROBOT = 4
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
STOP = 4
    
class Possibility:    
    
    def __init__(self):
        pass
        
    def set_possibility(self,y,x,state,field):
        
        N_WALL = [ROAD,START,GOAL]
        N_WALL2 = [ROAD,START,GOAL,ROBOT]

        if field[y][x].k in N_WALL2:
            if field[y][x-1].k in N_WALL:
                state[y][x].set_action(LEFT,True)
            if field[y][x+1].k in N_WALL:
                state[y][x].set_action(RIGHT,True)
            if field[y-1][x].k in N_WALL:
                state[y][x].set_action(UP,True)
            if field[y+1][x].k in N_WALL:
                state[y][x].set_action(DOWN,True)
        state[y][x].set_action(STOP,True)

    
    def set_all_possibility(self,state,row,col,field):
        
        for y in range(1,row):
            for x in range(1,col):
                Possibility.set_possibility(self,y,x,state,field)

    
    def now_possibility(self,y,x,state,field,number):
        
        N_WALL = [ROAD,START,GOAL]
        N_WALL2 = [ROAD,START,GOAL,ROBOT]
        ALL_WALL = [WALL,ROBOT]

        if number == 1:
            if field[y][x].k in N_WALL2:
                if field[y][x-1].k in N_WALL:
                    state[y][x].set_action(LEFT,True)
                if field[y][x-1].k == ROBOT:
                    state[y][x].set_action(LEFT,False)
                if field[y][x+1].k in N_WALL:
                    state[y][x].set_action(RIGHT,True)
                if field[y][x+1].k == ROBOT:
                    state[y][x].set_action(RIGHT,False)
                if field[y-1][x].k in N_WALL:
                    state[y][x].set_action(UP,True)
                if field[y-1][x].k == ROBOT:
                    state[y][x].set_action(UP,False)
                if field[y+1][x].k in N_WALL:
                    state[y][x].set_action(DOWN,True)
                if field[y+1][x].k == ROBOT:
                    state[y][x].set_action(DOWN,False)
                     
        if number == 2:
            if field[y][x].k in N_WALL2:
                if field[y-1][x-1].k in N_WALL:
                    state[y][x].set_action(LEFT,True)
                if field[y-1][x-1].k in ALL_WALL:
                    state[y][x].set_action(LEFT,False)
                if field[y+1][x+1].k in N_WALL:
                    state[y][x].set_action(RIGHT,True)
                if field[y+1][x+1].k in ALL_WALL:
                    state[y][x].set_action(RIGHT,False)
                if field[y-1][x+1].k in N_WALL:
                    state[y][x].set_action(UP,True)
                if field[y-1][x+1].k in ALL_WALL:
                    state[y][x].set_action(UP,False)
                if field[y+1][x-1].k in N_WALL:
                    state[y][x].set_action(DOWN,True)
                if field[y+1][x-1].k in ALL_WALL:
                    state[y][x].set_action(DOWN,False)


