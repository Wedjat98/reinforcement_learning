# coding:utf-8
"""
リフティング問題のDQNプログラム
Copyright(c) 2018 Koji Makino and Hiromitsu Nishizaki All Rights Reserved.
"""
import gym  #倒立振子(cartpole)の実行環境
from gym import wrappers  #gymの画像保存
import numpy as np
import time
import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
from multiprocessing import Pool
from chainer import serializers
import csv
import env_lifting

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


env = env_lifting.LiftingEnv()

print("observation space   : {}".format(env.observation_space.shape[0]))
print("action space        : {}".format(env.action_space))

n_times = 1
max_number_of_steps = 200  # 総step数
n_episodes = 500    #総試行回数

for n_repeat in range(1,n_times + 1):
    path_source = 'C:\\Users\\kiku\\PycharmProjects\\グループスタディ\\lifting_gl\\source_model.npz'
    path_target = 'C:\\Users\\kiku\\PycharmProjects\\グループスタディ\\lifting_gl\\reward_DQN_{}.csv'.format(n_repeat)

    gamma = 0.99    #割引率
    alpha = 0.5     #学習率
    q_func = QFunction(env.observation_space.shape[0], env.action_space.n)
    optimizer = chainer.optimizers.Adam(eps=1e-2)
    optimizer.setup(q_func)
    explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(start_epsilon=1.0, end_epsilon=0.1, decay_steps=n_episodes, random_action_func=env.action_space.sample)
    replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10 ** 6)
    phi = lambda x: x.astype(np.float32, copy=False)

    source_agent = chainerrl.agents.DQN(
            q_func, optimizer, replay_buffer, gamma, explorer,
            replay_start_size=500, update_interval=1, target_update_interval=100, phi=phi)

    with open(path_target, 'w') as f:
        for episode in range(1, n_episodes + 1):  # 試行数分繰り返す
            writer = csv.writer(f, lineterminator='\n')
            observation = env._reset()
            done = False
            reward = 0
            R = 0
            while not done and R < 10:
                if episode % 100 == 0:
                    env._render('human')    #画面表示
                action = source_agent.act_and_train(observation, reward)
                observation, reward, done, info = env._step(action)
                R += reward

            writer.writerow([episode, R, source_agent.get_statistics()])  # episode、reward, elapsed_time
            source_agent.stop_episode_and_train(observation, reward, done)
            if episode == 1 or episode % 10 == 0:
                print('NO.',n_repeat, 'episode:', episode, 'R:', R, 'statistics:', source_agent.get_statistics())  #結果表示
        serializers.save_npz(path_source, source_agent.target_model)

env.close()