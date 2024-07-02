import os
import shutil
import cv2
import time
import numpy as np
from tqdm import tqdm

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
        self.objs = sorted(objs, key=lambda x: x[0] * x[1], reverse=True)
        self.used_obj_flags = [False] * len(objs)
        self.boxes = [
            {'box_size': [100, 100], 'placements': []},
            {'box_size': [200, 200], 'placements': []},
            {'box_size': [300, 300], 'placements': []}
        ]
        
    def state(self):
        return self.objs, self.used_obj_flags, self.boxes

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
            # print("Cannot place object")
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
    
    def render(self):
        """Visualization boxes"""
        out_path = os.path.join(OUT_ROOT, f"{str(time.time()).replace('.', '_')}")
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

# Test
if __name__ == "__main__":
    objs = [[10, 20], [20, 30], [30, 40], [40, 50], [50, 60], [60, 70], [70, 80], [80, 90], [90, 100], [100, 110], [110, 120]]
    place_obj2box = PlaceObj2Box(objs)

    history = []
    history_output_path = []
    limit_steps = 1000
    for _ in tqdm(range(10000)):
        total_reward = 0
        for _ in range(limit_steps):
            obj_index = np.random.randint(0, len(objs))
            box_index = np.random.randint(0, 3)
            pos = [np.random.randint(0, 300), np.random.randint(0, 300)]

            reward, done = place_obj2box.action(obj_index, box_index, pos)
            total_reward += reward

            if done:
                out_path = place_obj2box.render()
                history.append(total_reward)
                history_output_path.append(out_path)
                break        

        place_obj2box.reset()

    print("len(history): ", len(history))
    print("Max reward: ", max(history))
    print("Max reward output path: ", history_output_path[np.argmax(history)])