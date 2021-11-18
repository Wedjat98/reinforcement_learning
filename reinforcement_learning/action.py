import const

class Action:
    def __init__(self, direction, possibility):
        self.q_value = 0.00
        self.possibility = possibility
        self.direction = direction

    def getd(self):
        return self.direction
    def setd(self, value):
        self.direction = value
    d = property(getd, setd)
    
    def getp(self):
        return self.possibility
    def setp(self, value):
        self.possibility = value
    p = property(getp, setp)

    def set_possibility(self,direction,possibility):
        self.possibility = possibility
        self.direction = direction
    
    def update_q_value(self,no,r,state,qtable,x1,y1,action,xx1,yy1):
        alpha = const.LEARNING_RATE
        gamma = const.DISCOUNT_RATE
        max_action = state.get_max_q_action(qtable,x1,y1).d
        #print (max_action)
        max_q = qtable[x1][y1][max_action]
        #print (max_q)
        #print(qtable[x1][y1][x2][y2][x3][y3][action])
        #print(x1)
        #print(y1)
        #print(x2)
        #print(y2)
        #print(x3)
        #print(y3)
        #print(action)
        #print(max_q)
        qtable[xx1][yy1][action] = qtable[xx1][yy1][action] + alpha*(r + gamma*max_q - qtable[xx1][yy1][action])    
        
        #if qtable[xx1][yy1][xx2][yy2][xx3][yy3][action] >= 50:
            #print("q=" + str(qtable[xx1][yy1][xx2][yy2][xx3][yy3][action]))
            