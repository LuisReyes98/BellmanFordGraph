import pdb 	#python debugger

from tkinter import * #se importa todo de tkinter
import tkinter as tk #tkinter se declara como tk

#from tkinter import messagebox #mensajes de dialogo
import sys #para cerrar el programa despues


global numNodos
global numAristas
global vectorDeNodos
global aristaEnCreacion
global aristaAux #variable global de la arista a crear
global canvas #canvas tkinter
global panelTexto

numNodos=1 #contador de la cantidad de nodos hechos/ id arista
numAristas=1#contador de las aristas hechas / id arista
vectorDeNodos=[]#vector que contedra a todos los nodos
aristaEnCreacion=False


def _create_circle(self, x, y, r, **kwargs):#metodo que dibuja los circulos
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle #le añade a tk.Canvas el metodo create_circle

def _create_circle_arc(self, x, y, r, **kwargs):#metodo que dibuja arcos 
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc


# Paso 1: Inicializamos el arreglo de salida y destino
def initialize(graph, source):
    d = {} # Destino
    p = {} # Salida
    for node in graph:
        d[node] = float('Inf') # Iniciamos admitiendo que todos los nodos son incansables
        p[node] = None
    d[source] = 0 # Se le asigna 0 al nodo donde inicaremos
    return d, p

def relax(node, neighbour, graph, d, p):
    # Si la distancia entre el nodo y su vencino es menor que la que tengo actualmente
    if d[neighbour] > d[node] + graph[node][neighbour]:
        # Guarda esta distancia menor
        d[neighbour]  = d[node] + graph[node][neighbour]
        p[neighbour] = node


def bellman_ford(graph, source):
    global panelTexto    
    
    j = 0
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Se recorre hasta terminar
        for u in graph:
            j+= 1
            for v in graph[u]: #Para cada vecino en u
                relax(u, v, graph, d, p) #Relajamos
            panelTexto.insert(END,'Iteracion %d \n'%(j))
           
            panelTexto.insert(END,'Arreglo destino \n')
            panelTexto.insert(END,'%s \n'%(d))
            panelTexto.insert(END,'Arreglo Salida \n')
            panelTexto.insert(END,'%s \n'%(p))
    # Paso 3: se verifica si hay ciclos negativos
    for u in graph:
        for v in graph[u]:
            assert d[v] <= d[u] + graph[u][v]
    return d, p

def main():
    graph = {
         'a': {'b': -1, 'c':  4},
         'b': {'c':  3, 'd':  2, 'e':  2},
         'c': {},
         'd': {'b':  1, 'c':  5},
         'e': {'d': -3}
        }

    d,p = bellman_ford(graph,'a')
 
    print (d)
    print (p)

    mainWindow()


def mainWindow():#metodo de creacion de ventana segun pygame
    global canvas
    
    root = tk.Tk()#ventana tkinter   
    root.title("Grafos Bellman-Ford")
    
    bottomFrame= tk.Frame(root)#panel inferior
    bottomFrame.pack(side=BOTTOM)

    topFrame=tk.Frame(root)#panel superior
    topFrame.pack(side=TOP)            

    w=790 #ancho de la ventana
    h=600 #alto de la ventana
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))#el valor del string es "700x(600+x+y)" para marcar las dimensiones y la ubicacion de la ventana en el centro de la pantalla

    panelSuperior(topFrame,w,h)#crear el canvas

    arial14= ('Arial',14,"bold")#fuente de los botones

    botonCirculo= tk.Button(bottomFrame,text="Añadir Nodo",command= lambda: crearNodo(canvas),font=arial14)#boton de añadir nodos        
    botonEvaluar= tk.Button(bottomFrame,text="Evaluar Grafo",font=arial14,command=evaluateGraph)#boton de evaluar el grafo y realizar el algoritmo
    botonBorrar= tk.Button(bottomFrame,text="Borrar Todo",font=arial14,command=resetAll)#boton de borrar todo

    botonCirculo.pack(side=tk.LEFT)
    botonEvaluar.pack(side=tk.LEFT)
    botonBorrar.pack(side=tk.LEFT)

    root.mainloop()#ciclo infinito general de la ventana
    sys.exit(0)#para que el programa se cierre una vez se cierra la ventana

def panelSuperior(topFrame,w,h):
    global canvas
    global panelTexto#panel de texto donde se imprime la respuesta
    
    canvas = tk.Canvas(topFrame, width=585, height=h-50, borderwidth=0, highlightthickness=0, bg="#5D6D7E")
    panelTexto=tk.Text(topFrame, height=300, width=50)
    scroll = Scrollbar(topFrame)
    
    canvas.pack(side=tk.LEFT)
    
    scroll.pack(side=RIGHT,fill=Y)
    panelTexto.pack(side=LEFT)
    scroll.config(command=panelTexto.yview)
    panelTexto.config(yscrollcommand=scroll.set)


    
   


def resetAll():
    global canvas
    global numNodos
    global numAristas
    global aristaEnCreacion
    global aristaAux 
    global vectorDeNodos

    canvas.delete("all")    
    numNodos=1     
    numAristas=1
    vectorDeNodos=[] 
    aristaEnCreacion=False
    aristaAux=None


def evaluateGraph():#metodo final de evaluacion del grafo
    global vectorDeNodos    
    global panelTexto
    
    grafo={}
    
    auxArista={}#auxiliar de las aristas

    for i in range(len(vectorDeNodos)):                
        for j in range(len(vectorDeNodos[i].aristas)):#por cada arista que sale del nodo   
            auxArista[vectorDeNodos[i].aristas[j].nodo2.id]=int(vectorDeNodos[i].aristas[j].peso)# {nodo:peso}            
        grafo[vectorDeNodos[i].id]=auxArista# {nodo:{nodoDestino:pesoCamino,...},...}                
        auxArista={}#reseteo de la variable

    d,p = bellman_ford(grafo,vectorDeNodos[0].id)#llamado al metodo bellman-ford con el nodo 1 siempre siendo la base del calculo
    
    panelTexto.insert(END,'%s \n'%(d))
   
    panelTexto.insert(END,'%s \n'%(p))
   
        



def crearNodo(canvas):
    global vectorDeNodos
    nodo= Nodo(canvas,100,120,30)
    vectorDeNodos.append(nodo)

    
class Nodo:#Clase Nodo
    #x
    #y
    #r radio del circulo
    #canvas canvas donde se dibuja todo
    #circle canvas Circle ciculo visual del nodo
    #canvasNum canvasText numero visual del canvas
    #id int numero del nodo
    #moving boolean si el nodo no esta fijo   
    #aristaAux variable que guarda una recta cuando aun no se ha concetado a otro nodo 
    #arista[] vector que guarda todas las aristas que estan conectadas al nodo una vez se a confirmado su coneccion con otro nodo
    
    def __init__(self, canvas,x,y,r):
        self.aristas=[]
        self.canvas = canvas
        self.x=x
        self.y=y
        self.r=r
        self.moving=True
        self.dibujarNodo()
        self.popupMenu()

    def moveCircle(self,event):#metodo que mueve el circulo             
        if self.moving:
            posX=event.x-self.x
            posY=event.y-self.y
            self.x=event.x
            self.y=event.y
            self.canvas.move(self.circle,posX,posY)
            self.canvas.move(self.canvasNum,posX,posY)  
        
    def dibujarNodo(self):#metodo de dibujar el nodo en el canvas
        global numNodos
        self.id=numNodos        
        self.circle=self.canvas.create_circle(self.x, self.y, self.r, fill="#B91049", outline="#B91049", width=4)#circulo       
        self.canvasNum=self.canvas.create_text(self.x,self.y,fill="#000",font="Arial 14 bold",text='%d'%(numNodos))#numero del circulo
        numNodos+=1#aumenta el numero de nodos creados       

        self.canvas.tag_bind(self.circle, '<B1-Motion>', self.moveCircle) #mover si seleccionas el circulo
        self.canvas.tag_bind(self.canvasNum, '<B1-Motion>', self.moveCircle) #mover si seleccionas el numero

        self.canvas.tag_bind(self.circle, '<Button-3>', self.do_popup) #evento del popupmenu que posseen los menus
        self.canvas.tag_bind(self.canvasNum, '<Button-3>', self.do_popup) #evento del popupmenu que posseen los menus
        

    def popupMenu(self):#pop up de opciones para hacer con el nodo

        self.popupMenu=tk.Menu(self.canvas,tearoff=0)
        self.popupMenu.add_command(label="Fijar Nodo",command=self.popupFijarNodo)
        self.popupMenu.add_command(label="Mover Nodo",command=self.popupMoverNodo)
        self.popupMenu.add_command(label="Inicio Arista",command=self.iniciarCreacionArista)
        self.popupMenu.add_command(label="Fin Arista",command=self.finalizarCreacionArista)
    
    def iniciarCreacionArista(self):
        global aristaEnCreacion
        global aristaAux
        if not self.moving:
            aristaEnCreacion=True
            aristaAux=Arista(self.canvas,self)            
        else:
            tk.messagebox.showinfo("Alerta", "Debes Fijar el Nodo antes \n de Poder Crear Una Arista")

    def finalizarCreacionArista(self):
        global aristaEnCreacion
        global aristaAux
        if aristaEnCreacion and not(self.moving):
            aristaEnCreacion=False
            aristaAux.recibirNodo2(self)#se da el nodo con el cual debe conectar   
            
        else:
            tk.messagebox.showinfo("Alerta", "Debes Fijar el Nodo antes \n de Poder Crear Una Arista")


    def popupMoverNodo(self):#volver el nodo movible despues de fijarlo
        self.moving=True
        if self.aristas:            
            for i in range(len(self.aristas)):#for de las aristas
                aux=self.aristas[i]
                self.aristas[i].selfDestroy()
                self.aristas.remove(aux)
        
    def popupFijarNodo(self):#fijar el nodo
        self.moving=False

    def do_popup(self,event):
        # display the popup menu
        try:
            self.popupMenu.tk_popup(event.x_root+55, event.y_root+10, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popupMenu.grab_release()

class Arista:#Clase Arista
    #canvas
    #nodo1
    #nodo2
    #id arista
    #x1
    #y1
    #x2
    #y2
    #textpeso drawn object
    #peso int
    #auxBorder drawn object auxliar para el borde del peso de la arista en el canvas
    def __init__(self, canvas,nodo1):
        self.peso=0
        self.canvas=canvas
        self.nodo1=nodo1        
        self.x1=nodo1.x
        self.y1=nodo1.y
       
    def recibirNodo2(self,nodo2):
        global numAristas
        self.idArista=numAristas
        numAristas+=1
        self.x2=nodo2.x
        self.y2=nodo2.y
        self.nodo2=nodo2
        self.nodo1.aristas.append(self)#se añade la arista al nodo de salida
        #self.nodo2.aristas.append(self)#se añade la arista al nodo de llegada
        
        self.dibujarArista()

    def dibujarArista(self):
        InputDialog(self.canvas,"Arista","Inserte el Peso de la Arista",self)    

        if not (self.nodo1 is self.nodo2):            
            pointX1=(self.x1+self.x2)/2#punto medio de la recta
            pointY1=(self.y1+self.y2)/2#punto medio della recta
            pointX=pointX1
            pointY=pointY1

            for x in range(0, 3):#para que la recta se acerca al circulo pero no lo toque se hace un promedio
                pointX=(pointX+self.x2)/2
                pointY=(pointY+self.y2)/2

                pointX1=(pointX1+self.x1)/2
                pointY1=(pointY1+self.y1)/2

            self.aristaDibujo=self.canvas.create_line(pointX1,pointY1,pointX, pointY, fill="#7B241C", width=5,arrow="last",smooth=True)#flecha de la arista
        else:
            self.aristaDibujo= self.canvas.create_circle_arc(self.x1+10,self.y1-10,50,fill="",outline="#7B241C",width=4)                  

    def dibujarPeso(self):
        if not (self.nodo1 is self.nodo2):  
            self.textPeso=self.canvas.create_text((self.x1+self.x2)/2,(self.y1+self.y2)/2,fill="#FFF",font="Arial 11 bold",text=(self.peso))
        else:
            self.textPeso=self.canvas.create_text(self.x1+40,self.y1-50,fill="#FFF",font="Arial 11 bold",text=(self.peso))
        bbox = self.canvas.bbox(self.textPeso)
        self.auxBorder = self.canvas.create_rectangle(bbox, fill="#7B241C",outline="#7B241C")

        self.canvas.tag_raise(self.textPeso,self.auxBorder)

    def selfDestroy(self):
        self.canvas.delete(self.aristaDibujo)
        self.canvas.delete(self.textPeso)
        self.canvas.delete(self.auxBorder)
        self=None

class InputDialog:
    #top
    #arista
    #input
    def __init__(self, parent,title,message,arista):
        self.arista=arista
        top = self.top = Toplevel(parent)
        Label(top, text=message).pack()
        top.title(title)
        top.resizable(0,0)

        self.input = Entry(top)
        self.input.pack(padx=5)
        w=150#ancho de la ventana
        h=80#alto de la ventana
        # get screen width and height
        ws = top.winfo_screenwidth() # width of the screen
        hs = top.winfo_screenheight() # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen 
        # and where it is placed
        top.geometry('%dx%d+%d+%d' % (w, h, x, y))#el valor del string es "700x(600+x+y)" para marcar las dimensiones y la ubicacion de la ventana en el centro de la pantalla

        button = Button(top, text="Aceptar", command=self.accept)
        button2 = Button(top, text="Cancelar", command=self.cancel)
        
        button.pack(side=tk.LEFT,anchor=CENTER)        
        button2.pack(side=tk.LEFT,anchor=CENTER)

    def accept(self):
        self.value=self.input.get()
        if self.value==' ' or self.value=='':
            self.arista.peso='1'
        else:
            self.arista.peso=self.input.get()
        self.arista.dibujarPeso()
        self.top.destroy()                

    def cancel(self):
        self.top.destroy()
        


if __name__ == '__main__':
   
    mainWindow()
