import _tkinter
import cv2
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import PIL
from PIL import *
from PIL import ImageTk ,Image
import os


class ImageViewerGUI:
    def __init__(self , root):
        self.root = root
        self.root.bind("<Right>",self.callNext)
        self.root.bind("<Left>",self.callPrev)
        self.root.bind("<Up>", self.callzoomIn)
        self.root.bind("<Down>",self.callzoomOut)

        self.windowWidth = self.root.winfo_screenwidth()
        self.windowHeight = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0"%(self.windowWidth,self.windowHeight))


        # Canvas
        self.canvas = Canvas(self.root,height=self.windowHeight , width =self.windowWidth)
        self.canvas.pack(expand=YES , fill = BOTH)
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        # MenuBar
        self.menuBar(self.root)


    def menuBar(self,root):
        self.menubar = Menu(root)

        # File menu
        self.filemenu = Menu(self.menubar , tearoff = 0)
        self.filemenu.add_command(label = "Open Image" , command = lambda: self.openImage(root))
        self.filemenu.add_command(label = "Exit" , command = root.quit)
        self.menubar.add_cascade(label = "File" , menu = self.filemenu)

        #View menu
        self.viewMenu = Menu(root)

        self.zoomMenu = Menu(self.viewMenu , tearoff = 0)
        self.zoomMenu.add_command(label = "Zoom in" , command = self.zoomIN)
        self.zoomMenu.add_command(label = "Zoom out" , command = self.zoomOut)

        self.navigate = Menu(self.viewMenu , tearoff = 0)
        self.navigate.add_command(label = "Next" , command = self.next)
        self.navigate.add_command(label = "Previous" , command = self.previous)


        self.viewMenu.add_cascade(label = "Zoom" , menu = self.zoomMenu)
        self.viewMenu.add_cascade(label = "Navigate", menu = self.navigate)

        self.menubar.add_cascade(label = "View" , menu = self.viewMenu)

        root.config(menu = self.menubar)

    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def callzoomIn(self,event):
        self.zoomIN()

    def callzoomOut(self,event):
        self.zoomOut()

    def callNext(self,event):
        self.next()

    def callPrev(self,event):
        self.previous()

    def openImage(self ,root):
        self.selectedFilename = filedialog.askopenfilename(initialdir="/",title = "Select Image",filetypes = [("jpeg files",("*.jpeg","*.jpg")),("png files","*.png")])
        if len(self.selectedFilename) > 0:
            self.imagesDir()


        print("OpenImage called")



    def zoomIN(self):
        try:
            if self.selectedImagePos > -1:
                image = cv2.imread(self.imagesPathList[self.selectedImagePos],cv2.IMREAD_UNCHANGED)
                if self.zoomRate < 2:
                    print(self.zoomRate)
                    self.zoomRate = self.zoomRate+0.1
                    self.currentWidth = int(self.zoomRate * self.imgWidth)
                    self.currentHeight = int(self.zoomRate * self.imgHeight)

                dsize = (self.currentWidth,self.currentHeight)
                output = cv2.resize(image, dsize , interpolation=cv2.INTER_LINEAR)
                self.x = self.windowWidth / 2 - self.currentWidth / 2
                self.y = self.windowHeight / 2 - self.currentHeight / 2
                output = cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
                image = Image.fromarray(output)
                tk_image = ImageTk.PhotoImage(image)
                self.canvas.create_image(self.x, self.y, anchor=NW, image=tk_image)
                self.canvas.image = tk_image
        except:
            self.displayMsg("Image is not selected")

        print("clicked zoom in ")


    def zoomOut(self):
        try:
            if self.selectedImagePos > -1:
                image = cv2.imread(self.imagesPathList[self.selectedImagePos],cv2.IMREAD_UNCHANGED)
                if self.zoomRate > 1:
                    self.zoomRate = self.zoomRate-0.1
                    self.currentWidth = int(self.zoomRate * self.imgWidth)
                    self.currentHeight = int(self.zoomRate * self.imgHeight)

                dsize = (self.currentWidth,self.currentHeight)
                output = cv2.resize(image, dsize , interpolation=cv2.INTER_AREA)

                self.x = self.windowWidth / 2 - self.currentWidth / 2
                self.y = self.windowHeight / 2 - self.currentHeight / 2
                output = cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
                image = Image.fromarray(output)
                tk_image = ImageTk.PhotoImage(image)
                self.canvas.create_image(self.x, self.y, anchor=NW, image=tk_image)
                self.canvas.image = tk_image
        except:
            self.displayMsg("Image is not selected")

        print("clicked zoom out")

    def displayMsg(self,Msg):
        messagebox.showerror("Error",Msg)

    def next(self):
        try:
            if self.selectedImagePos > -1:
                if self.selectedImagePos+1 < len(self.imagesPathList):
                    self.selectedImagePos = self.selectedImagePos+1
                    self.canvas.xview_moveto(self.or_x)
                    self.canvas.yview_moveto(self.or_y)
                    image = Image.open(self.imagesPathList[self.selectedImagePos])
                    tk_image = ImageTk.PhotoImage(image)
                    self.imgWidth = tk_image.width()
                    self.imgHeight = tk_image.height()
                    if self.imgWidth > self.windowWidth or self.imgHeight > self.windowHeight:
                        image.thumbnail((self.windowWidth, self.windowHeight))
                        self.imgWidth, self.imgHeight = image.size

                    self.x = self.windowWidth / 2 - self.imgWidth / 2
                    self.y = self.windowHeight / 2 - self.imgHeight / 2
                    tk_image = ImageTk.PhotoImage(image)
                    self.canvas.create_image(self.x, self.y, anchor=NW, image=tk_image)
                    self.canvas.image = tk_image
                    self.zoomRate = 1
                    self.currentWidth = self.imgWidth
                    self.currentHeight = self.imgHeight
        except:
            self.displayMsg("Image is not selected")

        print("Next clicked")

    def previous(self):
        try:
            if self.selectedImagePos > -1:
                if self.selectedImagePos-1  > -1:
                    self.selectedImagePos = self.selectedImagePos-1
                    self.canvas.xview_moveto(self.or_x)
                    self.canvas.yview_moveto(self.or_y)
                    image = Image.open(self.imagesPathList[self.selectedImagePos])
                    tk_image = ImageTk.PhotoImage(image)
                    self.imgWidth = tk_image.width()
                    self.imgHeight = tk_image.height()
                    if self.imgWidth > self.windowWidth or self.imgHeight > self.windowHeight:
                        image.thumbnail((self.windowWidth, self.windowHeight))
                        self.imgWidth, self.imgHeight = image.size

                    self.currentWidth = self.imgWidth
                    self.currentHeight = self.imgHeight
                    self.x = self.windowWidth / 2 - self.imgWidth / 2
                    self.y = self.windowHeight / 2 - self.imgHeight / 2
                    tk_image = ImageTk.PhotoImage(image)
                    self.canvas.create_image(self.x, self.y, anchor=NW, image=tk_image)
                    self.canvas.image = tk_image
                    self.zoomRate = 1
                    self.currentWidth = self.imgWidth
                    self.currentHeight = self.imgHeight
        except:
            self.displayMsg("Image is not selected")
        print("Previous clicked")

    def imagesDir(self):
        extList = ["jpeg","jpg","png","jfif"] # accepted extensions
        self.imagesPathList = [] # list containing images path in directory
        self.dirPath = os.path.dirname(self.selectedFilename); # directory path of selected image
        self.selectedImageName = os.path.basename(self.selectedFilename) # file name of selected image
        dirFileNameList = os.listdir(self.dirPath) # list of names of files present in directory
        imageIndex = -1;
        self.selectedImagePos = -1; # selected image position in imagePathList
        if len(dirFileNameList) > 0:
            for filename in dirFileNameList: # taking files from dirFileNameList
                ext = filename.rsplit(".",1)
                if len(ext) == 2:
                    if ext[1].lower() in extList:
                        self.imagesPathList.append(os.path.join(self.dirPath,filename))
                        imageIndex = imageIndex+1;
                        if self.selectedImageName == filename:
                            self.selectedImagePos = imageIndex
        if self.selectedImagePos != -1:
            image = Image.open(self.imagesPathList[self.selectedImagePos])
            tk_image = ImageTk.PhotoImage(image)
            self.imgWidth = tk_image.width()
            self.imgHeight = tk_image.height()
            if self.imgWidth > self.windowWidth or self.imgHeight > self.windowHeight:
                image.thumbnail((self.windowWidth,self.windowHeight))
                self.imgWidth , self.imgHeight = image.size

            self.x = self.windowWidth/2 - self.imgWidth/2
            self.y = self.windowHeight/2 - self.imgHeight/2
            tk_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(self.x,self.y,anchor=NW,image = tk_image)
            self.canvas.image = tk_image
            self.zoomRate = 1
            self.currentWidth = self.imgWidth
            self.currentHeight = self.imgHeight


        self.or_x = self.canvas.xview()[0]
        self.or_y = self.canvas.yview()[0]

        print(self.imagesPathList)
        print(self.selectedImagePos)

root = Tk()
icon = ImageTk.PhotoImage(file="images.png")
root.iconphoto(False,icon)
root.title("ImageViewer")
myImageViewerGUI = ImageViewerGUI(root)
root.mainloop()