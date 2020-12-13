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
![pacman_qlearning]()

![pacman_sarsa]()