import swftt_const as SW
import xdbot_const as XDbot
import xdbot_search
import swftt_image
import json
import PIL.Image as I
import numpy as np
import copy

DETECT_MODE = "similar"
SIMILAR_THRESHOLD = 0.5

# image_reflection = {
#     SW.PATH: np.array(I.open("swftt_resources/path.png").convert('RGB')),
#     SW.WALL: np.array(I.open("swftt_resources/wall.png").convert('RGB')),
#     SW.USER: np.array(I.open("swftt_resources/user.png").convert('RGB')),
#     SW.PORTAL: np.array(I.open("swftt_resources/portal.png").convert('RGB')),
#     SW.DOOR: np.array(I.open("swftt_resources/door.png").convert('RGB')),
#     SW.SAND: np.array(I.open("swftt_resources/sand.png").convert('RGB')),
#     SW.WEB: np.array(I.open("swftt_resources/web.png").convert('RGB')),
#     SW.END: np.array(I.open("swftt_resources/end.png").convert('RGB'))
# }

image_reflection = {
    XDbot.NULL: np.array(I.open("swftt_resources/path.png").convert('RGB')),
    XDbot.WALL: np.array(I.open("swftt_resources/wall.png").convert('RGB')),
    XDbot.START: np.array(I.open("swftt_resources/user.png").convert('RGB')),
    # PORTAL: np.array(I.open("swftt_resources/portal.png").convert('RGB')), # 不支持
    XDbot.PISTON: np.array(I.open("swftt_resources/door.png").convert('RGB')),
    XDbot.SAND: np.array(I.open("swftt_resources/sand.png").convert('RGB')),
    XDbot.COBWEB: np.array(I.open("swftt_resources/web.png").convert('RGB')),
    XDbot.TERMINAL: np.array(I.open("swftt_resources/end.png").convert('RGB'))
}

if DETECT_MODE == "similar":
    from skimage.metrics import structural_similarity as ssim
    def compare_image(img1, img2, threshold=SIMILAR_THRESHOLD):
        if img1.shape != img2.shape:
            return False
        s = ssim(img1, img2, channel_axis=2, multichannel=True)
        return s >= threshold
elif DETECT_MODE == "equal":
    def compare_image(img1, img2):
        return np.array_equal(img1, img2)
else:
    print("Invalid DETECT_MODE.")
    exit()

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
            crop_type = -1
            for _type in image_reflection:
                if compare_image(image_reflection[_type], np.array(crop_image)):
                    crop_type = _type
                    break
            if crop_type == -1:
                print("Invalid image content.")
                if DETECT_MODE == "equal":
                    print("You may change the DETECT_MODE to 'similar' if the image is not clear.")
                exit()
            if crop_type == XDbot.START or crop_type == XDbot.TERMINAL:
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
print("Solution: "+"".join([SW.DIRECTIONS[i] for i in solution[0]]))

if input("Render gif for the solution? (y/n): ") != "y":
    exit()

temp_imgs = []
for i in range(len(solution[0])+1):
    temp_map = copy.deepcopy(solution[1][i])
    temp_map[solution[2][i][0]][solution[2][i][1]] = XDbot.START
    print("Saved game map",i,":",temp_map)
    temp_imgs.append(swftt_image.generate(temp_map))
temp_imgs[0].save("temp.gif", save_all=True, append_images=temp_imgs[1:], duration=500, loop=0)
print("Gif saved as temp.gif")