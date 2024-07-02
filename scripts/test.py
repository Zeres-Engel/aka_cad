import copy
import numpy as np

class Object:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Box:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.placements = []  # List of (object, position)

    def can_place(self, obj, position):
        # Check if the object can be placed at the specified position
        if position[0] + obj.width > self.width or position[1] + obj.height > self.height:
            return False
        for placed_obj, placed_pos in self.placements:
            if not (position[0] + obj.width <= placed_pos[0] or 
                    position[0] >= placed_pos[0] + placed_obj.width or 
                    position[1] + obj.height <= placed_pos[1] or 
                    position[1] >= placed_pos[1] + placed_obj.height):
                return False
        return True

    def place_object(self, obj, position):
        if self.can_place(obj, position):
            self.placements.append((obj, position))
            return True
        return False

class State:
    def __init__(self, objects, boxes):
        self.objects = objects  # List of objects not yet placed
        self.boxes = boxes  # List of boxes with their current placements

class Action:
    def __init__(self, object_index, box_index, position):
        self.object_index = object_index  # Index of the object to be placed
        self.box_index = box_index  # Index of the box where the object will be placed
        self.position = position  # Position in the box (x, y) where the object will be placed

class Environment:
    def __init__(self, initial_state):
        self.state = initial_state

    def step(self, action):
        new_state = self.transition(self.state, action)
        reward = self.calculate_reward(new_state)
        done = self.check_done(new_state)
        self.state = new_state
        return new_state, reward, done

    def transition(self, state, action):
        new_state = copy.deepcopy(state)
        object_to_place = new_state.objects.pop(action.object_index)
        box = new_state.boxes[action.box_index]
        if not box.place_object(object_to_place, action.position):
            raise ValueError("Invalid placement")
        return new_state

    def calculate_reward(self, state):
        # Reward can be based on the number of boxes used and space utilization
        total_boxes = len(state.boxes)
        empty_space = sum([self.calculate_empty_space(box) for box in state.boxes])
        return -total_boxes - empty_space * 0.01

    def calculate_empty_space(self, box):
        used_space = sum([obj.width * obj.height for obj, _ in box.placements])
        total_space = box.width * box.height
        return total_space - used_space

    def check_done(self, state):
        return len(state.objects) == 0  # Done when all objects are placed

# Example usage
initial_objects = [Object(30, 40), Object(50, 50), Object(60, 70), Object(20, 30)]
initial_boxes = [Box(100, 100), Box(200, 200), Box(150, 150)]
initial_state = State(initial_objects, initial_boxes)
env = Environment(initial_state)

action = Action(0, 0, (10, 10))
new_state, reward, done = env.step(action)
print(f"New State: {new_state}, Reward: {reward}, Done: {done}")
