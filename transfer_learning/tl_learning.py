import const
import state

class TL_learning:

    def __init__(self):
        pass

    def tl_update_q(self,qtable_c,qtable_s,qtable_t,x,y,action,delta,state):
        #self.delta = 1 - delta[x][y] - state[y][x].get_max_q_action_return_q(qtable_t,x,y)
        self.delta = 1 - delta[x][y]

        if self.delta < 0:
           self.delta = 0

        '''
        delta_a = qtable_t[x][y][action] + delta[x][y]
        if delta_a > 1:
           delta_a = 1
        self.delta = 1 - delta_a
        #print(self.delta)
        '''
        self.tau = const.TRANCE_RATE
        #qtable_c[x][y][action] = qtable_t[x][y][action] + self.tau * self.delta * qtable_s[x][y][action]

        for action_no in range(const.Action_no):
            qtable_c[x][y][action_no] = (1-self.delta)*qtable_t[x][y][action_no] +  self.tau*self.delta * qtable_s[x][y][action_no]


    def delta_rl(self,x,y,x_next,y_next,qtable_c,state,delta):
        max_action = state[y][x].get_max_q_action(qtable_c,x,y).d
        max_action_next =  state[y_next][x_next].get_max_q_action(qtable_c,x_next,y_next).d
        #"""忘却手法
        if qtable_c[x][y][max_action] >= qtable_c[x_next][y_next][max_action_next]:
            delta[x][y] = delta[x][y] + 0.1*(1-delta[x][y])
            #print(delta[x][y])
        #"""
