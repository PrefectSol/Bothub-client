import random
import numpy as np

from hub.abc_bot import ABCBot


class RandomBot(ABCBot):
    def __init__(self):
        self._field_size = 10
        self._ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


    def set_state(self, state: dict = None) -> dict:
        field = [[0 for _ in range(self._field_size)] for _ in range(self._field_size)]
        ship_counter = 1
        
        for ship in self._ships:
            while True:
                x = random.randint(0, self._field_size - 1)
                y = random.randint(0, self._field_size - 1)
                direction = random.choice(("h", "v"))
                
                if direction == "h" and x + ship > self._field_size:
                    continue
                elif direction == "v" and y + ship > self._field_size:
                    continue
                if direction == "h":
                    if any(field[y][_x] != 0 for _x in range(x, x + ship)):
                        continue
                    
                    for _x in range(max(x - 1, 0), min(x + ship + 1, self._field_size)):
                        for _y in range(max(y - 1, 0), min(y + 2, self._field_size)):
                            if field[_y][_x] != 0:
                                break
                        else:
                            continue
                        break
                    else:
                        for _x in range(x, x + ship):
                            field[y][_x] = ship_counter
                        break
                else:
                    if any(field[_y][x] != 0 for _y in range(y, y + ship)):
                        continue
                    
                    for _x in range(max(x - 1, 0), min(x + 2, self._field_size)):
                        for _y in range(max(y - 1, 0), min(y + ship + 1, self._field_size)):
                            if field[_y][_x] != 0:
                                break
                        else:
                            continue
                        break
                    else:
                        for _y in range(y, y + ship):
                            field[_y][x] = ship_counter
                        break
                    
            ship_counter += 1

        return { 'field' : field }
    

    def get_action(self, state: dict) -> dict:
        array = np.array(state)
        zero_coordinates = np.argwhere(array == 0)
        random_zero = zero_coordinates[np.random.choice(zero_coordinates.shape[0])]

        return {'x' : random_zero[0], 'y' : random_zero[1]}