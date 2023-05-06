from tkinter import *
from demostracion import Interfaz
from logica import Premisas, traductor
import re
implicacion = "\u2192"
negacion = "\u00AC"
disyuncion = "\u2228"
conjuncion = "\u2227"
contradiccion = "\u22A5"
color = 'royal blue'


class Gestor:
    def __init__(self, ventana):
        # Inicializar la ventana con un título
        self.ventana = ventana
        self.Interfaz = Interfaz
        self.ventana.title("Gabrielle")
        self.frame = Frame(self.ventana,bg= color)
        self.frame.grid()


        self.label = Label(self.frame,text="Premisas",height=2,font=("Helvetica", 15),bg= color)
        self.label.grid(sticky="n", row = 0, column= 0, columnspan=5,padx =(5,5))
        self.label = Label(self.frame, text="Conclusión",height=2,font=("Helvetica", 15), bg = color)
        self.label.grid(sticky="n", row=3, column=0, columnspan=5,padx =(5,5))
        self.prem = Text(self.frame, font=("Helvetica", 15), cursor="arrow", height=1)
        self.prem.grid(row=1, column=0, columnspan=5,padx =(5,5))

        self.conc = Text(self.frame,  font=("Helvetica", 15), cursor="arrow", height=1)
        self.conc.grid(row=4, column = 0, columnspan=5,padx =(5,5))

        b = Button(self.frame, text="Demostrar", command=self.mostrador, height=9)
        b.grid(row = 0, rowspan=10, column = 5, sticky="snew",padx =(0,5),pady=(5,5))

        b1 = self.creaboton(texto=disyuncion)
        b2 = self.creaboton(texto=conjuncion)
        b3 = self.creaboton(texto=negacion)
        b4 = self.creaboton(texto=implicacion)
        b5 = self.creaboton(texto=contradiccion)

        b6 = self.creaboton(texto=disyuncion,prem=False)
        b7 = self.creaboton(texto=conjuncion,prem=False)
        b8 = self.creaboton(texto=negacion,prem=False)
        b9 = self.creaboton(texto=implicacion,prem=False)
        b10 = self.creaboton(texto=contradiccion,prem=False)
        botonera = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10]
        botonera[0].grid(row=2, column=0, sticky="nsew",padx=(5,0))
        for i in range(1,5):
            botonera[i].grid(row=2,column=i,sticky="nsew")
        botonera[5].grid(row=5, column=0, sticky="nsew",padx=(5,0),pady=(0,5))
        for i in range(6,10):
            botonera[i].grid(row=5,column=i-5,sticky="nsew",pady=(0,5))


    def creaboton(self,texto,prem= True):
        if prem:
            return Button(self.frame, text=texto,  height=1, font=("Helvetica", 15),
                          command=lambda: self.escribeP(texto))
        else:
            return Button(self.frame, text=texto, height=1, font=("Helvetica", 15),
                          command=lambda: self.escribeC(texto))

    def escribeP(self,texto):
        self.prem.insert(END,texto)

    def escribeC(self,texto):
        self.conc.insert(END,texto)

    def escritoP(self):
        premisas = Premisas()
        if len(self.prem.get('1.0',"end-1c")) >= 1:
            for i in self.prem.get('1.0',"end-1c").split(",") :
                premisas.une(traductor(self.sus(i)))
            return premisas

        else:

            return premisas

    def escritoC(self):
        return ( (traductor(self.sus(self.conc.get('1.0',"end-1c")))))

    def mostrador(self):
        if self.conc.get("1.0","end-1c") != "" or "," in self.conc.get("1.0","end-1c") :
            self.frame.grid_forget()
            self.Interfaz(self.ventana,self.escritoP(), self.escritoC()).tkraise(self.frame)
        else:
            self.escribeC("Error en el número de conclusiones")

    def sus(self,texto): #Ya esta definida en demostracion, pero no se importarla
        s = re.sub(negacion,"¬",texto)
        s = re.sub(conjuncion,"&",s)
        s = re.sub(disyuncion,"|",s)
        s = re.sub(implicacion,">",s)
        return s

ventana_principal = Tk()
calculadora = Gestor(ventana_principal)
ventana_principal.mainloop()