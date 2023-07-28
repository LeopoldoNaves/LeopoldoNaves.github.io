import numpy as np
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as tkFileDialog
from PIL import Image
from PIL import ImageTk
import cv2 as cv



#Usar o pack ao invés do root

#Converte a imagem para o padrao aceito pelo tkinter
#Param: imagem RGB
#Return: imagem para o padrao tkinter
def convertToTk(image):
    convertedImage = Image.fromarray(image)
    convertedImage = ImageTk.PhotoImage(convertedImage)
    return convertedImage 


###################################################################################

###################################################################################
#Classe Principal do nosso App
class App(Tk):
    selectMenu = None
    canvas = None
    sideMenu = None
    mainFrame = None
    imageLena = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Inicialiazacao da variaveis globais
        global blurCheck; blurCheck = BooleanVar(value= False)
        global blurValue; blurValue = IntVar(value = 1)

        global histogramCheck; histogramCheck = BooleanVar(value= False)

        global satCheck; satCheck = BooleanVar(value= False)
        global satValue; satValue = IntVar(value = 0)

        global bgSubCheck; bgSubCheck = BooleanVar(value= False)

        global threshCheck; threshCheck = BooleanVar(value= False)
        global lowHueValue; lowHueValue = IntVar(value = 0)
        global lowSatValue; lowSatValue = IntVar(value = 0)
        global lowLumaValue; lowLumaValue = IntVar(value = 0)
        global highHueValue; highHueValue = IntVar(value = 0)
        global highSatValue; highSatValue = IntVar(value = 0)
        global highLumaValue; highLumaValue = IntVar(value = 0)
        ####################################################
        self.title("Contador de barra fixa, Leop e Chico")
        self.resizable(0, 0)
        #inicia os estilos
        self.defStyle()

        #Inicia o mainFrame(Toda a gui vai ser implementada neste frame)
        self.mainFrame = ttk.Frame(self,style="Frame3.TFrame")
        self.mainFrame.propagate(False)
        self.mainFrame.configure(width=800, height=400)
        #Inicia o menu webcam ou video
        self.selectMenu = SelectMode(self)
        print("Mode selected:"+self.selectMenu.selectedMode.get())
        #cria todos os widgets do mainframe, sideMenu e canvas
        self.createWidgets(mode=self.selectMenu.selectedMode.get(), pathVideo = self.selectMenu.pathVideo.get())
        self.selectMenu.pack_forget()
        self.mainFrame.pack()
        
        
        #self.canvas.setThumbnail(self.selectMenu.selectedMode.get())
    

 
    def defStyle(self):
        styleManager = ttk.Style()
        styleManager.configure('sideMenu.TFrame', background='red')
        styleManager.configure('canvas.TFrame', background='green')
        styleManager.configure('Frame3.TFrame', background='gray')

    #Cria o tela principal de acrodo com a escolha do usuario.
    def createWidgets(self,mode,pathVideo):
        #Criando o side menu
        self.sideMenu = SideMenu(self.mainFrame)
        self.sideMenu.pack(side=LEFT)
        #Criando o canvas 
        self.canvas = Canvas(self.mainFrame,pathVideo, mode)
        self.canvas.pack(side=RIGHT)

####################################################################################
#Classe que define o menu incial de seleção do modo
class SelectMode(ttk.Frame):
    #selectedMode pode ter duas opcões, webcam ou um arquivo de vídeo. 
    selectedMode = None
    width = 200
    height = 50
    btnFile = None
    btnCam = None
    pathVideo = None

    def __init__(self, parent):
        super().__init__(parent)
        #Declaração de estilos
        self.defStyle()
        #algumas configurações...
        self.propagate(False)
        self.configure(width = self.width, height = self.height)
        #Botões de escolha
        self.selectedMode  = StringVar()
        self.pathVideo = StringVar()
        self.btnFile = ttk.Button(self, text="Video", style ="leave.TButton", command=lambda: self.selectedMode.set("video"))
        self.btnCam = ttk.Button(self, text="Câmera", style="leave.TButton",  command=lambda: self.selectedMode.set("webcam"))
        self.btnFile.pack(side=LEFT,fill=BOTH, expand=True)
        self.btnCam.pack(side=RIGHT,fill=BOTH, expand=True)
        self.pack()
        print("wait choose mode")
        self.wait_variable(self.selectedMode)
        #######
        if(self.selectedMode.get() == "video"):
            self.pathVideo.set(tkFileDialog.askopenfilename())
        else:
            self.pathVideo.set("none")

    def defStyle(self):
        styleManager = ttk.Style()
        styleManager.configure('leave.TButton', background='gray')
        styleManager.configure('enter.TButton', background='green')

#####################################################################################
#Classe que descreve o menu lateral onde os parametros serão alterados
class SideMenu(ttk.Frame):
    width = 300
    height = 400
    style = "sideMenu.TFrame"
    def __init__(self,parent):
        super().__init__(parent)
        self.propagate(False)
        self.configure(width = self.width, height = self.height, style = self.style)
        self.createWidgets()

    def createWidgets(self):
        title = ttk.Label(self,text = "Menu")
        title.pack(fill = X, anchor = N)

        #BLUR
        self.blurFrame = ttk.Frame(self, width = self.width)
        self.blurLabel = ttk.Label(self.blurFrame,text = "Blur")
        self.blurCheckbox = ttk.Checkbutton(self.blurFrame, variable = blurCheck, onvalue = True, offvalue= False ) 
        self.blurSlider = ttk.Scale(self.blurFrame, variable = blurValue, from_= 0 , to =10, orient = "horizontal")
        self.blurCheckbox.pack(side = LEFT)
        self.blurLabel.pack(side = LEFT)
        self.blurSlider.pack(side = RIGHT)
        self.blurFrame.pack(side=TOP,anchor = N, fill = X)

        #Histogram
        self.histogramFrame = ttk.Frame(self, width = self.width)
        self.histogramLabel = ttk.Label(self.histogramFrame,text = "Histogram equalization")
        self.histogramCheckbox = ttk.Checkbutton(self.histogramFrame, variable = histogramCheck, onvalue = True, offvalue= False ) 
        self.histogramCheckbox.pack(side = LEFT)
        self.histogramLabel.pack(side = LEFT)
        self.histogramFrame.pack(side=TOP,anchor = N, fill = X)

        #Saturation
        self.satFrame = ttk.Frame(self, width = self.width)
        self.satLabel = ttk.Label(self.satFrame,text = "Saturation")
        self.satCheckbox = ttk.Checkbutton(self.satFrame, variable = satCheck, onvalue = True, offvalue= False ) 
        self.satSlider = ttk.Scale(self.satFrame, variable = satValue, from_= -255 , to = 255, orient = "horizontal")
        self.satSlider.bind('<Double-Button-1>',lambda a: self.satSlider.set(0))
        self.satSlider.set(0)
        self.satCheckbox.pack(side = LEFT)
        self.satLabel.pack(side = LEFT)
        self.satSlider.pack(side = RIGHT)
        
        self.satFrame.pack(side=TOP,anchor = N, fill = X)

        #BGsubtractor
        self.bgSubFrame = ttk.Frame(self, width = self.width)
        self.bgSubLabel = ttk.Label(self.bgSubFrame,text = "BG Subtractor")
        self.bgSubCheckbox = ttk.Checkbutton(self.bgSubFrame, variable = bgSubCheck, onvalue = True, offvalue= False ) 
        self.bgSubCheckbox.pack(side = LEFT)
        self.bgSubLabel.pack(side = LEFT)
        self.bgSubFrame.pack(side=TOP,anchor = N, fill = X)

        #Threshold
        self.threshFrame = ttk.Frame(self, width = self.width)
        self.threshFrame1 = ttk.Frame(self.threshFrame, width = self.width)
        self.threshFrame2 = ttk.Frame(self.threshFrame, width = self.width)
        self.threshFrame3 = ttk.Frame(self.threshFrame, width = self.width)
        self.threshFrame4 = ttk.Frame(self.threshFrame, width = self.width)
        self.threshFrame5 = ttk.Frame(self.threshFrame, width = self.width)
        self.threshFrame6 = ttk.Frame(self.threshFrame, width = self.width)

        self.threshLabel = ttk.Label(self.threshFrame,text = "Threshod")
        self.threshCheckbox = ttk.Checkbutton(self.threshFrame, variable = threshCheck, onvalue = True, offvalue= False ) 
        self.lowHueSlider = ttk.Scale(self.threshFrame1, variable = lowHueValue, from_= 0 , to =255, orient = "horizontal")
        self.lowSatSlider = ttk.Scale(self.threshFrame2, variable = lowSatValue, from_= 0 , to =255, orient = "horizontal")
        self.lowLumaSlider = ttk.Scale(self.threshFrame3, variable = lowLumaValue, from_= 0 , to =255, orient = "horizontal")
        self.highHueSlider = ttk.Scale(self.threshFrame4, variable = highHueValue, from_= 0 , to =255, orient = "horizontal")
        self.highSatSlider = ttk.Scale(self.threshFrame5, variable = highSatValue, from_= 0 , to =255, orient = "horizontal")
        self.highLumaSlider = ttk.Scale(self.threshFrame6, variable = highLumaValue, from_= 0 , to =255, orient = "horizontal")

        self.lowHueLabel = ttk.Label(self.threshFrame1, text = "lowHue  ")
        self.lowSatLabel = ttk.Label(self.threshFrame2, text = "lowSat  ")
        self.lowLumaLabel = ttk.Label(self.threshFrame3, text = "lowLuma ")
        self.highHueLabel = ttk.Label(self.threshFrame4, text = "highHue ")
        self.highSatLabel = ttk.Label(self.threshFrame5, text = "highSat ")
        self.highLumaLabel = ttk.Label(self.threshFrame6, text = "highLuma")

        self.threshFrame6.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame5.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame4.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame3.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame2.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame1.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        
        self.threshCheckbox.pack( fill=BOTH, side=LEFT)
        self.threshLabel.pack( fill=BOTH, side=LEFT)
        
        
        self.lowHueLabel.pack( expand=True, fill=X, side=LEFT)
        self.lowHueSlider.pack( expand=True, fill=X, side=LEFT)
        
        self.lowSatLabel.pack(expand=True, fill=X, side=LEFT)
        self.lowSatSlider.pack(expand=True, fill=X, side=LEFT)
        
        self.lowLumaLabel.pack(expand=True, fill=X, side=LEFT)
        self.lowLumaSlider.pack(expand=True, fill=X, side=LEFT)

        self.highHueLabel.pack(expand=True, fill=X, side=LEFT)
        self.highHueSlider.pack(expand=True, fill=X, side=LEFT)

        self.highSatLabel.pack(expand=True, fill=X, side=LEFT)
        self.highSatSlider.pack(expand=True, fill=X, side=LEFT)

        self.highLumaLabel.pack(expand=True, fill=X, side=LEFT)
        self.highLumaSlider.pack(expand=True, fill=X, side=LEFT)
        
        self.threshFrame.pack( side=TOP, fill = X)

        #
    def resize(self,width, height):
        self.width = width
        self.height = height
        self.configure(width = self.width, height = self.height)

    

    
        

####################################################################################
#Classe qeu define o canvas
class Canvas(ttk.Frame):
    width = 500
    height = 400
    canvasLabel= None
    videoPipeline = None
    style = "canvas.TFrame"
    def __init__(self,parent,path, mode):
        super().__init__(parent)
        self.propagate(False)
        self.configure(width = self.width, height = self.height, style = self.style)
        self.videoPipeline = VideoPipeline(self.width, self.height, path)
        self.canvasLabel = ttk.Label(self,width = self.width)
        self.setThumbnail(mode)
        
    
    def setThumbnail(self,mode):
        if(mode == "webcam"):
            self.play()
        else:
            self.flush(self.videoPipeline.render())
        
    #Take a image and push to screen
    def flush(self, img):
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        img = convertToTk(img)
        self.canvasLabel.configure( image = img)
        self.canvasLabel.image = img
        self.canvasLabel.pack(side=LEFT,padx=10,pady=10)

    def play(self):
        self.flush(self.videoPipeline.render())
        self.canvasLabel.after(10, self.play)
        
    
    def resize(self,width, height):
        self.width = width
        self.height = height
        self.configure(width = self.width, height = self.height)

    

###################################################################################
#Classe que defina a engine do video##
#Todos os filtros esta'o aqui
class VideoPipeline():
    cap = None
    heightCanvas = None
    widthCanvas = None
    aspectRatioCanvas = None
    path = None
    
    heightCap = None
    widthCap = None
    aspectRatioCap = None

    #facedetect
    fd = None

    #subtrator
    backSub = cv.createBackgroundSubtractorMOG2()
    def __init__(self, width, height, path):
        if(path == "none"):
            self.cap = cv.VideoCapture(0)
        else:
            self.path = path
            self.cap = cv.VideoCapture(path)
        #Capturar na maior resolucao possivel

        #Video native resolution
        self.heightCap = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT) 
        self.widthCap =  self.cap.get(cv.CAP_PROP_FRAME_WIDTH) 
        self.aspectRatioCap = self.widthCap / self.heightCap
        print("resulution:"+str(self.widthCap)+"x"+str(self.heightCap))
        #Canvas resolution
        self.heightCanvas = height
        self.widthCanvas = width
        self.aspectRatioCanvas =   self.widthCanvas / self.heightCanvas
        #facedetect
        self.fd = faceDetect()



    #Renderiza um frame do cap
    def render(self):
        img = self.cap.read(0)[1]   #Aquizicao
        img = self.autoFit(img)
        img = self.blur(img)        #blur
        img = self.histogram(img)   #histogram equalization
        img = self.saturation(img)  #saturation adjust
        img = self.bgSub(img)       #bg subtractor
        img = self.tresh(img)       #Threshold
        img = self.fd.detect(img)
        return img
    

    #faz o autofit da imagem para a resolução do Canvas
    def autoFit(self, img):
        #ajuste pela altura
        
        if self.aspectRatioCap >= self.aspectRatioCanvas:
            print("height")
            scaleFactor = self.heightCanvas / self.heightCap
            newWidth =  scaleFactor * self.widthCap
            newHeight = scaleFactor * self.heightCap 
            centerOffsetI = (int(newWidth) - int(self.widthCanvas)) / 2
            centerOffsetF = newWidth - centerOffsetI
            newRes = (int(newWidth), int(newHeight))
            img_resize = cv.resize(img, newRes, interpolation= cv.INTER_LINEAR)
            img_resize = img_resize[:, int(centerOffsetI):int(centerOffsetF),:]

        else:#Ajuste pelo comprimento
            print("width")
            scaleFactor = self.widthCanvas / self.widthCap
            newWidth =  scaleFactor * self.widthCap
            newHeight = scaleFactor * self.heightCap 
            centerOffsetI = (int(newHeight) - int(self.heightCanvas)) / 2
            centerOffsetF = newHeight - centerOffsetI
            newRes = (int(newWidth), int(newHeight))
            img_resize = cv.resize(img, newRes, interpolation= cv.INTER_LINEAR)
            img_resize = img_resize[int(centerOffsetI):int(centerOffsetF), :,:]

        return img_resize

    #Aplica o efeito blur
    def blur(self, img):
        if(blurCheck.get()):
            return cv.medianBlur(img,(blurValue.get()*2 + 1))
        else:
            return img 

    #Aplica equalizacao do histograma
    def histogram(self, img):
        if(histogramCheck.get()):
            imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            imgLuma = imgHSV[:,:,2]
            imgLuma = cv.equalizeHist(imgLuma)
            imgHSV[:,:,2] = imgLuma
            img = cv.cvtColor(imgHSV, cv.COLOR_HSV2BGR)
            return img 
        else:
            return img 
        
    #Ajuste de saturacao
    def saturation(self, img):
        if(satCheck.get()):
            imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            imgSat = imgHSV[:,:,1]
            imgSat_16 = imgSat.astype(np.int16)
            imgSat_16 += satValue.get()
            imgSat_16 = np.clip(imgSat_16,0,255)
            imgSat = imgSat_16.astype(np.uint8)
            imgHSV[:,:,1] = imgSat
            img = cv.cvtColor(imgHSV, cv.COLOR_HSV2BGR)
            print(satValue.get())
            return img 
        else:
            return img 
        
    #Aplica o efeito blur
    def bgSub(self, img):
        if(bgSubCheck.get()):
            fgMask = self.backSub.apply(img)
            masked = cv.bitwise_and(img, img, mask=fgMask)
            return masked
        else:
            return img 
    #Faz o trhreshold da imagem no pizel format HSV
    def tresh(self,img):
        if(threshCheck.get()):
            lowHue = lowHueValue.get()
            lowSat = lowSatValue.get()
            lowLuma = lowLumaValue.get()
            highHue = highHueValue.get()
            highSat = highSatValue.get()
            highLuma = highLumaValue.get()
            imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            maskThreshold = cv.inRange(imgHSV, (lowHue, lowSat, lowLuma), (highHue, highSat, highLuma))
            img = cv.bitwise_and(img, img, mask=maskThreshold)
            return img
        else:
            return img 
        
###################################################################################
#Classe do detector de face
class faceDetect():
    face_detector = None
    def __init__(self):
        self.face_detector = cv.FaceDetectorYN_create("yunet.onnx", "", (0, 0))

    def detect(self,img):
        height, width, _ = img.shape
        self.face_detector.setInputSize((width, height))
        _, faces = self.face_detector.detect(img)
        faces = faces if faces is not None else []

        for face in faces:
            box = list(map(int, face[:4]))
            color = (0, 0, 255)
            thickness = 2
            cv.rectangle(img, box, color, thickness, cv.LINE_AA)

            #landmarks = list(map(int, face[4:len(face)-1]))
            #landmarks = np.array_split(landmarks, len(landmarks) / 2)
            #for landmark in landmarks:
            #    radius = 5
            #    thickness = -1
            #    cv.circle(img, landmark, radius, color, thickness, cv.LINE_AA)
                

            confidence = face[1]+ face[3]
            confidence = "{:.2f}".format(confidence)
            position = (box[0], box[3] + 10)
            font = cv.FONT_HERSHEY_SIMPLEX
            scale = 0.5
            thickness = 2
            cv.putText(img, confidence, position, font, scale, color, thickness, cv.LINE_AA)

        return img
    
        
    


if __name__ == "__main__":
    app = App()
    app.mainloop()


