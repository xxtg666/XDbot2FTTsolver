# Modified from https://github.com/ITCraftDevelopmentTeam/XDbot2/blob/master/src/plugins/Core/lib/FindingTheTrail/image.py

from PIL import Image
from xdbot_const import *

BLOCKS = {
    NULL: Image.open("resources/stone_bricks.png"),
    WALL: Image.open("resources/bricks.png"),
    START: Image.open("resources/iron_block.png"),
    TERMINAL: Image.open("resources/diamond_block.png"),
    PISTON: Image.open("resources/piston_top.png"),
    SAND: Image.open("resources/sand.png"),
    COBWEB: Image.open("resources/cobweb.png")
}

def generate(game_map: list[list[int]]):
    image = Image.new("RGB", (len(game_map[0]) * 16, len(game_map) * 16), (51, 255, 255))
    for row in range(len(game_map)):
        for column in range(len(game_map[row])):
            item = game_map[row][column]
            x0 = column * 16
            y0 = row * 16
            image.paste(BLOCKS[item], (x0, y0))
    return image

if __name__ == "__main__":
    import json
    ftt_map = json.loads(input("Enter the map: "))
    generate(ftt_map).show()