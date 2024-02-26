import numpy as np
import gym
from gym import spaces
from features import *
from parameters import *
import os
class LogicSynEnv(gym.Env):
    def _reward_table(self, constraint_met, contraint_improvement, optimization_improvement):
        return {
            True: {
                0: {
                    1: 3,
                    0: 0,
                    -1: -3
                }
            },
            False: {
                1: {
                    1: 3,
                    0: 2,
                    -1: 1
                },
                0: {
                    1: 2,
                    0: 0,
                    -1: -2
                },
                -1: {
                    1: -1,
                    0: -2,
                    -1: -3
                }
            }
        }[constraint_met][contraint_improvement][optimization_improvement]

    def _get_metrics(self, stats):
        """
        parse LUT count and levels from the stats command of ABC
        """
        line = stats.decode("utf-8").split('\n')[-2].split(':')[-1].strip()
        
        ob = re.search(r'lev *= *[0-9]+', line)
        levels = int(ob.group().split('=')[1].strip())
        
        ob = re.search(r'nd *= *[0-9]+', line)
        lut_6 = int(ob.group().split('=')[1].strip())

        return lut_6, levels

    def _get_reward(self, lut_6, levels):
        constraint_met = True
        optimization_improvement = 0    # (-1, 0, 1) <=> (worse, same, improvement)
        constraint_improvement = 0      # (-1, 0, 1) <=> (worse, same, improvement)

        # check optimizing parameter
        if lut_6 < self.lut_6:
            optimization_improvement = 1
        elif lut_6 == self.lut_6:
            optimization_improvement = 0
        else:
            optimization_improvement = -1
        
        # check constraint parameter
        if levels > self.levels_limitation:
            constraint_met = False
            if levels < self.levels:
                constraint_improvement = 1
            elif levels == self.levels:
                constraint_improvement = 0
            else:
                constraint_improvement = -1

        # now calculate the reward
        return self._reward_table(constraint_met, constraint_improvement, optimization_improvement)

    def _get_state(self,design_file):
        return extract_features(design_file, yosys_binary, abc_binary)
    def run_command(self,command):
        if not os.path.exists(episodes_dir+'_'+self.design+'\\'+str(self.episode_num)):
            os.makedirs(episodes_dir+'_'+self.design+'\\'+str(self.episode_num));
        output_design_file = os.path.join(episodes_dir+'_'+self.design,str(self.episode_num),str(self.step_num) + '.v');
        output_design_file_mapped = os.path.join(episodes_dir+'_'+self.design,str(self.episode_num),str(self.step_num) + '-mapped.v');
        abc_command = 'read ' + self.design_file + '; ';
        abc_command += ';'.join(command) + '; ';
        abc_command += 'write ' + output_design_file + '; '
        abc_command += 'if -K ' + str(FPGA_Mapping['lut_inputs']) + '; ';
        abc_command += 'write ' + output_design_file_mapped + '; '
        abc_command += 'print_stats;';
        try:
            proc = check_output([abc_binary, '-c', abc_command])
            # get reward
            lut_6, levels = self._get_metrics(proc)
            reward = self._get_reward(lut_6, levels)
            self.lut_6, self.levels = lut_6, levels
            self.log_inform = 'ls_command='+command[len(command)-1]+', lut_6_num='+str(self.lut_6)+', lut_6_level='+str(self.levels);
            # get new state of the circuit
            state = self._get_state(output_design_file)
            return state, reward
        except Exception as e:
            print(e)
            return None, None

    def __init__(self,design_file,design,levels_limitation):
        self.action_space = spaces.Discrete(len(LogicSynCommands));
        self.observation_space = spaces.Box(low=0,high=10000,shape=(len(features),),dtype=np.float64);
        self.lut_6, self.levels = 10000, 10000
        self.step_num = 1;
        self.episode_num = 0;
        self.iteration_num = 1;
        self.log_actions = ['strash'];
        self.log_inform = '';
        self.design_file = design_file;
        self.design = design;
        self.levels_limitation = levels_limitation

    def step(self, action):
        self.log_actions.append(LogicSynCommands[action]);
        state,reward = self.run_command(self.log_actions);
        self.iteration_num += 1;    
        done = False;
        if self.iteration_num == episode_iteration_num:
            done = True;
        log(self.log_inform);
        return state,reward,done,{};
    
    def reset(self):
        self.log_actions = ['strash'];
        self.iteration_num = 1;
        self.episode_num += 1;
        state,_ = self.run_command(self.log_actions);
        print('episode '+str(self.episode_num));
        log(self.log_inform);
        return state
    
    def render(self, mode='human'):
        lut_num,levels = self.lut_6,self.levels;
        log(self.log_inform);

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
