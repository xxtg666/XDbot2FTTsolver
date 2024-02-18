import os
from xdbot_const import *
import xdbot_search
import xdbot_image
import json
import PIL.Image as I
import numpy as np
import copy

def images_are_equal(img1, img2):
    return np.array_equal(img1, img2)

image_reflection = {
    NULL: np.array(I.open("resources/stone_bricks.png").convert('RGB')),
    WALL: np.array(I.open("resources/bricks.png").convert('RGB')),
    START: np.array(I.open("resources/iron_block.png").convert('RGB')),
    TERMINAL: np.array(I.open("resources/diamond_block.png").convert('RGB')),
    PISTON: np.array(I.open("resources/piston_top.png").convert('RGB')),
    SAND: np.array(I.open("resources/sand.png").convert('RGB')),
    COBWEB: np.array(I.open("resources/cobweb.png").convert('RGB'))
}

mode = input("Enter the map form (1 for json, 2 for image): ")
if mode == "1":
    try:
        ftt_map = json.loads(input("Enter the map: "))
    except:
        print("Invalid json content.")
        exit()
elif mode == "2":
    ftt_image_path = input("Enter the image path: ")
    ftt_image = I.open(ftt_image_path)
    ftt_map_width = int(ftt_image.size[0]/16)
    ftt_map_height = int(ftt_image.size[1]/16)
    ftt_map = []
    for i in range(ftt_map_height):
        row = []
        for j in range(ftt_map_width):
            area = (j*16, i*16, (j+1)*16, (i+1)*16)
            crop_image = ftt_image.crop(area)
            crop_type = UNKNOWN
            for _type in image_reflection:
                if images_are_equal(image_reflection[_type], np.array(crop_image)):
                    crop_type = _type
                    break
            if crop_type == UNKNOWN:
                print("Invalid image content.")
                exit()
            if crop_type == START or crop_type == TERMINAL:
                del image_reflection[crop_type]
            row.append(crop_type)
        ftt_map.append(row)
    print("Map: "+str(ftt_map))
else:
    print("Invalid mode.")
    exit()

try:
    solution = xdbot_search.search(ftt_map)
    if not solution:
        raise Exception
except Exception:
    print("Cannot find the solution.")
    exit()
print("Solution: "+"".join([DIRECTIONS[i] for i in solution[0]]))

if input("Render gif for the solution? (y/n): ") != "y":
    exit()

temp_imgs = []
for i in range(len(solution[0])+1):
    temp_map = copy.deepcopy(solution[1][i])
    temp_map[solution[2][i][0]][solution[2][i][1]] = START
    print("Saved game map",i,":",solution[1][i])
    temp_imgs.append(xdbot_image.generate(temp_map))
    temp_imgs[0].save("temp.gif", save_all=True, append_images=temp_imgs[1:], duration=500, loop=0)
print("Gif saved as temp.gif")