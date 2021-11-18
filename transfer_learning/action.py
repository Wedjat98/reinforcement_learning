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

    def set_possibility(self, direction, possibility):
        self.possibility = possibility
        self.direction = direction

    def update_q_value(self, no, r, state, qtable_t, x_next, y_next, action, x, y, qtable_c, delta):
        alpha = const.LEARNING_RATE
        gamma = const.DISCOUNT_RATE
        '''
        gamma = delta[x][y]-0.1
        if gamma < 0:
            gamma = 0
        '''
        max_action = state[y_next][x_next].get_max_q_action(qtable_t, x_next, y_next).d
        max_q = qtable_t[x_next][y_next][max_action]
        qtable_t[x][y][action] = qtable_t[x][y][action] + alpha * (r + gamma * max_q - qtable_t[x][y][action])

        '''
        if const.MAX_qtable_t <= qtable_t[x][y][action]:
            const.MAX_qtable_t = qtable_t[x][y][action]
            #print(const.MAX_qtable_t)


        if delta[x_next][y_next] == 0 and const.EPISODE_Agent1 != 1:
            max_action = state[y_next][x_next].get_max_q_action(qtable_c,x_next,y_next).d
            max_q = qtable_c[x_next][y_next][max_action]
            qtable_t[x][y][action] = qtable_t[x][y][action] + alpha*(r + gamma*max_q - qtable_t[x][y][action]) 

            if max_action == 0:
                x_next = x_next-1
            elif max_action == 1:
                x_next = x_next+1
            elif max_action == 2:
                y_next = y_next-1
            elif max_action == 3:
                y_next = y_next+1

            if x == x_next and y == y_next:
                pass
            else:
                max_action = state[y_next][x_next].get_max_q_action(qtable_c,x_next,y_next).d
                max_q = qtable_c[x_next][y_next][max_action]
                qtable_t[x][y][action] = qtable_t[x][y][action] + alpha*(r + gamma*max_q - qtable_t[x][y][action]) 
         '''