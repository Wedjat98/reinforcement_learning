# coding:utf-8
"""
倒立振子のDQNプログラム
Copyright(c) 2018 Koji Makino and Hiromitsu Nishizaki All Rights Reserved.
"""
import numpy as np
import time
import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
from multiprocessing import Pool
from chainer import serializers
import csv
import env_cartpole

# Q-関数の定義
class QFunction(chainer.Chain):
    def __init__(self, obs_size, n_actions, n_hidden_channels=50):
        super().__init__(
            l0=L.Linear(obs_size, n_hidden_channels),
            l1=L.Linear(n_hidden_channels, n_hidden_channels),
            l2=L.Linear(n_hidden_channels, n_actions))
    def __call__(self, x, test=False):
        h = F.tanh(self.l0(x))
        h = F.tanh(self.l1(h))
        return chainerrl.action_value.DiscreteActionValue(self.l2(h))



env = env_cartpole.CartPoleEnv()
n_times = 1
print("observation space   : {}".format(env.observation_space.shape[0]))
print("action space        : {}".format(env.action_space))


for n_repeat in range(1, n_times+1):
    path_source = 'C:\\Users\\kiku\\PycharmProjects\\グループスタディ\\cartpole_gl' \
                  '\\source_model_1.npz'
    path_target = 'C:\\Users\\kiku\\PycharmProjects\\グループスタディ\\cartpole_gl' \
                  '\\reward_trancefer_{}.csv'.format(n_repeat)



    gamma = 0.99    #割引率
    alpha = 0.5     #学習率
    max_number_of_steps = 200  #最大step数
    num_episodes = 500  #総試行回数(最大eposode数)

    q_func = QFunction(env.observation_space.shape[0], env.action_space.n)
    serializers.load_npz(path_source, q_func)
    optimizer = chainer.optimizers.Adam(eps=1e-2)
    optimizer.setup(q_func)
    explorer = chainerrl.explorers.ConstantEpsilonGreedy(epsilon=0.1,
                                                         random_action_func=env.action_space.sample)  # ε-greedy法
    replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10 ** 6)
    phi = lambda x: x.astype(np.float32, copy=False)
    agent = chainerrl.agents.DQN(
        q_func, optimizer, replay_buffer, gamma, explorer,
        replay_start_size=500, update_interval=1, target_update_interval=100, phi=phi)


    with open(path_target, 'w') as f:   #結果ファイルの作成
        for episode in range(1, num_episodes+1):  #試行数分繰り返す
            writer = csv.writer(f, lineterminator='\n')
            observation = env.reset()
            done = False
            reward = 0
            R = 0
            for t in range(max_number_of_steps):  #1試行のループ
                if episode % 100 == 0:
                    env.render()    #画面表示
                action = agent.act_and_train(observation, reward)
                observation, reward, done, info = env.step(action)
                R += reward
                if done:
                    break
            writer.writerow([episode, R, agent.get_statistics()])
            agent.stop_episode_and_train(observation, reward, done)
            if episode == 1 or episode % 10 == 0:
                print('NO.', n_repeat, 'episode:', episode, 'R:', R, 'statistics:', agent.get_statistics())   #結果表示
        #serializers.save_npz(path_source, agent.target_model)

env.close()