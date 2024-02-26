LogicSynCommands = [
    'rewrite',
    'rewrite -z',
    'refactor',
    'refactor -z',
    'resub',
    'resub -z',
    'balance'
    ''
    ];

features = [
    'input_pins',
    'output_pins',
    'number_of_nodes',
    'number_of_edges',
    'number_of_levels',
    'number_of_latches',
    'percentage_of_ands',
    'percentage_of_ors',
    'percentage_of_nots'
    ];

abc_binary = './yosys-abc.exe';
yosys_binary = './yosys.exe';

design_dir = 'benchmarks/arithmetic/';

FPGA_Mapping = {
    'levels': 100,
    'lut_inputs': 6
    }

episodes_dir = 'playground'
episode_iteration_num = 50;

RL_Alg = 'ppo';

Log_file = 'log.txt';