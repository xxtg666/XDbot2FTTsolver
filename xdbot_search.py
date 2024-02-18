# Modified from https://github.com/ITCraftDevelopmentTeam/XDbot2/blob/master/src/plugins/Core/lib/FindingTheTrail/search.py

from typing import TypedDict
from xdbot_const import *
import copy

def get_item_by_pos(pos: tuple[int, int], game_map: list[list[int]]) -> int:
    return game_map[pos[0]][pos[1]]

def get_start_pos(game_map: list[list[int]]) -> tuple[list[list[int]], tuple[int, int]]:
    for r in range(len(game_map)):
        for c in range(len(game_map[r])):
            if get_item_by_pos((r, c), game_map) == START:
                game_map[r][c] = NULL
                return game_map, (r, c)
    raise ValueError

DR = (-1, 1, 0, 0)
DC = (0, 0, -1, 1)

def get_moved_pos(original_pos: tuple[int, int], direction: int) -> tuple[int, int]:
    return (original_pos[0] + DR[direction - 1], original_pos[1] + DC[direction - 1])

def is_item_moveable(item: int) -> bool:
    return item in [NULL, TERMINAL, PISTON, COBWEB]

def get_moveable_direction(
    game_map: list[list[int]], pos: tuple[int, int]
) -> list[int]:
    return [
        i
        for i in range(1, 5)
        if is_item_moveable(get_item_by_pos(get_moved_pos(pos, i), game_map))
    ]

def get_back_direction(direction: int) -> int:
    return {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}[direction]

def parse_sand(game_map: list[list[int]], pos: tuple[int, int]) -> list[list[int]]:
    _id = id(game_map)
    for d in [UP, DOWN, RIGHT, LEFT]:
        p = get_moved_pos(pos, d)
        i = get_item_by_pos(p, game_map)
        if i == SAND:
            if id(game_map) == _id:
                game_map = copy.deepcopy(game_map)
            game_map[p[0]][p[1]] = NULL
    return game_map

def move(
    game_map: list[list[int]], pos: tuple[int, int], direction: int
) -> tuple[list[list[int]], tuple[int, int]]:
    _id = id(game_map)
    while True:
        pos = get_moved_pos(pos, direction)
        item = get_item_by_pos(pos, game_map)
        if not is_item_moveable(item):
            return game_map, get_moved_pos(pos, get_back_direction(direction))
        elif item == TERMINAL:
            return game_map, pos
        elif item == COBWEB:
            return game_map, pos
        elif item == PISTON:
            if id(game_map) == _id:
                game_map = copy.deepcopy(game_map)
            game_map[pos[0]][pos[1]] = WALL

class QueueItem(TypedDict):
    game_map: list[list[int]]
    direction: int
    original_pos: tuple[int, int]
    path: list[int]

def search(game_map: list[list[int]], max_step: int = 12):
    game_map, start_pos = get_start_pos(game_map)
    queue: list[QueueItem] = [
        {"direction": d, "game_maps": [game_map], "original_pos": start_pos, "path": [d], "saved_pos": [start_pos]}
        for d in get_moveable_direction(game_map, start_pos)
    ]
    while True:
        try:
            item = queue.pop(0)
        except IndexError:
            return False
        if get_item_by_pos(item["original_pos"], item["game_maps"][-1]) == TERMINAL:
            return (item["path"][:-1], item["game_maps"], item["saved_pos"])
        game_map, pos = move(item["game_maps"][-1], item["original_pos"], item["direction"])
        game_map = parse_sand(game_map, item["original_pos"])
        queue.extend(
            [
                {
                    "direction": d,
                    "original_pos": pos,
                    "game_maps": item["game_maps"] + [game_map],
                    "path": item["path"] + [d],
                    "saved_pos": item["saved_pos"] + [pos]
                }
                for d in get_moveable_direction(game_map, pos)
            ]
        )
        if len(item["path"]) >= max_step:
            return False