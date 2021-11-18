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
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size)   #以下、self.名称はアトリビュートを追加
        pygame.display.set_caption(u"Source-Task")
        self.font = pygame.font.SysFont("timesnewroman",42)
        self.field = [[Field(GOAL)  for x in range(NUM_ROW)] for y in range(NUM_COL)]  #State(GOAL)はfieldクラスの呼び出し　fieldに対してk,rの変数を追加！←重要
        self.agent = Agent()    #agentという変数にｘとｙを追加（set getの部分を初期化している）
        self.state_agent = [[State(GOAL) for x in range(NUM_ROW)] for y in range(NUM_COL)]
        self.qtable_agent = [[[0 for action in range(ACTION)]for y in range(NUM_COL)] for x in range(NUM_ROW)] #7次元配列
        self.clear()    #下記のclear()を開いて、報酬の設定などの初期設定を行う
        self.field_now = self.field[self.agent.y][self.agent.x]
        self.state_agent_now = self.state_agent[self.agent.y][self.agent.x]    #上記の初期化でagent.xはcurrentxとなっている（yも同様）

        self.run = False
        self.possibility = Possibility()
        self.log = Log()

        self.cursor = [int(NUM_COL/2), int(NUM_ROW/2)]
        self.possibility.set_all_possibility(self.state_agent,NUM_COL,NUM_ROW,self.field)   
        clock = pygame.time.Clock()
        self.draw(self.screen)   #描画
        self.screen.fill((255,255,255))
        self.count = 0
        self.count2 = 0

        self.f=open('step_episode.csv','w')
        self.q=open('q_table(source).csv','w')
        self.stop=0
        
        self.draw_t = True


        while (const.EPISODE_Agent1 != FINISH_EPISODE+1):
            clock.tick(10000)
            self.update()
            if self.draw_t == True:
                self.draw(self.screen)
            pygame.display.update()
            for event in pygame.event.get():   #キーボード入力
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==KEYDOWN:   #キーを押したとき
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key==K_t:   
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
                        print ('      %05.2f' %self.view1.action[2].q)
                        print ('%05.2f' %self.view1.action[0].q,)
                        print ('       %05.2f' %self.view1.action[1].q)
                        print ('      %05.2f' %self.view1.action[3].q)
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

    #init
    def clear(self):
        for y in range(NUM_COL):
            for x in range(NUM_ROW):
                self.field[y][x] = Field(const.FIELD[y][x])
    
    def draw(self, screen):   #マップを描画
        sysfont = pygame.font.SysFont(None, 30)
        for y in range(NUM_COL):
            for x in range(NUM_ROW):
                if self.field[y][x].k == WALL:   #障害物
                    pygame.draw.rect(screen,(0,0,0),Rect(x*CS,y*CS,CS,CS))   #0,0,0=黒
                elif self.field[y][x].k == START:   #スタート
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    direction = u"S"
                    screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS+10,y*CS))
                elif self.field[y][x].k == GOAL:   #ゴール
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    direction = u"G"
                    screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS+5,y*CS))
                elif self.field[y][x].k == ROAD:
                    pygame.draw.rect(screen,CS_COLOR,Rect(x*CS,y*CS,CS,CS))
                    if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_agent,x,y) != 0:   #色を濃くしていく部分（元のサンプルコード）
                        val = self.state_agent[y][x].get_max_q_action_return_q(self.qtable_agent,x,y)
                        if val > 1:
                             val = 1
                        val *= 255.0   #複合演算子
                        color = (255,255-val,255-val)
                        pygame.draw.rect(screen,color,Rect(x*CS,y*CS,CS,CS))
                        num = self.state_agent[y][x].get_max_q_action(self.qtable_agent,x,y).d
                        direction = u""
                        if num==UP:
                            direction = u"↑"
                        elif num==DOWN:
                            direction = u"↓"
                        elif num==LEFT:
                            direction = u"←"
                        else:
                            direction = u"→"
                        if self.state_agent[y][x].get_max_q_action_return_q(self.qtable_agent,x,y) > 0 and self.state_agent[y][x].get_max_q_prob(self.qtable_agent,x,y,self.state_agent_now) >= 0.9:
                            screen.blit(self.font.render(direction, True, (0,0,0)), (x*CS,y*CS))
                if y == self.agent.y and x == self.agent.x:   #常に表示
                    pygame.draw.rect(screen,(0,0,255),Rect(x*CS,y*CS,CS,CS))   #0,0,255=青色　　　エージェントの位置
                pygame.draw.rect(screen,(50,50,50),Rect(x*CS,y*CS,CS,CS),1)   #50,50,50=灰色　　　グリッドの淵の色
                step = sysfont.render('step='+'%d' %const.Step_Agent1, False, (0,0,0))
                white_step = sysfont.render('         '+'%d' %const.Step_f_Agent1, False, (255,255,255))
                episode=sysfont.render('episode='+'%d' %const.EPISODE_Agent1, False, (0,0,0))
                white_episode = sysfont.render('               '+'%d' %const.EPISODE_Agent1, False, (255,255,255))
                self.screen.blit(white_step, (20,const.SCR_Y+35 ))
                self.screen.blit(step, (20,const.SCR_Y+35))
                self.screen.blit(white_episode, (20,const.SCR_Y+70))
                self.screen.blit(episode, (20,const.SCR_Y+70))

        pygame.draw.rect(screen, (0,255,0), Rect(self.cursor[0]*CS,self.cursor[1]*CS,CS,CS), 5)   #0,255,0=緑　カーソルの淵
    

    def step(self):
        self.action = self.state_agent_now.action_select(self.qtable_agent,self.agent.x,self.agent.y)    #field.pyにあるaction_select()をself.field（現在位置）で開く　stateはfieldを代入しているのでmが使える！
        self.action_no = self.action.d
        self.xx1 = self.agent.x
        self.yy1 = self.agent.y
        self.agent.move(self.action)    #行動によって移動先にcurrentを（x or y）を変更！
        self.possibility.now_possibility(self.agent.y,self.agent.x,self.state_agent,self.field)
        self.field_now = self.field[self.agent.y][self.agent.x]
        self.state_agent_now = self.state_agent[self.agent.y][self.agent.x]    #上記に伴いstateも移動先に変更！
        const.Step_Agent1 = const.Step_Agent1+1
        self.episode_finish(self.agent,self.field)
        pygame.draw.rect(self.screen, (255,255,255), Rect(10,const.SCR_Y,200,const.SCR_Y + 100))
        
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
            self.action.update_q_value(1,1,self.state_agent_now,self.qtable_agent,self.agent.x,self.agent.y,self.action_no,self.xx1,self.yy1)
            self.agent.move_start()
            self.state_agent_now = self.state_agent[self.agent.y][self.agent.x]
            self.field_now = self.field[self.agent.y][self.agent.x]

            sysfont = pygame.font.SysFont(None, 30)
            white_step = sysfont.render('         '+'%d' %const.Step_f_Agent1, False, (255,255,255))
            white_episode = sysfont.render('               '+'%d' %const.EPISODE_Agent1, False, (255,255,255))
            self.screen.blit(white_step, (20,const.SCR_Y+35))
            self.screen.blit(white_episode, (20,const.SCR_Y+75))
            print("episode" + str(const.EPISODE_Agent1) + ":" + str(const.Step_Agent1))
            self.log.q_logger_step_episode(self.f)
            const.EPISODE_Agent1 = const.EPISODE_Agent1+1
            const.Step_Agent1 = 0

            if const.EPISODE_Agent1 == FINISH_EPISODE:
                self.log.q_logger_q_table(self.qtable_agent,NUM_ROW-1,NUM_COL-1,ACTION,self.q)


        else:
            if self.action.p == True:
                self.action.update_q_value(1,0,self.state_agent_now,self.qtable_agent,self.agent.x,self.agent.y,self.action_no,self.xx1,self.yy1)



if __name__ == '__main__':
    Map()
