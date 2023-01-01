import pyautogui
import pytesseract
import pydirectinput
from PIL import ImageEnhance,Image
import numpy as np
import time
def read(coords,enhance=False):
    """Takes in a pair of coords and returns any text between them."""
    try:
        coords1 = coords[0]
        coords2 = coords[1]
        image = pyautogui.screenshot(region=[coords1[0],coords1[1],coords2[0]-coords1[0],coords2[1]-coords1[1]])
        if enhance == True:
            enh = ImageEnhance.Contrast(image)
            image = enh.enhance(2)
            image = image.convert("L")
            image = image.point(lambda x: 0 if x<200 else 255, '1')
        image.save("image.png")
    except OSError:
        print(f"Screen grab failed: Retrying with index {index}")
        return read(coords1,coords2)
    img1 = np.array(image)
    text = pytesseract.image_to_string(img1)
    return text
def screenshot(coords):
    coords1 = coords[0]
    coords2 = coords[1]
    return pyautogui.screenshot(region=[coords1[0],coords1[1],coords2[0]-coords1[0],coords2[1]-coords1[1]])
nameCoords = [[77,147],[766,214]]
descCoords = [[78,208],[784,370]]
prosCoords = [[100,410],[327,509]]
consCoords = [[364,408],[580,504]]
graphCoords = [[84,516],[462,673]]
typeCoords = [[79,27],[281,64]]

attachments = []
class attachment:
    def __init__(self,name=read(nameCoords),description=read(descCoords),type=read(typeCoords),pros=read(prosCoords),cons=read(consCoords),graph=screenshot(graphCoords)) -> None:
        self.name = "_".join("_".join(name.title().split(" ")).split("-")).replace("\n","")
        self.description = description.replace("\n"," ")
        self.type = type.lower()
        self.pros = pros
        self.cons = cons
        self.graph = graph
        graph.save(f"graphs/{self.name}.png")
    def describe(self):
        print(self.pros)
        newlinePros = "\n".join(self.pros.split("\n"))
        newlineCons = "\n".join(self.cons.split("\n"))
        return f"{self.name}:\n\nDescription:{self.description}\n\nType:{self.type}\nPros:\n{newlinePros}\nCons:\n{newlineCons}"

time.sleep(1)
for i in range(0,18):
    attachments.append(attachment(name=read(nameCoords),description=read(descCoords),type=read(typeCoords),pros=read(prosCoords),cons=read(consCoords),graph=screenshot(graphCoords)))
    pydirectinput.press("d")
    

with open("attachments.txt","w") as f:
    string = "\n-----------------------------------------------------------------------\n\n".join([x.describe() for x in attachments])
    f.write(string)
