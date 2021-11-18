#!/usr/local/bin python
# -*- coding:utf-8 -+-
import math
import random
import const
from action import *
import random
from map import *
from field import *



class State:
    
    def __init__(self,kind):
        self.kind = kind
        self.action = [Action(0,False),Action(1,False),Action(2,False),Action(3,False),Action(4,False)]

    def set_action(self,direction,possibility):
        self.action[direction].set_possibility(direction,possibility)
    
    def get_max_q_action(self,qtable,x1,y1):
        m = max(range(len(self.action)), key=lambda i: qtable[x1][y1][i])   #最大の行動のQ値を見つける！
        if qtable[x1][y1][0] == 0.00 and qtable[x1][y1][1] == 0.00 and qtable[x1][y1][2] == 0.00 and qtable[x1][y1][3] == 0.00 and qtable[x1][y1][4] == 0.00:   #�e�s����Q�l��0�̏ꍇ
            m = random.randint(0,4)   #�����_����0~3�̐�����m�Ɋi�[����
            # while True:
            #     m = random.randint(0,3)
            #     if self.action[m].p!=False:
            #         break
        return self.action[m]
    
    def get_max_q_action_return_q(self,qtable,x1,y1):
        m = max(range(len(self.action)), key=lambda i: qtable[x1][y1][i])   #最大の行動のQ値を見つける！
        if qtable[x1][y1][0] == 0.00 and qtable[x1][y1][1] == 0.00 and qtable[x1][y1][2] == 0.00 and qtable[x1][y1][3] == 0.00 and qtable[x1][y1][4] == 0.00:   #�e�s����Q�l��0�̏ꍇ
            return 0
            #m = random.randint(0,4)   #�����_����0~3�̐�����m�Ɋi�[����
            # while True:
            #     m = random.randint(0,3)
            #     if self.action[m].p!=False:
            #         break
        return qtable[x1][y1][m]
    
    def get_max_q_prob(self,qtable,x1,y1,state):
        choosen = 0                  #ボルツマンによって選択された行動
        denom = 0                    #ボルツマンの分母
        prob = [0 for i in range(const.Action_no)] #それぞれの行動に対する確率
        posible_action = []
        max_prob = 0

        for act in range(const.Action_no):
            posible_action.append([act,qtable[x1][y1][act]])
        
        for act in range(len(posible_action)):
            no = posible_action[act]
            tmp = no[1] / const.T
            denom = math.exp(tmp) + denom

        for act in range(len(posible_action)):
            no = posible_action[act]
            tmp = no[1] / const.T
            prob[act] =  math.exp(tmp) / denom
            if max_prob < prob[act]:
                max_prob = prob[act]
                
        return max_prob
        
    def choose(self, candidates, probabilities):
        probabilities = [sum(probabilities[:x+1]) for x in range(len(probabilities))]
        """
        if probabilities[-1] > 1.0:
            #確率の合計が100%を超えていた場合は100％になるように調整する
            probabilities = [x/probabilities[-1] for x in probabilities]
        """
        rand = random.random()
        for candidate, probability in zip(candidates, probabilities):
            if rand < probability:
                return candidate
        #どれにも当てはまらなかった場合はNoneを返す
        return None

    def action_select(self,qtable,x1,y1,state):
        
        
        '''
        if const.T > 0.01:
            if const.EPISODE_Agent1 % 10 == 0 and const.Step_Agent1 == 1:
               const.T = const.T * 0.9
               print(const.T)
        '''
        
    #Boltzman---------------------------------------------------------------------------------------------------------
        choosen = 0                  #ボルツマンによって選択された行動
        denom = 0                    #ボルツマンの分母
        prob = [0 for i in range(const.Action_no)] #それぞれの行動に対する確率
        posible_action = []
        act_no = []
        prob_no = []

        for act in range(const.Action_no):
            if state.action[act].p == True:
                posible_action.append([act,qtable[x1][y1][act]])
        
        
        #すべての行動のQ値が0のとき
        '''
        if qtable[x1][y1][0] == 0.00 and qtable[x1][y1][1] == 0.00 and qtable[x1][y1][2] == 0.00 and qtable[x1][y1][3] == 0.00 and qtable[x1][y1][4] == 0.00:
            choosen = random.randint(0,4)
            return self.action[choosen]
        

        #取りうる行動のQ値が0でないとき
        '''
        #else:
        for act in range(len(posible_action)):
            no = posible_action[act]
            tmp = no[1] / const.T
            denom = math.exp(tmp) + denom
            act_no.append(act)

        for act in range(len(posible_action)):
            no = posible_action[act]
            tmp = no[1] / const.T
            prob[act] =  math.exp(tmp) / denom
            prob_no.append(prob[act])


        choosen = self.choose(act_no,prob_no)
        action = posible_action[choosen]
        action_no = action[0]

           # print(choosen,prob)

        return self.action[action_no]
        
    def action_select0(self):
        return self.action[0]
        
    def action_select1(self):
        return self.action[1]
    
    def action_select2(self):
        return self.action[2]
    
    def action_select3(self):
        return self.action[3]


