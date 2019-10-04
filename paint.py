# Paint project 2018/2019
from pygame import *
from math import *
from random import randint
import glob
from tkinter import *
from tkinter.colorchooser import *

init()
font.init()
display.set_caption('Pokemon Paint')

dimensions = width, height = 1200, 800
screen = display.set_mode(dimensions)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

wallpaper = transform.scale(image.load("Misc/temp.png"), (1200, 800))  # Decorative wallpaper
screen.blit(wallpaper, (0, 0))

# Save and load stuff
root = Tk()
root.withdraw()


# Tool class for all tools, as well as other buttons such as the save and load or add color buttons
class Tool:
    def __init__(self, button, size, pic, tool, chosen=False):
        self.button = button  # The rect of the button
        self.size = size  # The size of the tool, i.e. thickness
        self.pic = pic
        self.tool = tool  # Name of the tool
        self.chosen = chosen  # Boolean variable of whether this tool is selected or not. (Default not selected)

    # Function draws the tool button border
    def redraw(self): 
        screen.set_clip(0, 0, 1200, 800)
        if self.chosen:  # If it is the chosen button, the border is red
            draw.rect(screen, RED, self.button, 2)
        elif self.button.collidepoint(mx, my):  # If the button is hovered over but not chosen, it is green
            draw.rect(screen, GREEN, self.button, 2)
        else:  # If it is neither hovered over or chosen, it is black
            draw.rect(screen, BLACK, self.button, 2)


# Tool class for sub-tools (stamps, polygon tools)
# Pretty much the same as the Tool class+
class SubTool(Tool):
    def __init__(self, button, size, pic, tool, chosen=False):
        Tool.__init__(self, button, size, pic, tool, chosen)

    def redraw(self):  # Blits the button on the screen, and uses the same highlighting method as the Tool class
        screen.set_clip(0, 575, 1200, 325)
        screen.blit(self.pic, (self.button[0], self.button[1])) 
        # Highlighting of tools
        if self.chosen: 
            draw.rect(screen, RED, self.button, 2)
        elif self.button.collidepoint(mx, my):
            draw.rect(screen, GREEN, self.button, 2)
        else:
            draw.rect(screen, BLACK, self.button, 2)


# Class for color palette
class Palette:
    def __init__(self, button, col, chosen=False):
        self.button = button  # Button rect
        self.col = col  # Color of the palette
        self.chosen = chosen  # Boolean variable of whether this color button is selected or not. (Default not selected)

    def redraw(self):
        draw.rect(screen, self.col, self.button)
        # Highlighting of palette (no hover)
        if self.chosen:
            draw.rect(screen, RED, self.button, 1)
        else:
            draw.rect(screen, BLACK, self.button, 1)


# Class for background buttons
class Background:
    def __init__(self, button, pic, small_pic, chosen=False):
        self.button = button  # Button rect
        self.pic = pic  # Actual background
        self.small_pic = small_pic  # Preview pic on button
        self.chosen = chosen  # Boolean variable of whether this background button is selected or not. (Default not selected)

    def redraw(self):
        screen.set_clip(0, 575, 1200, 325)
        if self.small_pic is not None:
            screen.blit(self.small_pic, (self.button[0], self.button[1]))
        # Highlighting of background buttons
        if self.chosen:
            draw.rect(screen, RED, self.button, 2)
        elif self.button.collidepoint(mx, my):
            draw.rect(screen, GREEN, self.button, 2)
        else:
            draw.rect(screen, BLACK, self.button, 2)


toolList = []  # List of tools
polygonTools = []  # Polygon sub-tools

# Initializing variables
selected = "pencil"  # Tool currently selected, default of pencil
selectedColor = BLACK

# Creating tool objects
pencil = Tool(Rect(25, 80, 70, 70), 1, "Tool_Images/pencil_tool.png", "pencil", True)
toolList.append(pencil)

eraser = Tool(Rect(115, 80, 70, 70), 10, "Tool_Images/eraser_tool.png", "eraser")
toolList.append(eraser)

brush = Tool(Rect(205, 80, 70, 70), 10, "Tool_Images/brush_tool.png", "brush")
toolList.append(brush)

line = Tool(Rect(25, 170, 70, 70), 1, "Tool_Images/line_tool.png", "line")
toolList.append(line)

highlighter = Tool(Rect(115, 170, 70, 70), 10, "Tool_Images/highlighter_tool.png", "highlighter")
toolList.append(highlighter)

spray = Tool(Rect(205, 170, 70, 70), 10, "Tool_Images/spray_tool.png", "spray")
toolList.append(spray)

bucket = Tool(Rect(25, 260, 70, 70), 1, "Tool_Images/bucket_tool.png", "bucket")
toolList.append(bucket)

dropper = Tool(Rect(115, 260, 70, 70), 1, "Tool_Images/dropper_tool.png", "dropper")
toolList.append(dropper)

polygon = Tool(Rect(205, 260, 70, 70), 1, "Tool_Images/rectangle_tool.png", "polygon")
toolList.append(polygon)

rectangle = SubTool(Rect(490, 680, 70, 70), 1, image.load("Tool_Images/rectangle_tool.png"), "rectangle", True)
polygonTools.append(rectangle)

filledRect = SubTool(Rect(570, 680, 70, 70), 1, image.load("Tool_Images/filled_rectangle_tool.png"), "filled rectangle")
polygonTools.append(filledRect)

ellipse = SubTool(Rect(650, 680, 70, 70), 1, image.load("Tool_Images/ellipse_tool.png"), "ellipse")
polygonTools.append(ellipse)

filledEllipse = SubTool(Rect(730, 680, 70, 70), 1, image.load("Tool_Images/filled_ellipse_tool.png"), "filled ellipse")
polygonTools.append(filledEllipse)

customPolygon = SubTool(Rect(810, 680, 70, 70), 1, image.load("Tool_Images/custom_polygon_tool.png"), "custom polygon")
polygonTools.append(customPolygon)

background = Tool(Rect(25, 350, 70, 70), 1, "Tool_Images/background_tool.png", "background")
toolList.append(background)

stamp = Tool(Rect(115, 350, 70, 70), 1, "Tool_Images/stamp_tool.png", "stamp")
toolList.append(stamp)

clear = Tool(Rect(205, 350, 70, 70), 1, "Tool_Images/clear_tool.png", "clear")
toolList.append(clear)

undoTool = Tool(Rect(50, 500, 70, 70), 1, "Tool_Images/undo_tool.png", "undo")
toolList.append(undoTool)

redoTool = Tool(Rect(180, 500, 70, 70), 1, "Tool_Images/redo_tool.png", "redo")
toolList.append(redoTool)

save = Tool(Rect(300, 585, 40, 40), 1, "Tool_Images/save.png", "save")
toolList.append(save)

load = Tool(Rect(350, 585, 40, 40), 1, "Tool_Images/load.png", "load")
toolList.append(load)

addColor = Tool(Rect(875, 585, 40, 40), 1, "Tool_Images/add_color_tool.png", "addColor")
toolList.append(addColor)

# Blitting tool button images onto screen
for t in toolList:
    screen.blit(image.load(t.pic), (t.button[0], t.button[1]))

selectedPolygon = "rectangle"  

fixedSize = ["pencil", "line", "polygon"]  # Tools that have a fixed size
noSize = ["", "dropper", "background", "bucket"]  # Tools that have no size
noSelection = [undoTool, redoTool, save, addColor, load, clear]  # Tools that cannot be chosen

# Creating stamps
stampFiles = sorted(glob.glob("Stamps/stamp*.png"))
loadedStamps = [image.load(i) for i in stampFiles]
stampList = [SubTool(Rect(350 + 110*i, 670, 100, 100), 25, transform.scale(loadedStamps[i], (100, 100)), i)
             for i in range(len(stampFiles))]  # List of stamp objects. Used when any specific stamp is referenced
selectedStamp = 0  # Default stamp
stampList[0].chosen = True

# Creating backgrounds
backgroundFiles = sorted(glob.glob("Backgrounds/background*.jpg"))  # List of background files
smallBackgroundFiles = sorted(glob.glob("Backgrounds/small_background*.jpg"))  # List of preview background files

# List of background objects. Used whenever a specific background is referenced
backgroundList = [Background(Rect(330 + 110*i, 670, 100, 67), image.load(backgroundFiles[i]),
                  image.load(smallBackgroundFiles[i])) for i in range(len(backgroundFiles))]

backgroundList[0].chosen = True  # Initial chosen background of blank
selectedBackground = 0

# Creating colors
basicColors = [(255, 255, 255), (195, 195, 195), (88, 88, 88), (0, 0, 0), (136, 0, 27), (236, 28, 36), (255, 137, 39),
               (255, 202, 24), (253, 236, 166), (255, 242, 0), (196, 255, 14), (14, 209, 69), (140, 255, 251),
               (0, 168, 243), (63, 72, 204), (184, 61, 186), (255, 174, 200), (185, 122, 86)]  # Fixed colors

customColors = [WHITE for i in range(len(basicColors))]  # Colours that can be changed with custom color picker
# List of color objects. Used whenever the color palette is referenced
colorList = [Palette(Rect(490 + i*21, 585, 20, 20), basicColors[i]) for i in range(len(basicColors))] + \
            [(Palette(Rect(490 + i*21, 606, 20, 20), WHITE)) for i in range(len(basicColors))]


colorList[3].chosen = True  # Default colour of black

toolDict = {  # dictionary of tools
            "pencil": pencil,
            "eraser": eraser,
            "brush": brush,
            "line": line,
            "rectangle": rectangle,
            "filled rectangle": filledRect,
            "ellipse": ellipse,
            "filled ellipse": filledEllipse,
            "highlighter": highlighter,
            "dropper": dropper,
            "polygon": polygon,
            "spray": spray,
            "bucket": bucket,
            "background": background,
            "stamp": stamp,
            "undo": undoTool,
            "redo": redoTool,
            "save": save,
            "load": load,
            "clear": clear
            }

# Drawing the canvas
canvasRect = Rect(300, 80, 750, 500)
draw.rect(screen, WHITE, canvasRect)

# Misc decorations
pokemonText = image.load("Misc/pokemon_paint_text.png")
screen.blit(pokemonText, (450, 5))

# Information box
infoRect = Rect(20, 590, 270, 190)
draw.rect(screen, (150, 150, 150), infoRect)
draw.rect(screen, BLACK, infoRect, 2)  # Info rect border
cambria = font.SysFont("Arial", 32)  # Cambria doesn't work on the school computers for some reason so it's arial
screen.blit(cambria.render("Tool:", True, BLACK), (25, 590))  # Selected tool
screen.blit(cambria.render("Color:", True, BLACK), (25, 640))  # Selected colour
screen.blit(cambria.render("Size:", True, BLACK), (25, 690))  # Size of selected tool
screen.blit(cambria.render("Location:", True, BLACK), (25, 740))  # Pixel location of mouse on canvas
info = screen.copy().subsurface((20, 590, 280, 190)) 

mx, my = 0, 0


# Function to update the information box
def update_info():
    """
    This function updates the information in the information box. This includes the selected color, size of the
    selected tool, pixel location, etc. This function blits the update information onto the screen whenever any
    of the information changes, such as if the user switches tools. If the polygon tool tab is open, different
    information is blitted, otherwise, the aforementioned infomration is blitted.
    """
    screen.set_clip(infoRect)
    screen.blit(info, (20, 590))
    draw.rect(screen, selectedColor, (120, 640, 40, 40))  # Color preview box
    global mx, my
    if canvasRect.collidepoint(mx, my):  # Displays the pixel location of mouse
        screen.blit(cambria.render("{0}, {1} px".format(mx - 300, my - 80), True, BLACK), (140, 740))

    # If the polygon tab is opened, different info is to be blitted
    if selected == "polygon":  
        screen.blit(cambria.render(selectedPolygon, True, BLACK), (100, 590))  # Displays selected polygon tool
        if selectedPolygon == "rectangle" or selectedPolygon == "ellipse":
            screen.blit(cambria.render(str(toolDict[selectedPolygon].size), True, BLACK), (100, 690))  # Size of tool
            return
    # Normal info if polygon tab is not opened
    else: 
        screen.blit(cambria.render(selected, True, BLACK), (100, 590))  # Displays selected tool
    if selected not in noSize:
        screen.blit(cambria.render(str(toolDict[selected].size), True, BLACK), (100, 690))  # Displays size of tool

    screen.set_clip(0, 0, 1200, 800)


update_info()  # Initial update of info


# Bucket tool fill
def fill(surface, x, y, new):
    """
    The fill function takes in 4 arguments, the surface (screen), the x and y positions of the inital click, and the
    new color (selectedColor). A pixel array is created, and the flood fill algorithm is applied to it. The function
    uses a queue beginning with the inital click, and checks if it is the same color as the old color. If it is, the 4
    adjacent pixels are also sampled, until the queue is empty or more pixels than the size of the canvas have been
    sampled.
    """
    pxarray = PixelArray(surface)  # Pixel array of canvas
    pending = [(x, y)]  # Pixels to be sampled
    old = pxarray[x, y]  # Old color
    count = 0  # Counter variable for number of pixels sampled
    while pending:
        x, y = pending.pop()  # Checking the last pixel in the array
        if pxarray[x, y] != old:  # If that pixel is the old color, we must check its neighbours
            continue
        pxarray[x, y] = new  # Set the pixel to the new color
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]  
        for d in dirs:
            pending.append((x+d[0], y+d[1]))  # Appending the neighbouring pixels to the queue
        count += 1
        if count > 750 * 500:  # Breaks if the number of pixels sampled is greater than the canvas
            break
    del pxarray  


# Undo and redo arrays
undoArray = [(screen.copy().subsurface((300, 80, 750, 500)), 0)]
redoArray = []


# Undo function
def undo():
    """
    The undo function blits the screenshot that is the last element of the undoArray onto the canvas. The
    screenshot is blitted onto the canvas, and the undone image is appended into the redo array.
    Whenever the user changes the background, instead of just a screenshot being appended to the undoArray,
    a tuple that includes both the screenshot and the old background is appended instead. The function
    checks if the element is a tuple, and if it is changes the selectedBackground to what it was previously,
    as well as appending a tuple instead of just a screenshot.
    """
    if len(undoArray) > 0:
        is_tuple = False  # Variable indicating whether the element was a tuple
        # If the element is a tuple, it means that the background was changed with the undo
        if type(undoArray[-1]) is tuple:
            # Changes the value of the selected background
            global selectedBackground 
            current_background = selectedBackground  
            selectedBackground = undoArray[-1][1]
            undoArray[-1] = undoArray[-1][0]
            screen.set_clip(300, 630, 900, 170)

            # Changing the old chosen background to un-chosen and switching the newly chosen one to chosen.
            for b in backgroundList:
                b.chosen = False
            backgroundList[selectedBackground].chosen = True  

            # Redrawing the backgrounds
            for b in backgroundList:
                b.redraw()
            is_tuple = True

        if selected != "background":
            screen.blit(blank, (300, 630))  # Blitting the blank bottom if the selected tool is not background
        screen.set_clip(canvasRect)
        global screenShot
        screenShot = screen.copy()

        # If the undoArray element was a tuple, then the image that is being blitted to the
        # redo array also needs to be a tuple with the background
        if is_tuple:
            redoArray.append((screenShot.subsurface((300, 80, 750, 500)), current_background))
        else:
            redoArray.append(screenShot.subsurface((300, 80, 750, 500)))

        screen.blit(undoArray.pop(), (300, 80))
        screen.set_clip(0, 0, 1200, 800)


def redo():
    """
     The redo function is almost identical to the undo function, except that it blits screenshots from the redoArray
     and appends to the undoArray.
    """
    if len(redoArray) > 0:
        is_tuple = False
        if type(redoArray[-1]) is tuple:
            global selectedBackground
            selectedBackground = redoArray[-1][1]
            redoArray[-1] = redoArray[-1][0]
            screen.set_clip(300, 630, 900, 170)
            for b in backgroundList:
                b.chosen = False
            backgroundList[selectedBackground].chosen = True
            for b in backgroundList:
                b.redraw()
            is_tuple = True

        if selected != "background":
            screen.blit(blank, (300, 630))
        
        screen.set_clip(canvasRect)
        global screenShot
        screenShot = screen.copy()

        if is_tuple:
            undoArray.append((screenShot.subsurface((300, 80, 750, 500)), selectedBackground))
        else:
            undoArray.append(screenShot.subsurface((300, 80, 750, 500)))
        screen.blit(redoArray[-1], (300, 80))
        redoArray.pop()
        screen.set_clip(0, 0, 1200, 800)


# Initializing variables
sx, sy = mouse.get_pos()  # Original x, y coordinates for line and polygon tools
screenShot = screen.copy()  # Screenshot of canvas
firstClick = False  # Whether it is the first click of a polygon for custom polygon tool or not
activePolygon = False  # Whether the custom polygon tool is active or not
oPoint = (0, 0)  # Original point of a polygon for custom polygon tool
myClock = time.Clock()
blank = screen.copy().subsurface((300, 630, 900, 170))  # Blank tab at bottom of screen.
zDown = False  
yDown = False

running = True
while running:
    clicked = False
    zDown = False
    ctrlDown = False
    yDown = False
    escDown = False
    omx, omy = mx, my  # Old mx and old my for pencil tool
    for evt in event.get():
        if evt.type == QUIT:
            running = False

        if evt.type == KEYDOWN:
            if evt.key == K_z:
                zDown = True

            if evt.key == K_y:
                yDown = True
                
            if evt.key == K_ESCAPE:  # If escape is pressed, it deselects the currently selected tool
                screen.set_clip(0, 0, 300, 800)
                for i in toolList:
                    i.chosen = False
                selected = ""
                update_info()

        if evt.type == KEYUP:
            if evt.key == K_z:
                zDown = False

            if evt.key == K_y:
                yDown = False

        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                clicked = True

                # Dealing with custom polygon tool
                if selected == "polygon" and selectedPolygon == "custom polygon" and canvasRect.collidepoint(mx, my):
                    activePolygon = True
                    if not firstClick:
                        oPoint = mouse.get_pos()
                    firstClick = True

                sx, sy = mouse.get_pos()  # Starting position of the line and used in polygon tool
                screenShot = screen.copy()  # Screen capture

            # Increases the size of the selected tool if the mouse is scrolled up
            if evt.button == 4:
                if toolDict[selected].size < 50 and selected not in fixedSize:
                    toolDict[selected].size += 1
                elif selected == "polygon" and selectedPolygon == "rectangle" and rectangle.size < 50:
                    rectangle.size += 1
                elif selected == "polygon" and selectedPolygon == "ellipse" and ellipse.size < 50:
                    ellipse.size += 1

                update_info()

            # Decreases the size of the selected tool if the mouse is scrolled down
            elif evt.button == 5:
                if toolDict[selected].size > 1 and selected not in fixedSize:
                    toolDict[selected].size -= 1
                elif selected == "polygon" and selectedPolygon == "rectangle" and rectangle.size > 1:
                    rectangle.size -= 1
                elif selected == "polygon" and selectedPolygon == "ellipse" and ellipse.size > 1:
                    ellipse.size -= 1

                update_info()

        if evt.type == MOUSEBUTTONUP:
            osx, osy = sx, sy
            # Appending to the undoArray when the mouse is released after any canvas action
            if canvasRect.collidepoint(mx, my) and selected != "" and selected != "background" \
                    and selected != "dropper":
                undoArray.append(screenShot.subsurface((300, 80, 750, 500)))

    mx, my = mouse.get_pos()  
    mb = mouse.get_pressed()

    keys = key.get_pressed()
    if keys[K_LCTRL] or keys[K_RCTRL]:
        ctrlDown = True

    # CTRL + Z undo shortcut
    if ctrlDown and zDown:
        undo()
    # CTRL + Y redo shortcut
    elif ctrlDown and yDown:
        redo()

    # For each tool, it checks if the tool is selected, hovered over, or neither, and draws the appropriate border.
    # If any tool has been clicked, it changes the chosen property for all tools to false, and then changes the clicked
    # tool to be true.
    for t in toolList:
        screen.set_clip(0, 0, 1200, 800)
        if t.button.collidepoint(mx, my) and clicked and t not in noSelection:
            for i in toolList:  # All tools in the toolList have their chosen property set to false
                i.chosen = False
            t.chosen = True  # The clicked tool has their chosen property set to true
            selected = t.tool
            screen.set_clip(0, 575, 1200, 325)
            screen.blit(blank, (300, 630))
            update_info()
        t.redraw()

    # For each color, it checks if the color is selected, or not, and draws the appropriate border.
    for c in colorList:
        screen.set_clip(0, 575, 1200, 325)
        if c.button.collidepoint(mx, my) and clicked:
            for i in colorList:
                i.chosen = False
            c.chosen = True
            selectedColor = c.col
            update_info()
        c.redraw()

    # If the polygon button is pressed, the polygon sub-tools are drawn
    if polygon.button.collidepoint(mx, my) and clicked:
        screen.set_clip(0, 0, 1200, 800)
        for p in polygonTools:
            p.redraw()

    # Checking if undo button is clicked
    if clicked and undoTool.button.collidepoint(mx, my):
        undo()

    # Checking if redo button is clicked
    if clicked and redoTool.button.collidepoint(mx, my):
        redo()

    # Save button
    if clicked and save.button.collidepoint(mx, my):
        try:
            fname = filedialog.asksaveasfilename(defaultextension=".png")  # User enters file name to be saved
            image.save(screen.subsurface(canvasRect), fname)  # Saves image to computer
        except:
            print("Saving error")

    # Load button
    if clicked and load.button.collidepoint(mx, my):
        try:
            f = filedialog.askopenfilename()
            loaded = transform.scale(image.load(f), (750, 500))
            screen.set_clip(canvasRect)
            screen.blit(loaded, (300, 80))
        except:
            print("Loading error")

    # Add custom color button
    if clicked and addColor.button.collidepoint(mx, my):
        """
        The custom color picker works by opening the color picker prompt and allowing the user to select a color. The 
        colorList is then looped through to check what the index of the selected color is and then the customColors list
        is looped through to check what 
        """
        newCol, newColAsString = askcolor(title='Custom Color Picker')  # Opens custom color prompt
        hasWhite = False  # Whether or not the custom colours still have an empty slot
        index = 0  # Index of selected color
        if newCol is None:
            pass
        else:
            for i in range(len(colorList)):
                if colorList[i].chosen:
                    index = i  
                    break

            # If there is an empty color slot, the first one is changed to the chosen color
            if WHITE in customColors:
                customColors[customColors.index(WHITE)] = newCol
                selectedColor = newCol
                index = len(basicColors) + customColors.index(WHITE) - 1  # Index of color to be chosen
                hasWhite = True

            # If there is no empty custom color slot, the selected color is changed if it is custom,
            # otherwise the color is changed
            if not hasWhite and index > 17:
                customColors[index - len(basicColors)] = newCol
                selectedColor = newCol
            elif not hasWhite and index < 17:
                customColors[-1] = newCol
                selectedColor = newCol


            # Updating list of color objects
            colorList = [Palette(Rect(490 + i * 21, 585, 20, 20), basicColors[i]) for i in range(len(basicColors))] + \
                        [(Palette(Rect(490 + i * 21, 606, 20, 20), customColors[i])) for i in range(len(basicColors))]

            colorList[index].chosen = True

        # Clear screen button
    if clicked and clear.button.collidepoint(mx, my):
        screen.set_clip(canvasRect)
        screen.blit(backgroundList[selectedBackground].pic, (300, 80))  # Blits the selected background to clear screen

    # Usage of tools
    if mb[0] and canvasRect.collidepoint(mx, my):
        screen.set_clip(canvasRect)
        if selected == "pencil":
            draw.line(screen, selectedColor, (omx, omy), (mx, my), 1)

        if selected == "eraser":
            dist = ((omx - mx) ** 2 + (omy - my) ** 2) ** 0.5  # Distance between the cursor between frames
            if dist == 0:
                dist = 1

            # Erases for each pixel in the distance
            for i in range(1, int(dist) + 1):
                dotX = int(omx + i * (mx - omx) / dist - eraser.size//2)
                dotY = int(omy + i * (my - omy) / dist - eraser.size//2)
                if selectedBackground == 0:  # If no background, simply draw a white circle
                    draw.circle(screen, WHITE, (dotX, dotY), eraser.size)
                else:
                    try:
                        w, h = eraser.size, eraser.size  # Width and height of subsurface to be erased
                        # If the eraser is on the edge of the canvas where a fully sized eraser subsurface would be off
                        # the screen, the appropriate size to fit the edge is calculated.
                        if mx < 300 + eraser.size // 2:  # Left edge
                            dotX = 300
                            w = mx - 300 + eraser.size // 2
                        elif mx > 1050 - eraser.size // 2:  # Right edge
                            dotX = mx - eraser.size // 2
                            w = 1050 - mx + eraser.size // 2
                        if my < 80 + eraser.size // 2:  # Top edge
                            dotY = 80
                            h = my - 80 + eraser.size // 2
                        elif my > 580 - eraser.size // 2:  # Bottom edge
                            dotY = my - eraser.size // 2
                            h = 580 - my + eraser.size // 2

                        # Creating and bliting background subsurface
                        sample = backgroundList[selectedBackground].pic.subsurface((dotX - 300, dotY - 80, w, h))
                        screen.blit(sample, (dotX, dotY))
                    except ValueError:
                        pass

        if selected == "brush":
            # Uses pythagorean distance and draws a circle for each pixel along the distance
            dist = ((omx - mx) ** 2 + (omy - my) ** 2) ** 0.5
            if dist == 0:
                dist = 1
            for i in range(1, int(dist) + 1):
                dotX = int(omx + i * (mx - omx) / dist)
                dotY = int(omy + i * (my - omy) / dist)
                draw.circle(screen, selectedColor, (dotX, dotY), brush.size)
            
        if selected == "line":
            screen.blit(screenShot, (0, 0))
            draw.line(screen, selectedColor, (mx, my), (sx, sy), line.size)

        if selected == "highlighter" and (mx != omx or my != omy):
            hSize = highlighter.size  # Variable for size of highlighter to save typing
            highlight = Surface((2*hSize, 2*hSize), SRCALPHA)  # Creating a highlight surface
            draw.circle(highlight, (selectedColor[0], selectedColor[1], selectedColor[2], 8), (hSize, hSize), hSize)

            # Uses pythagorean distance and draws a circle for each pixel along the distance
            dist = ((mx - omx) ** 2 + (my - omy) ** 2) ** 0.5
            for i in range(1, int(dist) + 1):
                dotX = int(omx + i * (mx - omx) / dist - hSize)
                dotY = int(omy + i * (my - omy) / dist - hSize)
                screen.blit(highlight, (dotX, dotY))

        if selected == "bucket":
            fill(screen, mx, my, selectedColor)

        if selected == "dropper":
            # Gets the colour at the clicked pixel and deselects the currently selected color button
            selectedColor = screen.get_at((mx, my))
            for c in colorList:
                c.chosen = False
            update_info()

        if selected == "spray":
            # Randomly generates a pixel within a circle of the tool size radius using polar coordinates. A random angle
            # and hypotenuse is generated, and its x, y value is calculated using sin and cos.
            for i in range(15*spray.size):
                angle = randint(0, 359) 
                rad = randint(1, spray.size)
                screen.set_at((int(mx + rad * cos(angle)), int(my + rad * sin(angle))), selectedColor)

        if selected == "polygon":
            if selectedPolygon == "rectangle":
                """
                If the dimensions of the rectangle are negative (i.e. if mx > sx or my > sy, they are made positive
                with the top left corner translated the amount of the dimensions.
                This concept is also used in the filled rectangle, ellipse, and filled ellipse tools
                """
                screen.blit(screenShot, (0, 0))
                dotX, dotY = mx, my  # Top left corner of rectangle
                w = abs(sx - mx)  # Width of rectangle
                h = abs(sy - my)  # Height of rectangle
                if sx - mx < 0:   # Horizontal translation
                    dotX -= w
                if sy - my < 0:   # Vertical translation
                    dotY -= h
                # If the rectangle is too small to have a hole in it,
                # a smaller filled rectangle is drawn instead
                if w < rectangle.size or h < rectangle.size:
                    draw.rect(screen, selectedColor, (dotX, dotY, w, h))
                else:  # A bunch of smaller rectangles are drawn to simulate a rectangle with the specified thickness
                    for i in range(rectangle.size):
                        draw.rect(screen, selectedColor, (dotX + i, dotY + i, w - 2 * i, h - 2 * i), 1)

            if selectedPolygon == "filled rectangle":
                screen.blit(screenShot, (0, 0))
                # Same dimension calculation as rectangle tool
                dotX, dotY = mx, my
                w = abs(sx - mx)  # Width of rectangle
                h = abs(sy - my)  # Height of rectangle
                if sx - mx < 0:
                    dotX -= w
                if sy - my < 0:
                    dotY -= h
                draw.rect(screen, selectedColor, (dotX, dotY, w, h))
                
            if selectedPolygon == "ellipse":
                # Same dimension calculation as rectangle tool
                screen.blit(screenShot, (0, 0))
                dotX, dotY = mx, my
                w = abs(sx - mx)  # Width of ellipse rect
                h = abs(sy - my)  # Height of ellipse rect
                if sx - mx < 0:
                    dotX -= w
                if sy - my < 0:
                    dotY -= h

                # Blits 5 ellipses of the specified thickness slightly offset of each other
                dirs = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]  # Offsets of the ellipses
                for i in range(len(dirs)):
                    eliRect = Rect(dotX + dirs[i][0], dotY + dirs[i][1], w, h)
                    eliRect.normalize()
                    try:
                        draw.ellipse(screen, selectedColor, eliRect, ellipse.size)
                    except ValueError:  # If a unfilled ellipse cannot be drawn a filled one is drawn instead
                        draw.ellipse(screen, selectedColor, eliRect)

            if selectedPolygon == "filled ellipse":
                # Same dimension calculation as rectangle tool
                screen.blit(screenShot, (0, 0))
                dotX, dotY = mx, my
                w = abs(sx - mx)
                h = abs(sy - my)
                if sx - mx < 0:
                    dotX -= w
                if sy - my < 0:
                    dotY -= h
                eliRect = Rect(dotX, dotY, w, h)
                eliRect.normalize()
                draw.ellipse(screen, selectedColor, eliRect)

        if selected == "stamp":
            screen.blit(screenShot, (0, 0))
            pendingStamp = transform.scale(loadedStamps[selectedStamp], (int(100*(1 + 0.03*stamp.size)),
                                                                         int(100*(1 + 0.03*stamp.size))))
            screen.blit(pendingStamp, (mx - (100*(1 + 0.03*stamp.size)) // 2, my - (100*(1 + 0.03*stamp.size)) // 2))

    if selected == "polygon":
        # For each tool, it checks if the tool is selected, hovered over, or neither, and draws the appropriate border.
        # If any tool has been clicked, it changes the chosen property for all tools to false, and then changes the
        # clicked tool to be true.
        for p in polygonTools:
            if p.button.collidepoint(mx, my) and clicked:
                screen.set_clip(0, 575, 1200, 325)
                for i in polygonTools:
                    i.chosen = False
                p.chosen = True
                selectedPolygon = p.tool
                update_info()
            p.redraw()

            """
            For the custom polygon, first it checks if it is the first click of a polygon, and if so it starts a new 
            active polygon and stores the original point. If not, it will add to the already existing polygon. A 2 point
            polygon is drawn from sx, sy to mx, my. When the user clicks, the line is drawn and they can draw a new 
            one. When the user right clicks, a line is drawn to the original point, and the active polygon is disabled.
            """
            if selectedPolygon == "custom polygon" and activePolygon and canvasRect.collidepoint(mx, my):
                screen.set_clip(canvasRect)
                screen.blit(screenShot, (0, 0))

                # Drawing the line
                if canvasRect.collidepoint(sx, sy):
                    draw.polygon(screen, selectedColor, [(sx, sy), (mx, my)], 1)

                # Closing the line
                if mb[2] or escDown:
                    activePolygon = False
                    firstClick = False
                    screen.blit(screenShot, (0, 0))
                    draw.polygon(screen, selectedColor, [(sx, sy), oPoint], 1)  # Line to original point

    if selected != "polygon" or (selected == "polygon" and selectedPolygon != "custom polygon"):
        # If the tool is changed while there is an active polygon, it is disabled
        activePolygon = False
        firstClick = False
        
    if selected == "background":
        # For each background, it checks if the background is selected, hovered over, or neither, and draws the
        # appropriate border. If any background has been clicked, it changes the chosen property for all backgrounds to
        # false and then changes the clicked background to be true.
        for b in backgroundList:
            if b.button.collidepoint(mx, my) and clicked:
                screen.set_clip(0, 0, 1200, 800)
                for i in backgroundList:
                    i.chosen = False
                b.chosen = True
                screen.blit(b.pic, (300, 80))
                undoArray.append((screenShot.subsurface((300, 80, 750, 500)), selectedBackground))  # Appending to undo
                selectedBackground = backgroundList.index(b)
                update_info()
            b.redraw()

    if selected == "stamp":
        # For each stamp, it checks if the stamp is selected, hovered over, or neither, and draws the appropriate border
        # If any stamp has been clicked, it changes the chosen property for all stamps to false, and then changes the
        # clicked stamp to be true.
        for s in stampList:
            if s.button.collidepoint(mx, my) and clicked:
                screen.set_clip(0, 575, 1200, 375)
                for i in stampList:
                    i.chosen = False
                s.chosen = True
                selectedStamp = s.tool
                update_info()  
            s.redraw()
    
    update_info()
    myClock.tick(60)
    display.flip() 

quit()
