import xdbot_const as XDbot
import swftt_const as SW
import json

def convert(item):
    return {
        XDbot.NULL: SW.PATH,
        XDbot.WALL: SW.WALL,
        XDbot.START: SW.USER,
        XDbot.TERMINAL: SW.END,
        XDbot.PISTON: SW.DOOR,
        XDbot.SAND: SW.SAND,
        XDbot.COBWEB: SW.WEB,
        SW.PATH: XDbot.NULL,
        SW.WALL: XDbot.WALL,
        SW.DOOR: XDbot.PISTON,
        SW.SAND: XDbot.SAND,
        SW.WEB: XDbot.COBWEB,
        SW.END: XDbot.TERMINAL,
        SW.USER: XDbot.START
    }[item]

mode = input("Enter the mode (1 for SW -> XDbot, 2 for XDbot -> SW): ")
if mode == "1":
    try:
        sw_ftt = json.loads(input("Enter the SW FTT map: "))
    except:
        print("Invalid json content.")
        exit()
    for i in range(len(sw_ftt["map"])):
        for j in range(len(sw_ftt["map"][i])):
            sw_ftt["map"][i][j] = convert(sw_ftt["map"][i][j])
    xdbot_ftt = sw_ftt["map"]
    xdbot_ftt[sw_ftt["userPosition"]["second"]][sw_ftt["userPosition"]["first"]] = XDbot.START
    # xdbot_ftt[sw_ftt["endPosition"]["second"]][sw_ftt["endPosition"]["first"]] = XDbot.TERMINAL
    print("Converted XDbot FTT map:", xdbot_ftt)
elif mode == "2":
    print("WORK IN PROGRESS")
    exit()
    try:
        xdbot_ftt = json.loads(input("Enter the XDbot FTT map: "))
    except:
        print("Invalid json content.")
        exit()
else:
    print("Invalid mode.")
    exit()