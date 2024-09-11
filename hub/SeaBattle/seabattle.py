import random
import re
import numpy as np
import os

from hub.game import Game


class SeaBattle(Game):
    def __init__(self, settings):
        self._players_count = 2
        self._field_size = 10
        self._is_playing = True
        self._is_next = True
        self._winner = ""
        self._clients = []
        self._fields = []
        self._viewed_fields = []
        self._last_action = {"x": -1, "y": -1}

        if settings["first move"] == 1 or settings["first move"] == 2:
            self._move = int(settings["first move"]) - 1
        else:
            self._move = random.randint(0, 1)
        self._save_fmove = self._move

    def add_client(self, bot_impl) -> bool:
        if len(self._clients) < self._players_count:
            match = re.search("class (\\w+)", bot_impl)
            if not match:
                return False

            exec(bot_impl)
            bot = eval(match.group(1))
            self._clients.append(bot())

            return True

        return False

    def set_state(self):
        self._is_playing = True
        self._is_next = True
        self._winner = ""
        self._last_action = {"x": -1, "y": -1}
        self._move = self._save_fmove
        self._fields.clear()
        self._viewed_fields.clear()

        self._fields.append(self._clients[0].set_state()["field"])
        self._fields.append(self._clients[1].set_state()["field"])

        self._viewed_fields.append(
            np.zeros((self._field_size, self._field_size), dtype=int)
        )
        self._viewed_fields.append(
            np.zeros((self._field_size, self._field_size), dtype=int)
        )

    def get_log(self) -> dict:
        result = {
            "is_playing": self._is_playing,
            "winner": self._winner,
            "move": self._move,
            "next": self._is_next,
            "last_action_x": int(self._last_action["x"]),
            "last_action_y": int(self._last_action["y"]),
            "field_player_0": self.__get_field_str(self._fields[0]),
            "field_player_0_viewed": self.__get_field_str(self._viewed_fields[0]),
            "field_player_1": self.__get_field_str(self._fields[1]),
            "field_player_1_viewed": self.__get_field_str(self._viewed_fields[1]),
        }

        return result

    def step(self):
        viewed_field = self._viewed_fields[self._move]
        self._last_action = self._clients[self._move].get_action(viewed_field)

        self._is_next = self.__calc_field()
        self.__check_winner()

        if self._is_playing and self._is_next:
            self._move = (self._move + 1) % 2

    def __get_field_str(self, field):
        field_str = os.linesep
        for row in field:
            field_str += " ".join(f"{num:2d}" for num in row) + os.linesep

        return field_str

    def __calc_field(self):
        isNext = False
        x = self._last_action["x"]
        y = self._last_action["y"]

        if self._fields[(self._move + 1) % 2][x][y] == 0:
            self._viewed_fields[self._move][x][y] = -1
            isNext = True
        elif self._fields[(self._move + 1) % 2][x][y] > 0:
            self._fields[(self._move + 1) % 2][x][y] = -2
            self._viewed_fields[self._move][x][y] = -2

            if self.__is_ship_destroyed(x, y):
                self.__mark_around_destroyed_ship(x, y)

        return isNext

    def __mark_around_destroyed_ship(self, x, y):
        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        ship_cells = [(x, y)]
        for dx, dy in directions[:4]:
            nx, ny = x + dx, y + dy
            while (
                0 <= nx < self._field_size
                and 0 <= ny < self._field_size
                and self._fields[(self._move + 1) % 2][nx][ny] == -2
            ):
                ship_cells.append((nx, ny))
                nx, ny = nx + dx, ny + dy

        for sx, sy in ship_cells:
            for dx, dy in directions:
                nx, ny = sx + dx, sy + dy
                if (
                    0 <= nx < self._field_size
                    and 0 <= ny < self._field_size
                    and self._fields[(self._move + 1) % 2][nx][ny] == 0
                ):
                    self._viewed_fields[self._move][nx][ny] = -1

    def __is_ship_destroyed(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        ship_cells = [(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < self._field_size and 0 <= ny < self._field_size:
                if self._fields[(self._move + 1) % 2][nx][ny] > 0:
                    return False
                if self._fields[(self._move + 1) % 2][nx][ny] == -2:
                    ship_cells.append((nx, ny))
                if self._fields[(self._move + 1) % 2][nx][ny] != -2:
                    break
                nx, ny = nx + dx, ny + dy

        return len(ship_cells) <= 4 and all(
            self._fields[(self._move + 1) % 2][sx][sy] == -2 for sx, sy in ship_cells
        )

    def __check_winner(self):
        if all(
            all(cell <= 0 for cell in row) for row in self._fields[(self._move + 1) % 2]
        ):
            self._winner = self._move
            self._is_playing = False
