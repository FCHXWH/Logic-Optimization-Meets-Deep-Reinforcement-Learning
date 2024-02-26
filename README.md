# Logic-Optimization-Meets-Deep-Reinforcement-Learning

Logic optimization is a key step during the process of designing digit circuits, whose purpose is to reduce the area and delay of digital circuits. Several logic optimization
algorithms have been proposed in the past decades, which have been developed as the basic logic optimization operators (LOO). Designers apply these LOOs iteratively and hybridly to reduce
the area and delay of digital circuits continually. However, the order of applying these LOOs has a significant impact on the reward of logic optimization, which is designed by experience. In this project, we are aimed at determining the order of LOOs automatically with the aid of deep reinforcement learning (DRL).
![image](https://github.com/FCHXWH/Logic-Optimization-Meets-Deep-Reinforcement-Learning/assets/37615445/d63eadb5-2efd-4d68-b5a2-ffb0dbc8849f)
![image](https://github.com/FCHXWH/Logic-Optimization-Meets-Deep-Reinforcement-Learning/assets/37615445/e0cdecd2-1695-471d-bc1e-a9527f891a08)

## Requirements:
1. Logic Optimization tools: yosys.exe, yosys-abc.exe, abc.rc

## Setup:
1. set up an conda virtual environment: conda create --name LODRL python=3.6;
2. enter the env: conda activate LODRL;
3. install the required packages: pip install -r requirement.txt;

## Benchmarks:
1. git clone https://github.com/lsils/benchmarks.git

## Run:
1. Edit parameters.py;
2. Run python LODRL_Stable_Baselines3

## Other materials:
1. VE693_Project.pdf: project report;
2. Course-Syllabus-VE693-Fall2021.pdf: course syllabus of course ve693 (Deep Reinforcement Learning).
