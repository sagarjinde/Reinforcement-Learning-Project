# Policy Gradient

## CartPole
![cartpole](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cartpole.gif)

### Environment
Used OpenAI Gym Environment. Refer to [wiki](https://github.com/openai/gym/wiki/CartPole-v0) for details.

### Observation
Comparing all possible combinations of reward-to-go and advantage-normalization

|  | reward-to-go = False | reward-to-go = True |
| --- | --- | --- |
| advantage-normalization = False | ![cp_FF](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cp_FF.png) | ![cp_TF](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cp_TF.png) |
| advantage-normalization = True | ![cp_FT](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cp_FT.png) | ![cp_TT](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cp_TT.png) |
#### Result: Best results were obtained using both reward-to-go and advantage-normalization 

## LunarLander
![lunarlander](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/lunarlander.gif)

### Observation
Comparing all possible combinations of reward-to-go and advantage-normalization

![ll_TT](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/ll_TT.png)

#### reward-to-go: True, advantage-normalization: False
![ll_TF](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/ll_TF.png)

#### reward-to-go: False, advantage-normalization: True
![ll_FT](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/ll_FT.png)

#### reward-to-go: False, advantage-normalization: False
![ll_FF](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/ll_FF.png)