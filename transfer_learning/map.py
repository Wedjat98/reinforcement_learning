#!/usr/local/bin python
# -*- coding:utf-8 -+-
import csv
import const
import pygame
from pygame.locals import *
import random
import sys
from state import *
from agent import *
from field import *
from const import *
from sensor import *
from possibility import *
from log import *
from inter_task_mapping import *

from tl_learning import *
from inter_task_mapping import Inter_task_mapping


SCR_RECT = Rect(0,0,const.SCR_X,const.SCR_Y+const.Text_Y)   #Rect(left,top,width,height)
CS = const.CS
NUM_ROW = int(const.SCR_X / CS)   # フィールドの行数11
NUM_COL = int(const.SCR_Y/ CS)  # フィールドの列数11
GLID = 49
EGENT = 1
ACTION = 5
START = 0
GOAL = 1
ROAD = 2
WALL = 3
ROBOT = 4
CS_COLOR = (255,255,255)
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
STOP = 4
DIREC = [LEFT,RIGHT,UP,DOWN]

FINISH_EPISODE = const.FINISH_EPISODE


'''---------------------------------------------short_pass_program---------------------------------------------'''
class Map:
    def __init__(self):   #初期化メソッド
        print('select agent')
        print('select1 plus')
        print('select2 xlos')
        self.agent_number = int(input('please input>>'))
        if self.agent_number == 1:
            self.agent = Agent1()    #agentという変数にｘとｙを追加（set getの部分を初期化している）
        elif self.agent_number == 2:
            self.agent = Agent2()
        else:
            print('not select agent')
        self.run = False
        self.possibility = Possibility()
        self.log = Log()
        self.tl_learning = TL_learning()
        self.trance = Inter_task_mapping()
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size)   #以下、self.名称はアトリビュートを追加
        pygame.display.set_caption(u"Target-Task")
        self.font = pygame.font.SysFont("timesnewroman",42)
        self.field = [[Field(GOAL)  for x in range(NUM_ROW)] for y in range(NUM_COL)]  #State(GOAL)はfieldクラスの呼び出し　fieldに対してk,rの変数を追加！←重要
        self.state_agent = [[State(GOAL) for x in range(NUM_ROW)] for y in range(NUM_COL)]
        self.qtable_c = [[[0 for action in range(ACTION)]for y1 in range(NUM_COL)] for x1 in range(NUM_ROW)]  #統合知識
        self.qtable_s = [[[0 for action in range(ACTION)]for y1 in range(S_NUM_COL+1)] for x1 in range(S_NUM_ROW+1)]  #source task
        self.qtable_t = [[[0 for action in range(ACTION)]for y1 in range(NUM_COL)] for x1 in range(NUM_ROW)]  #target task
        self.qtable= []
        self.delta = [[0 for y in range(NUM_COL)]for x in range(NUM_ROW)]
        self.delta_state = [[0 for y in range(NUM_COL)]for x in range(NUM_ROW)]
        self.delta_state_check = [[0 for y in range(NUM_COL)]for x in range(NUM_ROW)]
        self.f = open('step_episode.csv','w')
        self.q = open('q_table(target).csv','w')
        self.t = open('q_table(target_t).csv','w')
        self.b = open('boukyaku.csv','w')
        self.v = open('T_value.csv','w')
        self.d = open('delta.csv','w')
        self.field_now = self.field[self.agent.y][self.agent.x]
        self.state_agent_now = self.state_agent[self.agent.y][self.agent.x]    #上記の初期化でagent.xはcurrentxとなっている（yも同様）
        self.state_agent_now_prob = self.state_agent[self.agent.y][self.agent.x]

        self.clear()    #下記のclear()を開いて、報酬の設定などの初期設定を行う

        self.cursor = [int(NUM_ROW/2), int(NUM_COL/2)]
        self.possibility.set_all_possibility(self.state_agent,NUM_COL,NUM_ROW,self.field)
        clock = pygame.time.Clock()
        self.draw(self.screen)   #描画
        self.screen.fill((255,255,255))

        self.draw_t = True

        print("各種パラメータの値")
        print("転移率:" + str(const.TRANCE_RATE))
        print("温度定数(初期値):" + str(const.T))

        while (True):
            clock.tick(10000)
            self.update()
            if self.draw_t == True:
                self.draw(self.screen)
            if const.EPISODE_Agent1 == const.FINISH_EPISODE:
                self.run = False

            pygame.display.update()
            for event in pygame.event.get():   #キーボード入力
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==KEYDOWN:   #キーを押したとき
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key==K_t:   #aを押したとき
                        self.draw_t = not self.draw_t
                    elif event.key==K_a:   #aを押したとき
                        self.run = not self.run   #自動
                    elif event.key==K_s:   #sを押したとき
                        self.run = not self.run   #自動
                    elif event.key==K_w:   #nを押したとき
                        self.step()   #1ステップずつ
                    elif event.key==K_F1:
                        self.action = self.state_agent_now.action_select2()
                        self.step_control()
                    elif event.key==K_F2:
                        self.action = self.state_agent_now.action_select0()
                        self.step_control()
                    elif event.key==K_F3:
                        self.action = self.state_agent_now.action_select3()
                        self.step_control()
                    elif event.key==K_F4:
                        self.action = self.state_agent_now.action_select1()
                        self.step_control()
                    elif event.key ==K_x:
                        self.stop=1
                        if self.cursor[0] < 0: self.cursor[0] = 0
                    elif event.key == K_LEFT:
                        self.cursor[0] -= 1
                        if self.cursor[0] < 0: self.cursor[0] = 0
                    elif event.key == K_RIGHT:
                        self.cursor[0] += 1
                        if self.cursor[0] > NUM_COL-1: self.cursor[0] = NUM_COL-1
                    elif event.key == K_UP:
                        self.cursor[1] -= 1
                        if self.cursor[1] < 0: self.cursor[1] = 0
                    elif event.key == K_DOWN:
                        self.cursor[1] += 1
                        if self.cursor[1] > NUM_ROW-1: self.cursor[1] = NUM_ROW-1

                    elif event.key == K_o:
                        for x in range(NUM_COL):
                            for y in range(NUM_ROW):
                                pass

                    elif event.key == K_SPACE:
                        x, y = self.cursor
                        self.view1 = self.state_agent[y][x]
                        print ('-----------------------------------')
                        print ('      %05.6f' %self.qtable_t[x][y][2])
                        print ('%05.6f' %self.qtable_t[x][y][0])
                        print ('       %05.6f' %self.qtable_t[x][y][1])
                        print ('      %05.6f' %self.qtable_t[x][y][3])
                        print ('-----------------------------------')

                    elif event.key == K_g:
                        x, y = self.cursor
                        self.view2 = self.state_hunter2[y][x]
                        print ('-----------------------------------')
                        print ('      %05.2f' %self.view2.action2[2].q)
                        print ('%05.2f' %self.view2.action2[0].q,)
                        print ('       %05.2f' %self.view2.action2[1].q)
                        print ('      %05.2f' %self.view2.action2[3].q)
                        print ('-----------------------------------')

                    elif event.key == K_d:
                        self.log.delta(self.delta,self.d,NUM_ROW-1,NUM_COL-1)
                    elif event.key == K_c:
                        self.log.q_logger_q_table(self.qtable_c,NUM_ROW-1,NUM_COL-1,ACTION,self.q)    #init
                    elif event.key == K_b:
                        self.draw_b(self.screen)
                    elif event.key == K_q:
                        self.draw_q(self.screen)

    def clear(self):
        for y in range(NUM_COL):
            for x in range(NUM_ROW):
                self.field[y][x] = Field(const.FIELD[y][x])

        if self.agent_number == 1:
            self.trance.inter_mapping(self.qtable, self.qtable_c, self.qtable_s)

        if self.agent_number == 2:
            self.trance.inter_mapping2(self.qtable, self.qtable_c, self.qtable_s)

        self.s_count = 0;
        for y in range(NUM_COL):
            for x in range(NUM_ROW):
                if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_c,x,y) > 0 and self.state_agent[y][x].get_max_q_prob(self.qtable_c,x,y,self.state_agent_now_prob) >= 0.9:
                    self.delta_state[x][y] = 1

    '''
    def draw(self, screen):   #マップを描画
        #print("debug draw")
        sysfont = pygame.font.SysFont(None, 30)
        for y in range(NUM_COL):
            for x in range(NUM_ROW):
                if self.field[y][x].k == WALL:   #障害物
                    pygame.draw.rect(screen,(0,0,0),Rect(x*CS,y*CS,CS,CS))   #0,0,0=黒
                elif self.field[y][x].k == ROAD:
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))   #CS_COLOR=255,255,255=白
                elif self.field[y][x].k == GOAL:   #ゴール
                    pygame.draw.rect(screen,(100,255,255),Rect(x*CS,y*CS,CS,CS))   #100,255,255=水色　ゴール部分
                elif self.field[y][x].k == START:   #スタート
                    pygame.draw.rect(screen,(0,255,0),Rect(x*CS,y*CS,CS,CS))   #100,255,255=水色　ゴール部分
                self.state_agent_now_prob = self.state_agent[y][x]
                num = self.state_agent[y][x].get_max_q_action(self.qtable_c,x,y).d
                direction = u""
                if num==UP:
                    direction = u"↑"
                elif num==DOWN:
                    direction = u"↓"
                elif num==LEFT:
                    direction = u"←"
                elif num==RIGHT:
                    direction = u"→"
                if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_c,x,y) > 0 and self.state_agent[y][x].get_max_q_prob(self.qtable_c,x,y,self.state_agent_now_prob) >= 0.9:
                        color = (255,0,0)
                        screen.blit(self.font.render(direction, True, color), (x*CS,y*CS))
                if y == self.agent.y and x == self.agent.x:   #常に表示
                    pygame.draw.rect(screen,(0,0,255),Rect(x*CS,y*CS,CS,CS))   #0,0,255=青色　　　エージェントの位置
                pygame.draw.rect(screen,(50,50,50),Rect(x*CS,y*CS,CS,CS),1)   #50,50,50=灰色　　　グリッドの淵の色
                step = sysfont.render('step='+'%d' %const.Step_Agent1, False, (0,0,0))
                white_step = sysfont.render('         '+'%d' %const.Step_f_Agent1, False, (255,255,255))
                episode=sysfont.render('episode='+'%d' %const.EPISODE_Agent1, False, (0,0,0))
                white_episode = sysfont.render('               '+'%d' %const.EPISODE_Agent1, False, (255,255,255))
                self.screen.blit(white_step, (20,const.SCR_Y+35))
                self.screen.blit(step, (20,const.SCR_Y+35))
                self.screen.blit(white_episode, (20,const.SCR_Y+70))
                self.screen.blit(episode, (20,const.SCR_Y+70))
        pygame.draw.rect(screen, (0,255,0), Rect(self.cursor[0]*CS,self.cursor[1]*CS,CS,CS), 5)   #0,255,0=緑　カーソルの淵
    '''

    def draw_b(self, screen):
        #print('OK')
        for y in range(1,NUM_COL-1):
            for x in range(1,NUM_ROW-1):
                if self.delta[x][y] != 0:
                    pygame.draw.rect(screen,(0,255,0),Rect(x*CS,y*CS,CS,CS))
                    '''
                    val = self.delta[x][y]
                    if val > 1:
                         val = 1
                    val *= 255.0   #複合演算子
                    color = (0,val,0)
                    pygame.draw.rect(screen,color,Rect(x*CS,y*CS,CS,CS))
                    '''
                pygame.draw.rect(screen,(50,50,50),Rect(x*CS,y*CS,CS,CS),1)
                num = self.state_agent[y][x].get_max_q_action(self.qtable_s,x,y).d
                direction = u""
                if num==UP:
                    direction = u"↑"
                elif num==DOWN:
                    direction = u"↓"
                elif num==LEFT:
                    direction = u"←"
                elif num==RIGHT:
                    direction = u"→"
                if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_s,x,y) > 0 and self.state_agent[y][x].get_max_q_prob(self.qtable_s,x,y,self.state_agent_now_prob) >= 0.9:
                    color = (255,0,0)
                    screen.blit(self.font.render(direction, True, color), (x*CS,y*CS))

    def draw(self, screen):
         sysfont = pygame.font.SysFont(None, 30)
         for y in range(NUM_COL):
            for x in range(NUM_ROW):
                if self.field[y][x].k == WALL:   #障害物
                    pygame.draw.rect(screen,(0,0,0),Rect(x*CS,y*CS,CS,CS))   #0,0,0=黒


                if self.field[y][x].k == START:   #スタート
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    direction = u"S"
                    screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS+10,y*CS))


                if self.field[y][x].k == GOAL:   #ゴール
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    direction = u"G"
                    screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS+5,y*CS))
                    #pygame.draw.rect(screen,(100,255,255),Rect(x*CS,y*CS,CS,CS))

                if self.field[y][x].k == ROAD:
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_c,x,y) != 0:   #色を濃くしていく部分（元のサンプルコード）
                        val = self.state_agent[y][x].get_max_q_action_return_q(self.qtable_c,x,y)
                        if val > 1:
                             val = 1
                        val *= 255.0   #複合演算子
                        color = (255,255-val,255-val)
                        pygame.draw.rect(screen,color,Rect(x*CS,y*CS,CS,CS))
                        num = self.state_agent[y][x].get_max_q_action(self.qtable_c,x,y).d
                        direction = u""
                        if num==UP:
                            direction = u"↑"
                        elif num==DOWN:
                            direction = u"↓"
                        elif num==LEFT:
                            direction = u"←"
                        else:
                            direction = u"→"
                        '''
                        if self.agent_number ==1:
                            direction = u""
                            if num==UP:
                                direction = u"↑"
                            elif num==DOWN:
                                direction = u"↓"
                            elif num==LEFT:
                                direction = u"←"
                            else:
                                direction = u"→"
                        if self.agent_number ==2:
                            direction = u""
                            if num==UP:
                                direction = u"⇗"
                            elif num==DOWN:
                                direction = u"↙"
                            elif num==LEFT:
                                direction = u"↖"
                            else:
                                direction = u"↘"
                        '''
                        if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_c,x,y) > 0 and self.state_agent[y][x].get_max_q_prob(self.qtable_c,x,y,self.state_agent_now_prob) >= 0.9:
                            screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS,y*CS))

                if y == self.agent.y and x == self.agent.x:   #常に表示
                    pygame.draw.rect(screen,(0,0,255),Rect(x*CS,y*CS,CS,CS))

                pygame.draw.rect(screen,(50,50,50),Rect(x*CS,y*CS,CS,CS),1)
                step = sysfont.render('step='+'%d' %const.Step_Agent1, False, (0,0,0))
                white_step = sysfont.render('         '+'%d' %const.Step_f_Agent1, False, (255,255,255))
                episode=sysfont.render('episode='+'%d' %const.EPISODE_Agent1, False, (0,0,0))
                white_episode = sysfont.render('               '+'%d' %const.EPISODE_Agent1, False, (255,255,255))
                self.screen.blit(white_step, (20,const.SCR_Y+35))
                self.screen.blit(step, (20,const.SCR_Y+35))
                self.screen.blit(white_episode, (20,const.SCR_Y+70))
                self.screen.blit(episode, (20,const.SCR_Y+70))

    #ハンター1の行動step
    def step(self):
        if self.delta_state[self.agent.x][self.agent.y] == 1 and self.delta_state_check[self.agent.x][self.agent.y] ==0:
            self.delta_state_check[self.agent.x][self.agent.y] = 1
            self.s_count = self.s_count + 1
        self.possibility.now_possibility(self.agent.y,self.agent.x,self.state_agent,self.field,self.agent_number)
        self.action = self.state_agent_now.action_select(self.qtable_c,self.agent.x,self.agent.y,self.state_agent_now)    #field.pyにあるaction_select()をself.field（現在位置）で開く　stateはfieldを代入しているのでmが使える！
        self.action_no = self.action.d
        self.xx1 = self.agent.x
        self.yy1 = self.agent.y
        self.agent.move(self.action)    #行動によって移動先にcurrentを（x or y）を変更！
        self.field_now = self.field[self.agent.y][self.agent.x]
        self.state_agent_now = self.state_agent[self.agent.y][self.agent.x]    #上記に伴いstateも移動先に変更！
        const.Step_Agent1 = const.Step_Agent1+1
        self.episode_finish(self.agent,self.field)
        pygame.draw.rect(self.screen, (255,255,255), Rect(10,const.SCR_Y,200,const.SCR_Y + 100))
        #if (const.Step_Agent1 %1000) == 0:
             #self.run = not self.run

    def step_control(self):
        self.action_no = self.action.d
        self.xx1 = self.agent.x
        self.yy1 = self.agent.y
        self.agent.move(self.action)
        Possibility.now_possibility(self,self.agent.y,self.agent.x,self.state_agent)
        self.field_now = self.field[self.agent.y][self.agent.x]
        self.state_agent_now = self.state_agent[self.agent.y][self.agent.x]
        const.Step_Agent1 = const.Step_Agent1+1
        self.episode_finish(self.agent,self.field)



    def update(self):   #runの状態ならstepを進める
        if self.run == True:
            self.step()

    def episode_finish(self,agent,field):

        if self.field_now.k == GOAL:
            #self.tl_learning.delta_rl(self.xx1,self.yy1,self.agent.x,self.agent.y,self.qtable_c,self.state_agent,self.delta)
            self.action.update_q_value(1,1,self.state_agent,self.qtable_t,self.agent.x,self.agent.y,self.action_no,self.xx1,self.yy1,self.qtable_c,self.delta)
            self.tl_learning.tl_update_q(self.qtable_c,self.qtable_s,self.qtable_t,self.xx1,self.yy1,self.action_no,self.delta,self.state_agent)
            #self.log.boukyaku(const.EPISODE_Agent1,const.MAX_qtable_t,self.b)
            self.agent.move_start()
            self.state_agent_now = self.state_agent[self.agent.y][self.agent.x]
            self.field_now = self.field[self.agent.y][self.agent.x]
            sysfont = pygame.font.SysFont(None, 30)
            white_step = sysfont.render('         '+'%d' %const.Step_f_Agent1, False, (255,255,255))
            white_episode = sysfont.render('               '+'%d' %const.EPISODE_Agent1, False, (255,255,255))
            self.screen.blit(white_step, (20,const.SCR_Y+35))
            self.screen.blit(white_episode, (20,const.SCR_Y+70))
            const.EPISODE_Agent1 = const.EPISODE_Agent1+1
            print("episode" + str(const.EPISODE_Agent1) + ":" + str(const.Step_Agent1))
            #print("episode" + str(const.EPISODE_Agent1) + ":" + str(const.T))
            self.log.q_logger_step_episode(self.f)
            #self.log.T_value(self.v)
            const.Step_Agent1 = 0
            #const.T=(T_p_base+T_f)-((const.T_f-const.T_p)*math.exp(-const.K*const.EPISODE_Agent1)+const.T_p)
            #const.T=(const.T_f+const.T_p)-((const.T_p-const.T_f)*math.exp(-const.K*const.EPISODE_Agent1)+const.T_f)

            if const.EPISODE_Agent1 == FINISH_EPISODE:
                self.log.q_logger_q_table(self.qtable_c,NUM_ROW-1,NUM_COL-1,ACTION,self.q)
                self.log.delta(self.delta,self.d,NUM_ROW-1,NUM_COL-1)
                self.s_count_b = 0
                for y in range(NUM_COL):
                    for x in range(NUM_ROW):
                        if self.delta_state[x][y] == 1 and self.delta[x][y] != 0:
                            self.s_count_b = self.s_count_b + 1
                print("評価する状態:"+ str(self.s_count))
                print("忘却した状態:"+ str(self.s_count_b))
                self.similar = float(1 -(float(self.s_count_b)/float(self.s_count)))
                print("類似率:" + str(self.similar*100))

        else:
            if self.action.p == True:
                self.tl_learning.delta_rl(self.xx1,self.yy1,self.agent.x,self.agent.y,self.qtable_c,self.state_agent,self.delta)
                self.action.update_q_value(1,0,self.state_agent,self.qtable_t,self.agent.x,self.agent.y,self.action_no,self.xx1,self.yy1,self.qtable_c,self.delta)
                self.tl_learning.tl_update_q(self.qtable_c,self.qtable_s,self.qtable_t,self.xx1,self.yy1,self.action_no,self.delta,self.state_agent)


if __name__ == '__main__':
    Map()
