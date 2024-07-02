import os
import shutil
import cv2
import time
import numpy as np
from tqdm import tqdm
import random

def create_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
    except:
        pass
    os.mkdir(folder_path)

OUT_ROOT = 'out'
create_folder(OUT_ROOT)

class PlaceObj2Box:
    def __init__(self, objs):
        self.objs = objs
        self.used_obj_flags = [False] * len(objs)
        self.boxes = [
            {'box_size': [100, 100], 'placements': []},
            {'box_size': [200, 200], 'placements': []},
            {'box_size': [300, 300], 'placements': []}
        ]
        
    def state(self):
        # Convert state to a hashable type (tuple of tuples)
        used_flags = tuple(self.used_obj_flags)
        box_placements = tuple(
            tuple(
                (placed_obj['obj'][0], placed_obj['obj'][1], placed_obj['pos'][0], placed_obj['pos'][1])
                for placed_obj in box['placements']
            )
            for box in self.boxes
        )
        return used_flags, box_placements

    def action(self, obj_index, box_index, pos):
        """
        1. Select object
        2. Select box:
        3. Select position in box (center of object)
        """
        # check if object is used or new
        if self.used_obj_flags[obj_index]:
            reward = -1
            done = False
        else:
            selected_obj = self.objs[obj_index]
            selected_box = self.boxes[box_index]
            is_placed = self.place_obj(selected_obj, selected_box, pos)

            # calculate reward and check termination
            if is_placed:
                self.used_obj_flags[obj_index] = True
                reward = self.calculate_reward()
                done = self.check_termination()
            else:
                reward = -1
                done = False

        return reward, done

    def can_place(self, selected_obj, selected_box, pos):
        selected_pos_x1, selected_pos_y1, selected_pos_x2, selected_pos_y2 = pos[0] - selected_obj[0] / 2, pos[1] - selected_obj[1] / 2, pos[0] + selected_obj[0] / 2, pos[1] + selected_obj[1] / 2

        # check if selected object is out of box
        if selected_pos_x1 < 0 or selected_pos_x2 > selected_box['box_size'][0] or selected_pos_y1 < 0 or selected_pos_y2 > selected_box['box_size'][1]:
            return False
        
        # check if selected object is overlap with other objects
        for placed_obj in selected_box['placements']:
            placed_pos = placed_obj['pos']
            placed_obj_size = placed_obj['obj']
            placed_pos_x1, placed_pos_y1, placed_pos_x2, placed_pos_y2 = placed_pos[0] - placed_obj_size[0] / 2, placed_pos[1] - placed_obj_size[1] / 2, placed_pos[0] + placed_obj_size[0] / 2, placed_pos[1] + placed_obj_size[1] / 2

            if selected_pos_x1 < placed_pos_x2 and selected_pos_x2 > placed_pos_x1 and selected_pos_y1 < placed_pos_y2 and selected_pos_y2 > placed_pos_y1:
                return False
            
        return True

    def place_obj(self, selected_obj, selected_box, pos):
        if self.can_place(selected_obj, selected_box, pos):
            selected_box['placements'].append({
                'obj': selected_obj,
                'pos': pos
            })
            return True
        else:
            return False
        
    def calculate_reward(self):
        # Reward = number of used objects / number of used boxes / area of used boxes
        num_used_objs = sum(self.used_obj_flags)
        num_used_boxes = len([box for box in self.boxes if len(box['placements']) > 0])
        area_used_boxes = sum([box['box_size'][0] * box['box_size'][1] for box in self.boxes if len(box['placements']) > 0])
        return num_used_objs / num_used_boxes / area_used_boxes

    def check_termination(self):
        if sum(self.used_obj_flags) == len(self.objs):
            return True
        return False

    def reset(self):
        self.used_obj_flags = [False] * len(self.objs)
        for i in range(len(self.boxes)):
            self.boxes[i]['placements'] = []
    
    def render(self, total_reward):
        """Visualization boxes"""
        out_path = os.path.join(OUT_ROOT, f"{time.time()}_{total_reward}")
        create_folder(out_path)

        for box in self.boxes:
            box_size = box['box_size']
            img = np.zeros((box_size[1], box_size[0], 3), dtype=np.uint8)
            img_name = f"{box_size[0]}x{box_size[1]}.jpg"

            if len(box['placements']) == 0:
                continue

            for placed_obj in box['placements']:
                random_color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
                obj_size = placed_obj['obj']
                pos = placed_obj['pos']
                pos_x1, pos_y1, pos_x2, pos_y2 = pos[0] - obj_size[0] / 2, pos[1] - obj_size[1] / 2, pos[0] + obj_size[0] / 2, pos[1] + obj_size[1] / 2
                img = cv2.rectangle(img, (int(pos_x1), int(pos_y1)), (int(pos_x2), int(pos_y2)), random_color, -1)

            cv2.imwrite(os.path.join(out_path, img_name), img)
        
        return out_path

def choose_action(state, q_table, epsilon, action_space):
    if random.uniform(0, 1) < epsilon:
        return random.choice(action_space)
    else:
        state_actions = q_table.get(state, {})
        if not state_actions:
            return random.choice(action_space)
        return max(state_actions, key=state_actions.get)

def update_q_table(q_table, state, action, reward, next_state, alpha, gamma):
    current_q = q_table.get(state, {}).get(action, 0)
    next_max_q = max(q_table.get(next_state, {}).values(), default=0)

    new_q = (1 - alpha) * current_q + alpha * (reward + gamma * next_max_q)
    
    if state not in q_table:
        q_table[state] = {}
    q_table[state][action] = new_q

# Test
if __name__ == "__main__":
    objs = [[10, 20], [20, 30], [30, 40], [40, 50], [50, 60], [60, 70], [70, 80], [80, 90], [90, 100], [100, 110], [110, 120]]
    place_obj2box = PlaceObj2Box(objs)
    
    q_table = {}
    action_space = [(i, j, (x, y)) for i in range(len(objs)) for j in range(3) for x in range(300) for y in range(300)]
    alpha = 0.1
    gamma = 0.9
    epsilon = 0.1
    # episodes = 10000
    # limit_steps = 1000

    episodes = 1
    limit_steps = 10

    history = []
    history_output_path = []
    
    for episode in tqdm(range(episodes)):
        total_reward = 0
        place_obj2box.reset()
        state = place_obj2box.state()
        
        for _ in range(limit_steps):
            action = choose_action(state, q_table, epsilon, action_space)
            obj_index, box_index, pos = action
            reward, done = place_obj2box.action(obj_index, box_index, pos)
            total_reward += reward
            next_state = place_obj2box.state()
            update_q_table(q_table, state, action, reward, next_state, alpha, gamma)
            state = next_state

            if done:
                out_path = place_obj2box.render(total_reward)
                history.append(total_reward)
                history_output_path.append(out_path)
                break

    print("len(history): ", len(history))
    print("Max reward: ", max(history))
    print("Max reward output path: ", history_output_path[np.argmax(history)])
