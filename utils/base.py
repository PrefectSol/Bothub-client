import os

from datetime import datetime

from utils.status import StatusCode


# from hub.TicTacToe.tictactoe import TicTacToe
# from hub.SeaBattle.seabattle import SeaBattle

class Base:
    def __init__(self, log_dir: str):
        os.mkdir(log_dir)
        
        self._log_file = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
                # self._games = {
        #     # 'TicTacToe' : TicTacToe,
        #     'SeaBattle' : SeaBattle
        # }
        
        # self.log(f'Available games: {list(self._games.keys())}')


    def log(self, msg: str, status: StatusCode = StatusCode.Unknown):
        with open(self._log_file, 'a') as file:
            file.write(f'[{datetime.now()}] --- [{status.name}:{status.value}] --- {msg }\n')

    
    # @property
    # def games(self):
    #     return self._games;    