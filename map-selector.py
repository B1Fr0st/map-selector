#Known issues:
#-Cannot register Santa Sena Border Crossing and requires manual override, high priority (Fixed-Removed accented n from map name)
#-Occasionally cannot register Zarqwa Border Crossing and requires manual override, medium priority (Fixed-Added Zarawa Hydroelectric to map list)
#-Cannot handle joining games in progress, mostly on El Asilo.


#Note- All coordinates are for 1920x1080 screens, if you have a 1440 or 4k screen, the values will not be correct.


try:
    import pyautogui
    import pydirectinput
    import pytesseract
    import numpy as np
    import sys
    from time import sleep
except ImportError:
    print("One or more required module is not installed, required modules:\npyautogui\npydirectinput\npytesseract\nnumpy")
    exit()

playButtonCoords = [290,870]
gameModeCoords = [[190,690],[380,720]]
mapCoords = [[190,720],[450,745]]
lobbyLeaveButtonCoords = [300,930]
confirmLobbyLeaveButtonCoords = [700,660]
quickPlayCoords = [[190,700],[295,730]]

mapList = ["Farm 18","Mercado Las Almas","Breenbergh Hotel","Taraq","Crown Raceway","Embassy","El Asilo","Shoot House","Shipment","Zarqwa Hydroelectric","Al Bagra Fortress","Santa Sena Border Crossing"]
misreadMaps = ["Fl Asilo","Zarawa Hydroelectric","Al Baara Fortress"]#Maps consistently misread by the image-to-text function
mapList.extend(misreadMaps)
mapList = ["_".join(m.lower().split(" ")) for m in mapList]
#Since you'll see this function quite a bit, I'll explain it here.
#Essentially, what "_".join().split(" ") does is replace all of the spaces with underscores.
#For example, if you passed in farm 18 as input, it would return farm_18.

approvedMapList = ["Taraq","Shoot House"] #Edit this if you want to use more maps for longshots or anything else.
approvedMapList = ["_".join(m.lower().split(" ")) for m in approvedMapList]


def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

def read(coords1,coords2,index=0):
    """Takes in a pair of coords and returns any text between them."""
    try:
        image = pyautogui.screenshot(region=[coords1[0],coords1[1],coords2[0]-coords1[0],coords2[1]-coords1[1]])
    except OSError:
        print(f"Screen grab failed: Retrying with index {index}")
        return read(coords1,coords2,index+1)
    img1 = np.array(image)
    text = pytesseract.image_to_string(img1)
    return text
"""
Main Loop:
Click Quick Play (playButtonCoords)
Constantly read mapCoords. If it is in the map list but not in the approved map list, leave the game by pressing esc and confirm by pressing up twice and space.
"""
map = ""
gameMode = ""

def newGame():
    print("Escaping queue.")
    pydirectinput.click(lobbyLeaveButtonCoords[0],lobbyLeaveButtonCoords[1])
    sleep(0.1)
    pydirectinput.click(confirmLobbyLeaveButtonCoords[0],confirmLobbyLeaveButtonCoords[1])
    sleep(0.1)
    loop()
def loop(hibernate=False):
    if hibernate == False:
        pydirectinput.click(playButtonCoords[0],playButtonCoords[1])#click quick play button
        print("Joined Quick Play.")
        sleep(0.1)
        pydirectinput.click(playButtonCoords[0],playButtonCoords[1])#click find match button
        print("Matchmaking initiated; current approved maps are:", *approvedMapList,sep="\n-")
        sleep(0.1)
    elif hibernate == True:
        for i in progressbar(range(60),"Hibernating:",60):
            sleep(1)
        print("Ready to initiate matchmaking: current approved maps are:", *approvedMapList,sep="\n-")
    currentmap = "_".join(read(mapCoords[0],mapCoords[1]).lower().split(" ")).strip()
    while currentmap not in mapList:
        currentmap = "_".join(read(mapCoords[0],mapCoords[1]).lower().split(" ")).strip()
    if currentmap in mapList and currentmap not in approvedMapList:
        print(currentmap+" not in approved list; restarting queue.")
        newGame()
    elif currentmap in approvedMapList:
        print(currentmap+" in approved list;joining game and hibernating for 60 seconds.")
        loop(hibernate=True)



sleep(4)
loop()

