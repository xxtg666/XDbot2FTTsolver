import xdbot_const as XDbot
import mtsftt_const as MTS
import json

def convert(item):
    return {
        XDbot.NULL: MTS.NULL,
        XDbot.WALL: MTS.WALL,
        XDbot.START: MTS.NULL,
        XDbot.TERMINAL: MTS.NULL,
        XDbot.PISTON: MTS.PISTON,
        XDbot.SAND: MTS.SAND,
        XDbot.COBWEB: MTS.COBWEB,
        MTS.NULL: XDbot.NULL,
        MTS.WALL: XDbot.WALL,
        MTS.PISTON: XDbot.PISTON,
        MTS.SAND: XDbot.SAND,
        MTS.COBWEB: XDbot.COBWEB
    }[item]

mode = input("Enter the mode (1 for MTS -> XDbot, 2 for XDbot -> MTS): ")
if mode == "1":
    try:
        mts_ftt = json.loads(input("Enter the MTS FTT map: ").replace("'",'"').replace("null",'"null"'))
    except:
        print("Invalid json content.")
        exit()
    for i in range(len(mts_ftt["map"])):
        for j in range(len(mts_ftt["map"][i])):
            mts_ftt["map"][i][j] = convert(mts_ftt["map"][i][j])
    xdbot_ftt = mts_ftt["map"]
    xdbot_ftt[mts_ftt["player"][0]][mts_ftt["player"][1]] = XDbot.START
    xdbot_ftt[mts_ftt["target"][0]][mts_ftt["target"][1]] = XDbot.TERMINAL
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