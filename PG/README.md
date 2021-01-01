# Policy Gradient

## CartPole
![cartpole](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cartpole.gif)

### Environment
Used OpenAI Gym Environment. Refer to [wiki](https://github.com/openai/gym/wiki/CartPole-v0) for details.

### Observation
Comparing all possible combinations of reward-to-go and advantage-normalization

#### reward-to-go: True, advantage-normalization: True
![cp_TT](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cp_TT.png)

#### reward-to-go: True, advantage-normalization: False
![cp_TF](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cp_TF.png)

#### reward-to-go: False, advantage-normalization: True
![cp_FT](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cp_FT.png)

#### reward-to-go: False, advantage-normalization: False
![cp_FF](https://github.com/sagarjinde/Reinforcement-Learning-Project/blob/master/PG/figs/cp_FF.png)