#Known issues:
#-Cannot register Santa Sena Border Crossing and requires manual override, high priority (Fixed-Removed accented n from map name)
#-Occasionally cannot register Zarqwa Border Crossing and requires manual override, medium priority (Fixed-Added Zarawa Hydroelectric to map list)







import pyautogui
import pydirectinput
from PIL import Image
import pytesseract
import numpy as np
from time import sleep
playButtonCoords = [290,870]
gameModeCoords = [[190,690],[380,720]]
mapCoords = [[190,720],[450,745]]
confirmLobbyLeaveButtonCoords = [700,660]
quickPlayCoords = [[190,700],[295,730]]

mapList = ["Farm 18","Mercado Las Almas","Breenbergh Hotel","Taraq","Crown Raceway","Embassy","El Asilo","Shoot House","Shipment","Zarqwa Hydroelectric","Al Bagra Fortress","Santa Sena Border Crossing"]
misreadMaps = ["Fl Asilo","Zarawa Hydroelectric","Al Baara Fortress"]#Maps consistently misread by the image-to-text function
mapList.extend(misreadMaps)
mapList = ["_".join(m.lower().split(" ")) for m in mapList]
approvedMapList = ["Taraq","Shoot House"]
approvedMapList = ["_".join(m.lower().split(" ")) for m in approvedMapList]

import sys
def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
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
    pydirectinput.click(300,930)
    sleep(0.1)
    pydirectinput.click(700,660)
    sleep(0.1)
    loop()
def loop(hibernate=False):
    currentmap = ""
    oldmap = ""
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
    oldmap = currentmap
    currentmap = "_".join(read(mapCoords[0],mapCoords[1]).lower().split(" ")).strip()
    
    while currentmap not in mapList:
        if oldmap != currentmap:
            print(currentmap)
        currentmap = "_".join(read(mapCoords[0],mapCoords[1]).lower().split(" ")).strip()
    if currentmap in mapList and currentmap not in approvedMapList:
        print(currentmap+" not in approved list; restarting queue.")
        newGame()
    elif currentmap in approvedMapList:
        print(currentmap+" in approved list;joining game and hibernating for 60 seconds.")
        loop(hibernate=True)



sleep(4)
loop()

