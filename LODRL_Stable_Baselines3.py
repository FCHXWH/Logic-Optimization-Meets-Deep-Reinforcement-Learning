import gym,os
from parameters import *
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from env import LogicSynEnv
from features import *
from parameters import *
import datetime
for fpathe,dirs,fs in os.walk(design_dir):
    for f in fs:
        if not (f.split('.')[1] == 'blif'):
            continue;
        design_file = design_dir + f;
        #initialize the level limitation
        stats = {};
        stats = abc_init_stats(design_file,abc_binary,stats);
        FPGA_Mapping['levels'] = stats['levels'];
        #start training 
        env = LogicSynEnv(design_file,f.split('.')[0],stats['levels']);
        model = PPO("MlpPolicy", env, verbose=1)
        start = datetime.datetime.now();
        model.learn(2500);
        duration = datetime.datetime.now() - start;
        log_path = episodes_dir+'_'+f.split('.')[0]+'\\'+Log_file;
        data = open(log_path,'w+');
        print('The training time is '+str(duration),file=data);
        model_file_name = RL_Alg+'_'+f.split('.')[0];
        model.save(model_file_name);
        obs = env.reset()
        print("The trained Logic optimization sequences are: ",file=data);
        for i in range(episode_iteration_num):
            action, _states = model.predict(obs)
            print(LogicSynCommands[action],file=data);
            obs, reward, done, info = env.step(action)
            env.render()
            if done:
              obs = env.reset()
        data.close();
        env.close()

