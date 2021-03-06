#!/usr/local/bin python
# -*- coding:utf-8 -+-

'''--------パラメータ設定--------'''

LEARNING_RATE = 0.1                 #学習率
DISCOUNT_RATE = 0.9                 #割引率
SCR_X = 45*12                       #グリッドの大きさ(x軸)
SCR_Y = 45*12                       #グリッドの大きさ(y軸)
Text_Y = 35*4                       #文字表示のスペース
CS = 45                             #セルの大きさ
NUM_ROW = int(SCR_Y/CS)
NUM_COL = int(SCR_X/CS)
START_X = 1                         #スタート地点（x地点）
START_Y = 10                        #スタート地点（y地点）


Step_Agent1=0
Step_f_Agent1=-1
EPISODE_Agent1=1


T=0.01                              #温度定数
Action_no = 5                       #行動数

FINISH_EPISODE = 500                #終了エピソード数


'''
row0  = [3,3,3,3,3,3,3,3]
row1  = [3,2,2,2,2,2,1,3]
row2  = [3,2,2,2,2,2,2,3]
row3  = [3,2,2,2,2,2,2,3]
row4  = [3,2,2,2,2,2,2,3]
row5  = [3,2,2,2,2,2,2,3]
row6  = [3,2,2,2,2,2,2,3]
row7  = [3,0,2,2,2,2,2,3]
row8  = [3,3,3,3,3,3,3,3]



FIELD = [row0,row1,row2,row3,row4,row5,row6,row7,row8]
'''

'''10*10'''
'''
row0  = [3,3,3,3,3,3,3,3,3,3,3,3]
row1  = [3,2,2,2,2,2,2,2,2,2,1,3]
row2  = [3,2,2,2,2,2,2,2,2,2,2,3]
row3  = [3,2,2,2,2,2,2,2,2,2,2,3]
row4  = [3,2,2,2,2,2,2,2,2,2,2,3]
row5  = [3,2,2,2,2,2,2,2,2,2,2,3]
row6  = [3,2,2,2,2,2,2,2,2,2,2,3]
row7  = [3,2,2,2,2,2,2,2,2,2,2,3]
row8  = [3,2,2,2,2,2,2,2,2,2,2,3]
row9  = [3,2,2,2,2,2,2,2,2,2,2,3]
row10 = [3,0,2,2,2,2,2,2,2,2,2,3]
row11 = [3,3,3,3,3,3,3,3,3,3,3,3]



FIELD = [row0,row1,row2,row3,row4,row5,row6,row7,row8,row9,row10,row11]
'''

'''10*10'''

row0  = [3,3,3,3,3,3,3,3,3,3,3,3]
row1  = [3,2,3,2,2,2,2,2,3,3,1,3]
row2  = [3,2,3,2,2,2,2,2,3,2,2,3]
row3  = [3,2,2,2,2,3,2,2,2,2,2,3]
row4  = [3,2,2,2,3,2,3,3,2,3,2,3]
row5  = [3,2,2,2,2,3,2,2,3,2,2,3]
row6  = [3,2,2,2,3,2,3,2,2,3,2,3]
row7  = [3,2,2,2,2,2,2,2,2,3,3,3]
row8  = [3,3,2,3,2,2,3,3,2,2,2,3]
row9  = [3,2,2,3,2,2,2,2,2,2,2,3]
row10 = [3,0,2,2,2,3,2,2,2,2,2,3]
row11 = [3,3,3,3,3,3,3,3,3,3,3,3]



FIELD = [row0,row1,row2,row3,row4,row5,row6,row7,row8,row9,row10,row11]



