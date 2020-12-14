# Q-Learning

## Pac-Man

### Environment Design
- Initial grid size: 3x3
- Initial number of food pallets: 3
- MDP State depents on : 
	- pacman location
	- ghost location
	- food pallet location
- Number of food pallets generated after pacman consumes all food pallets: between 0 to 3 (Unifrom Distrabution)
- Reward: 
	- +10 for eating food pallets
	- -100 for dying 
	- +1 for surviving each turn
- Pacman can move left, right, up, down
- Pacman also has the option to not perform any moves
- Ghost can move left, right, up, down
- Ghost movements are random

### Observation
![pacman_qlearning](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/Q-Learning/figs/pac-man_qlearning.png)

![pacman_sarsa](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/Q-Learning/figs/pac-man_sarsa.png)

After `10000 epochs`, pacman scored around `1200 points` on average.

Q-Learning and SARSA gave almost similar performance. But on multiple runs of the code, it was observed that Q-Learning 
performed well consistantly whereas SARSA had some variance.

### Running the code
Type `python pacman.py`

## Tic-Tac-Toe

### Environment Design
- Standard Tic-Tac-Toe environment
- Agents can be of 3 types
	| Name | Behaviour |
	| ---- | --------- |
	| Random | Actions picked randomly |
	| Safe | Actions picked optimally | 
	| Both | Actions picked randomly with some probability | 
- Agent is trained for 49 epochs where in each epoch, 100 games are played
- Agent is tested on the 50th epoch where 1000 games are played and result is recorded
- Performance is measured by the number of wins, looses and draws

### Observation
| My Agent | Opponent Agent | #Wins | #Draws | #Losses |
| --- | --- | --- | --- | --- |
| Random | Random | 879 | 73 | 48 |
| Random | Safe | 448 | 459 | 93 |
| Safe | Random | 826 | 142 | 32 |
| Safe | Safe | 552 | 424 | 24 |
| Both | Random | 895 | 75 | 30 |
| Both | Safe | 441 | 488 | 71 |

### Running the code
Type `python tic-tac-toe.py`
