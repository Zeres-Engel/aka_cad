import random
import numpy as np
from tqdm import tqdm
from .place_obj2box import PlaceObj2Box

class RLLearning:
    def __init__(self):
        # self.obj = [[10, 20], [20, 30], [30, 40], [40, 50], [50, 60], [60, 70], [70, 80], [80, 90], [90, 100], [100, 110], [110, 120], [50, 50], [50, 50]]
        self.obj = [[50, 50]] * 20
        self.place_obj2box = PlaceObj2Box(self.obj)

        self.q_table = {}
        self.action_space = self.init_action_space()
        self.alpha = 0.2
        self.gamma = 0.99
        self.epsilon = 0.5
        self.episodes = 1000000
        self.limit_steps = 1000
        self.history = []

    def init_action_space(self):
        action_space = []
        for obj_index in range(len(self.obj)):
            for box_index in range(len(self.place_obj2box.boxes)):
                box_size = self.place_obj2box.boxes[box_index]['box_size']
                for x in range(box_size[0]):
                    for y in range(box_size[1]):
                        action_space.append((obj_index, box_index, (x, y)))
        return action_space
    
    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.action_space)
        else:
            state_actions = self.q_table.get(state, {})
            if not state_actions:
                return random.choice(self.action_space)
            return max(state_actions, key=state_actions.get)

    def update_q_table(self, state, action, reward, next_state):
        current_q = self.q_table.get(state, {}).get(action, 0)
        next_max_q = max(self.q_table.get(next_state, {}).values(), default=0)
        new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * next_max_q)
        
        if state not in self.q_table:
            self.q_table[state] = {}
        else:
            pass
        self.q_table[state][action] = new_q
        
    def run(self):
        for _ in tqdm(range(self.episodes)):
            total_reward = 0
            self.place_obj2box.reset()
            state = self.place_obj2box.state()

            for _ in range(self.limit_steps):
                # choose action
                action = self.choose_action(state)
                obj_index, box_index, pos = action

                # run action
                reward, done = self.place_obj2box.action(obj_index, box_index, pos)
                total_reward += reward
                next_state = self.place_obj2box.state()

                # update q_table
                self.update_q_table(state, action, reward, next_state)
                state = next_state

                if done:
                    print(total_reward)
                    out_path = self.place_obj2box.render()
                    self.history.append({
                        'total_reward': total_reward,
                        'out_path': out_path
                    })
                    break
            

        # get max reward
        max_reward = max([x['total_reward'] for x in self.history])
        max_reward_index = np.argmax([x['total_reward'] for x in self.history])
        max_reward_out_path = self.history[max_reward_index]['out_path']
        print("Max reward: ", max_reward)
        print("Max reward output path: ", max_reward_out_path)
