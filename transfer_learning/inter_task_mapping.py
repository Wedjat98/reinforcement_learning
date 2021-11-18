import const
import csv

CS = const.CS
NUM_ROW = int(const.SCR_X / CS)
NUM_COL = int(const.SCR_Y/ CS)
ACTION = 5

class Inter_task_mapping:

    def __init__(self):
        pass

    def inter_mapping(self,qtable,qtable_c,qtable_s):
        o = open('q_table(source).csv', 'r')
        dataReader = csv.reader(o)

        for row in dataReader:
            qtable.append(float(row[3]))

        self.count_qtable = 0
        for x in range(1,const.S_NUM_ROW+1):
            for y in range(1,const.S_NUM_COL+1):
                for action in range(ACTION):
                    
                    #self.qtable_c[x][y][action] = const.TRANCE_RATE*self.qtable[self.count_qtable]
                    qtable_s[x][y][action] = qtable[self.count_qtable]
                    self.count_qtable = self.count_qtable + 1

        for x in range(1,const.T_NUM_ROW+1):
            for y in range(1,const.T_NUM_COL+1):
                for action in range(ACTION):
                    try:
                        qtable_c[x][y][action] = const.TRANCE_RATE*qtable_s[x][y][action]
                        #print(self.qtable_c[x][y][action]) 
                    except IndexError:
                        print("exception")


    def inter_mapping2(self,qtable,qtable_c,qtable_s):
        o = open('q_table(source).csv', 'r')
        dataReader = csv.reader(o)

        for row in dataReader:
            qtable.append(float(row[3]))

        self.count_qtable = 0
        for x in range(1,const.S_NUM_ROW+1):
            for y in range(1,const.S_NUM_COL+1):
                for action in range(ACTION):
                    if action == 0:
                        #qtable_c[x][y][action] = ((qtable[self.count_qtable] + qtable[self.count_qtable+2]) /2) *const.TRANCE_RATE
                        qtable_s[x][y][action] = (qtable[self.count_qtable] + qtable[self.count_qtable+2]) /2

                    if action == 1:
                        #qtable_c[x][y][action] = ((qtable[self.count_qtable] + qtable[self.count_qtable+2]) /2) *const.TRANCE_RATE
                        qtable_s[x][y][action] = (qtable[self.count_qtable] + qtable[self.count_qtable+2]) /2

                    if action == 2:
                        #qtable_c[x][y][action] = ((qtable[self.count_qtable] + qtable[self.count_qtable-1]) /2) *const.TRANCE_RATE
                        qtable_s[x][y][action] = (qtable[self.count_qtable] + qtable[self.count_qtable-1]) /2

                    if action == 3:
                        #qtable_c[x][y][action] = ((qtable[self.count_qtable] + qtable[self.count_qtable-3]) /2) *const.TRANCE_RATE
                        qtable_s[x][y][action] = (qtable[self.count_qtable] + qtable[self.count_qtable-3]) /2

                    if action == 4:
                        #qtable_c[x][y][action] = const.TRANCE_RATE*qtable[self.count_qtable]
                        qtable_s[x][y][action] = qtable[self.count_qtable]
                    
                    self.count_qtable = self.count_qtable + 1
                  
        for x in range(1,const.T_NUM_ROW+1):
            for y in range(1,const.T_NUM_COL+1):
                for action in range(ACTION):
                    try:
                        qtable_c[x][y][action] = const.TRANCE_RATE*qtable_s[x][y][action]
                        #print(self.qtable_c[x][y][action]) 
                    except IndexError:
                        print("exception")
