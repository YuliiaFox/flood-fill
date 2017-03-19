import tkFileDialog, time, copy
from tkColorChooser import askcolor
import PIL.Image
from Tkinter import *
from PIL import ImageTk

def DeleteCanva(canva):
    canva.delete('all')

def OpenImage(canva):
    way = tkFileDialog.askopenfilename()
    global img
    img = PIL.Image.open(way)
    img1 = ImageTk.PhotoImage(img)
    DeleteCanva(canva)
    canva.create_image(0, 0, image=img1, anchor=NW)
    canva.pack(expand=YES, fill=BOTH)
    width, height = img.size
    #sys.setrecursionlimit(width*width*height*height)
    canva.mainloop()

def AskColor():
    acolor = askcolor()
    global color
    color= acolor[0]
    color=list(color)
    color.insert(3, 0)
    color=tuple(color)
    print color

def GetCoord(event):
    x = event.x
    y = event.y
    ProcessingImage(x,y)
    #FillingImg(x, y, img, color, old_color, stack)

    print "done"

def ProcessingImage(x, y):
    global old_color
    old_color = img.getpixel((x, y))
    stack = [[x,y]]
    i = 1

    img.putpixel((stack[0][0],stack[0][1]), color)
    while stack:
        stack.pop()
        check(x+i, y, color, old_color, stack)
        check(x-i, y, color, old_color, stack)
        check(x, y + i, color, old_color, stack)
        check(x, y - i, color, old_color, stack)
        i += 1
        img.save("new.png")

def check(i,j,color,old_color,stack):
        current_color = img.getpixel((i, j))
        if(current_color != color and current_color == old_color):
            img.putpixel((i,j), color)
            stack.append([i,j])



def FillingImg(x, y, img, color, old_color, stack):

    if img.getpixel((x, y)) == old_color:
        img.putpixel((x, y), color)
        time.sleep(1)
        root.update_idletasks()
        root.update()
        time.sleep(0.01)
    else:
        return 1
    FillingImg(x + 1, y, img, color, old_color)
    FillingImg(x - 1, y, img, color, old_color)
    FillingImg(x, y + 1, img, color, old_color)
    FillingImg(x, y - 1, img, color, old_color)

def CreatingFrame():
    global root
    root = Tk()
    root.geometry("900x700")
    canva = Canvas(root)
    canva.after(100)
    MenuBar = Menu(root)

    MenuBar.add_command(label='Open Image', command=(lambda: OpenImage(canva)))
    MenuBar.add_command(label='Choise color', command=(lambda: AskColor()))
    MenuBar.add_command(label='Clear', command=(lambda: DeleteCanva(canva)))
    MenuBar.add_command(label='Quit!', command=sys.exit)
    root.config(menu=MenuBar)

    hbar = Scrollbar(root, orient=HORIZONTAL) #scrolling
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=canva.xview)
    vbar = Scrollbar(root, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canva.yview)

    canva.bind('<Double-1>', GetCoord)
    root.mainloop()

CreatingFrame()
