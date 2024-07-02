import numpy as np
from tqdm import tqdm
from .place_obj2box import PlaceObj2Box

class RandomLearning:
    def __init__(self):
        self.obj = [[10, 20], [20, 30], [30, 40], [40, 50], [50, 60], [60, 70], [70, 80], [80, 90], [90, 100], [100, 110], [110, 120]]
        self.place_obj2box = PlaceObj2Box(self.obj)

        self.epoch = 10000
        self.limit_steps = 1000
        self.history = []

    def run(self):
        for _ in tqdm(range(self.epoch)):
            total_reward = 0
            for _ in range(self.limit_steps):
                # random action
                obj_index = np.random.randint(0, len(self.obj))
                box_index = np.random.randint(0, len(self.place_obj2box.boxes))
                
                pos_range = self.place_obj2box.boxes[box_index]['box_size']
                pos = [np.random.randint(0, pos_range[0]), np.random.randint(0, pos_range[1])]
                
                # run action
                reward, done = self.place_obj2box.action(obj_index, box_index, pos)
                # self.place_obj2box.state()

                total_reward += reward
                if done:
                    out_path = self.place_obj2box.render()
                    self.history.append({
                        'total_reward': total_reward,
                        'out_path': out_path
                    })
                    break

            self.place_obj2box.reset()

        # get max reward
        max_reward = max([x['total_reward'] for x in self.history])
        max_reward_index = np.argmax([x['total_reward'] for x in self.history])
        max_reward_out_path = self.history[max_reward_index]['out_path']
        print("Max reward: ", max_reward)
        print("Max reward output path: ", max_reward_out_path)


