# Modified from https://github.com/ITCraftDevelopmentTeam/XDbot2/blob/master/src/plugins/Core/lib/FindingTheTrail/image.py

from PIL import Image
from xdbot_const import *

BLOCKS = {
    NULL: Image.open("swftt_resources/path.png").convert('RGB'),
    WALL: Image.open("swftt_resources/wall.png").convert('RGB'),
    START: Image.open("swftt_resources/user.png").convert('RGB'),
    PISTON: Image.open("swftt_resources/door.png").convert('RGB'),
    SAND: Image.open("swftt_resources/sand.png").convert('RGB'),
    COBWEB: Image.open("swftt_resources/web.png").convert('RGB'),
    TERMINAL: Image.open("swftt_resources/end.png").convert('RGB')
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