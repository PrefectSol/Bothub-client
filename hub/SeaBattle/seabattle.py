import json
import random
import re
import numpy as np

from hub.game import Game


class SeaBattle(Game):
    def __init__(self, settings):
        self._players_count = 2
        self._field_size = 10
        self._is_playing = True
        self._winner = ''
        self._clients = []
        self._fields = []
        
        with open(settings, 'r') as file:
            self._config = json.load(file)
            
        if self._config['first move'] == 1 or self._config['first move'] == 2:
            self._move = int(self._config['first move']) - 1
        else:
            self._move = random.randint(0, 1)
       
    
    def add_client(self, client_info, bot_impl) -> bool:
        if len(self._clients) < self.players_count:
            match = re.search('class (\\w+)', bot_impl)
            if not match:
                return False
            
            exec(bot_impl)
            bot = eval(match.group(1))
            self._clients.append((client_info, bot()))
            
            return True
        
        return False

    
    def set_state(self):        
        self._fields.append(self._clients[0][1].set_state()['field'])
        self._fields.append(self._clients[1][1].set_state()['field'])
            
    
    def step(self):
        enemy_field = self._fields[(self._move + 1) % 2]
        action = self._clients[self._move][1].make_action(enemy_field)
        
        self._fields[self._move], isNext = self.__calc_field(self._fields[self._move], action)
        self.__check_winner()
                
        if self._is_playing and isNext:
            self._move = (self._move + 1) % 2

    
    def get_state(self) -> dict:
        if len(self._clients) < 2:
            return {'field1' : [], 'field2' : [],
                    'playerMove' : 'awaiting',
                    'winner': ''}
        
        return {'field1' : self._fields[0], 'field2' : self._fields[1],
                'playerMove' : self._clients[self._move][0]['from'],
                'winner': self._winner}
        
    

    def __calc_field(self, field, action):
        isNext = False
        x = action['x']
        y = action['y']

        if field[x][y] == 0:
            field[x][y] = -1
            isNext = True
        elif field[x][y] > 0:
            ship_id = field[x][y]
            field[x][y] = -1
            if not any(field[i][j] == ship_id for i in range(max(0, x-1), min(10, x+2))
                                        for j in range(max(0, y-1), min(10, y+2))):
                for i in range(max(0, x-2), min(10, x+3)):
                    for j in range(max(0, y-2), min(10, y+3)):
                        if field[i][j] == 0:
                            field[i][j] = -1
                            
                    
        return field, isNext


    def __check_winner(self):
        if all(all(cell <= 0 for cell in row) for row in self._fields[self._move]):
            self._winner = self._clients[self._move][0]['from']
            self._is_playing = False
