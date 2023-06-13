from tkinter import *
import re
import logica as log
from logica import Premisas, Formula
from copy import deepcopy

implicacion = "\u2192"
negacion = "\u00AC"
disyuncion = "\u2228"
conjuncion = "\u2227"
cuadrado = "\u25A1"
contradiccion = "\u22A5"
altura = 12


class Interfaz(Frame):
    def __init__(self, ventana, premisas, conclusion):
        super().__init__()
        # Inicializar la ventana con un título y colocar un frame donde almacenar los widgets
        self.ventana = ventana
        self.ventana.title("Gabrielle")
        self.ventana.rowconfigure(3, weight=1)
        self.ventana.rowconfigure(4, weight=1)
        self.ventana.rowconfigure(5, weight=1)

        # creacion de la barra de menu
        self.menu = Menu(self.ventana)
        self.ventana.config(menu=self.menu)
#creacion del menu opciones
        self.opciones = Menu(self.menu, tearoff=False,relief="raised")
        self.opciones.add_command(
            label='Reinicio', command=self.reinicio)
        self.menu.add_cascade(
            label="Opciones",
            menu=self.opciones)

        self.frame = Frame(self.ventana)
        self.frame.pack(side=TOP, fill=BOTH, expand=True)
        for i in range(6):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(25):
            self.frame.grid_columnconfigure(i, weight=1)

        # VARIABLES AUXLIARES
        self.tprevia = ""
        self.historial1 = premisas
        self.historial2 = Premisas(conclusion)
        self.objetivo = [conclusion]
        self.copiaH1 = deepcopy(self.historial1)
        self.copiaH2 = deepcopy(conclusion)
        self.copiaObj = [conclusion]
        self.asmpt = 0
        self.textopantalla = [i for i in self.historial1]
        self.textopantalla2 = [i for i in self.historial2]
        self.asunciones = Premisas()
        self.checkbox = {}
        self.variableas = {}
        self.checkbox2 = {}
        self.variables2 = {}


    #Contruccion de pantallas
        # Agregar la pantalla donde se irán mostrando los cálculos hacia delante
        self.pantalla = Text(self.frame, width=50, height=altura, background="lightgoldenrod4",
                                     foreground="black", font=("Helvetica", 15),cursor="arrow")
        # Ubicar la pantalla en la ventana
        self.pantalla.grid(row=0, column=0, columnspan=15, padx=(5, 5), pady=0, sticky='WSNE')
        # Agregar una pantalla lateral donde ver las variables y poder seleccionarlas
        self.vars = Text(self.frame, state="disabled", width=3, height=altura, background="lightgoldenrod2",
                         foreground="black", font=("Helvetica", 15), cursor="arrow")

        # Ubicar la pantalla en la ventana
        self.vars.grid(row=0, column=15, columnspan=9, padx=(5, 5), pady=0, sticky='WSNE')

        # Agregar la pantalla donde se irán mostrando los cálculos hacia atras
        self.pantalla2 = Text(self.frame, state="disabled", width=50, height=altura, background="lightgoldenrod4",
                              foreground="black", font=("Helvetica", 15), cursor="arrow")
        # Ubicar la pantalla en la ventana
        self.pantalla2.grid(row=1, column=0, columnspan=15, padx=(5, 5), pady=0, sticky='WSNE')



        # Agregar una pantalla lateral donde ver el estado de la demostración

        self.estado = Text(self.frame, state="disabled", width=3, height=altura, background="lightgoldenrod3",
                           foreground="black", font=("Helvetica", 15), cursor="arrow")
        # Ubicar la pantalla en la ventana
        self.estado.grid(row=1, column=15, columnspan=9, padx=(5, 5), pady=0, sticky='WNSE')

        # Agregar una caja de texto para que sea la previa de la calculadora, state es disabled para que el texto se
        # introduzca por raton

        self.previa = Text(self.frame, state="disabled", width=10, height=2.5, background="lightgoldenrod1",
                           foreground="black", font=("Helvetica", 15), cursor="arrow")
        # Ubicar la previa en la ventana
        self.previa.grid(row=2, column=0, columnspan=24, padx=5, pady=5, sticky='WSNE')







        # Crear los botones de la calculadora
        #Fila 1
        boton0 = self.crearBoton("P1"+conjuncion+"P2" + "i")
        boton1 = self.crearBoton("P2"+conjuncion+"P1" + "i")
        boton2 = self.crearBoton(conjuncion + "e1")
        boton3 = self.crearBoton(conjuncion+ "e2")
        boton4 = self.crearBoton(implicacion+ "e")
        boton5 = self.crearBoton("(", escribir=True)
        boton6 = self.crearBoton(")", escribir=True)
        boton7 = self.crearBoton(u"\u232B") # retroceso
        #Fila 2
        boton8 = self.crearBoton(disyuncion+"i1")
        boton9 =  self.crearBoton(disyuncion+"i2")
        boton10 = self.crearBoton(disyuncion+"e")
        boton11 = self.crearBoton(negacion+negacion + "i")
        boton12 = self.crearBoton(negacion+negacion + "e")
        boton13 =   self.crearBoton(disyuncion, escribir=True)
        boton14 = self.crearBoton(conjuncion, escribir=True)
        boton15 =  self.crearBoton(cuadrado+" Abrir")
        #Fila 3
        boton16 =  self.crearBoton("Modus Tollens")
        boton17 = self.crearBoton("Tercio Excluso")
        boton18 = self.crearBoton("Red. Abs.")
        boton19 =  self.crearBoton(negacion + "i")
        boton20 = self.crearBoton(negacion + "e")
        boton21 =  self.crearBoton(implicacion, escribir=True)
        boton22 =  self.crearBoton(negacion, escribir=True)
        boton23 =  self.crearBoton(cuadrado+" Cerrar")
        boton24 = self.crearBoton("\u22A5"+"e")
        # Ubicar los botones numéricos con el gestor grid
        botones = [boton0, boton1, boton2, boton3, boton4, boton5, boton6,
                   boton7, boton8, boton9, boton10, boton11, boton12, boton13,
                   boton14, boton15, boton16, boton17, boton18, boton19, boton20, boton21,boton22,boton23,boton24]
        contador = 0
        while contador < 8:

                botones[contador].grid(row=3, column=contador * 3, columnspan=3, sticky="wnse")
                contador += 1
        for columna in range(8):
            botones[contador].grid(row=4, column=columna * 3, columnspan=3, sticky="wnse")
            contador += 1

        for columna in range(8):
                botones[contador].grid(row=5, column=columna * 3, columnspan=3, sticky="wnse")
                contador += 1
        boton24.grid(row=6,column=0,columnspan=24,sticky="nswe")

        # Mostramos las variables a utilizar en la pantalla 2
        for i in set(premisas.variables()+conclusion.variables()+Formula(contradiccion).variables()):
            self.crearBotonVariable(i)


        # Mostramos las premisas iniciales y sus botones de eleccion
        self.actualizapantalla(self.textopantalla)

        # Mostramos el final de la demostracion
        self.actualizapantalla(self.textopantalla2, True)
        # Mostramos el objetivo de la demostracion
        self.mostrarEnestado(conclusion)


    def click(self, texto, escribir):
        if escribir:
            self.tprevia += str(texto)
            self.limpiarprevia()
            self.mostrarEnprevia(self.tprevia)

        elif texto == u"\u232B":
            self.tprevia = self.tprevia[:-1]
            self.limpiarprevia()
            self.mostrarEnprevia(self.tprevia)

        elif texto == cuadrado +" Abrir":
            self.asunciones.une(log.traductor((self.sus(self.tprevia))))
            self.textopantalla +=["#"+"------"+"-"*2*self.asmpt+"# "+str(self.asmpt)]
            self.historial1.une(log.traductor((self.sus(self.tprevia))))
            self.textopantalla += [(log.traductor((self.sus(self.tprevia))))]
            self.tprevia= ""
            self.asmpt += 1
            self.limpiarprevia()
            self.limpiarPantalla()
            self.actualizapantalla(self.textopantalla)

        elif texto == cuadrado +" Cerrar":
            if self.asmpt != 0:
                nueva = Formula(">", self.asunciones[-1], self.historial1[-1])
                self.historial1.intr_impl(self.asunciones[-1], self.historial1[-1])
                estado = True
                i = 1
                while estado:
                    if type(self.textopantalla[-i]) == str and (self.textopantalla[-i])[-1] == str(self.asmpt-1):
                        estado = False
                    elif type(self.textopantalla[-i]) == str:
                        print((self.textopantalla[-i])[-1])
                        print(self.asmpt-1)
                        i += 1
                    else:
                        del self.historial1[-2]
                        self.textopantalla[-i] = str(self.textopantalla[-i])
                        i += 1
                self.asmpt += -1
                self.textopantalla += ["#"+"------"+"-"*2*self.asmpt+"# "+str(self.asmpt)]
                self.textopantalla += [nueva]
                del(self.asunciones[-1])
                self.limpiarprevia()
                self.tprevia = ""
                self.limpiarPantalla()
                self.actualizapantalla(self.textopantalla)




        elif texto == conjuncion+"e1":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 1:
                    self.historial1.elim_conj1(seleccion[0])
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    self.mostrarEnprevia("Lo siento, regla no válida")
            else:
                if not self.tprevia == "" and len(self.selector(True)) == 1:
                    f = log.traductor(self.sus(self.tprevia))
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.elim_conj1_inv(self.selector(True)[0], f)
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.actualizapantalla(self.textopantalla2, True)
                else:
                    self.mostrarEnprevia("Error con las premisas")




        elif texto == conjuncion + "e2":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 1:
                    self.historial1.elim_conj2(seleccion[0])
                    self.textopantalla +=  [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    self.mostrarEnprevia("Lo siento, regla no válida")
            else:
                if not self.tprevia == "" and len(self.selector(True)) == 1:
                    f = log.traductor(self.sus(self.tprevia))
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.elim_conj2_inv(self.selector(True)[0], f)
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo +=[self.historial2[-1]]
                        self.textopantalla2.insert(0,self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.actualizapantalla(self.textopantalla2, True)


        elif texto == "P1"+conjuncion+"P2" + "i":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 2:
                    nueva = self.historial1.intr_conj(seleccion[0],seleccion[1])
                    self.historial1.une(nueva[0])
                    self.textopantalla +=[nueva[0]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)

            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.intr_conj_inv(self.selector(True)[0])
                    try:
                     self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1], self.historial2[-2]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.textopantalla2.insert(0, self.historial2[-2])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.actualizapantalla(self.textopantalla2, True)


        elif texto == "P2"+conjuncion+"P1" + "i":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 2:
                    nueva = self.historial1.intr_conj(seleccion[0],seleccion[1])
                    self.historial1.une(nueva[1])
                    self.textopantalla +=[nueva[1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.intr_conj_inv(self.selector(True)[0])
                    try :

                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1], self.historial2[-2]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.textopantalla2.insert(0, self.historial2[-2])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.actualizapantalla(self.textopantalla2, True)


        elif texto == disyuncion+"i1":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 1:
                    f = log.traductor(self.sus(self.tprevia))
                    self.historial1.intr_disy1(seleccion[0],f)
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.limpiarprevia()
                    self.actualizapantalla(self.textopantalla)
                else:
                    self.mostrarEnprevia("Lo siento, regla no válida")
            else:
                if len(self.selector(True)) == 1:

                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.intr_disy1_inv(self.selector(True)[0])
                    try:
                     self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.actualizapantalla(self.textopantalla2, True)


        elif texto == disyuncion+"i2":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 1:
                    f = log.traductor(self.sus(self.tprevia))
                    self.historial1.intr_disy2(seleccion[0],f)
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.limpiarprevia()
                    self.actualizapantalla(self.textopantalla)
                else:
                    self.mostrarEnprevia("Lo siento, regla no válida")
            else:
                if len(self.selector(True)) == 1:

                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.intr_disy2_inv(self.selector(True)[0])
                    try:
                     self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.actualizapantalla(self.textopantalla2, True)


        elif texto == disyuncion+"e":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 3:
                    self.historial1.elim_disy(seleccion[0], seleccion[1], seleccion[2])
                    self.textopantalla +=[self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else: raise Exception("Numero de premisas equivocado")

            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    f = log.traductor(self.sus(self.tprevia))
                    self.historial2.elim_disy_inv(self.selector(True)[0],f)
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1], self.historial2[-2],self.historial2[-3]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.textopantalla2.insert(0, self.historial2[-2])
                        self.textopantalla2.insert(0, self.historial2[-3])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)

                else:
                    raise Exception("Numero de premisas equivocado")
        elif texto == implicacion+"e":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 2:
                    self.historial1.elim_impl(seleccion[0],seleccion[1])
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    raise Exception("Numero de premisas equivocado")
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    f = log.traductor(self.sus(self.tprevia))
                    self.historial2.elim_impl_inv(self.selector(True)[0], f)
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1], self.historial2[-2]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.textopantalla2.insert(0, self.historial2[-2])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)

                else:
                    raise Exception("Numero de premisas equivocado")


        elif texto == negacion+negacion+"i":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 1:
                    self.historial1.intr_2neg(seleccion[0])
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    raise Exception("Numero de premisas equivocado")
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.elim_2neg(self.selector(True)[0])
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)

                else:
                    raise Exception("Numero de premisas equivocado")
        elif texto == negacion+negacion+"e":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 1:
                    self.historial1.elim_2neg(seleccion[0])
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    raise Exception("Numero de premisas equivocado")
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.intr_2neg(self.selector(True)[0])
                    try:
                     self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)

                else:
                    raise Exception("Numero de premisas equivocado")
        elif texto == negacion+"i":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 1:
                    self.historial1.intr_neg(seleccion[0])
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    raise Exception("Numero de premisas equivocado")
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.intr_neg_inv(self.selector(True)[0])
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)

                else:
                    raise Exception("Numero de premisas equivocado")

        elif texto == negacion+"e":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 2:
                    self.historial1.elim_neg(seleccion[0], seleccion[1])
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    raise Exception("Numero de premisas equivocado")
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    f = log.traductor(self.sus(self.tprevia))
                    self.historial2.elim_neg_inv(self.selector(True)[0], f)
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1], self.historial2[-2]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.textopantalla2.insert(0, self.historial2[-2])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)

                else:
                    raise Exception("Numero de premisas equivocado")

        elif texto == "Modus Tollens":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 2:
                    self.historial1.modus_tollens(seleccion[0], seleccion[1])
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    raise Exception("Numero de premisas equivocado")
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    f = log.traductor(self.sus(self.tprevia))
                    self.historial2.modus_tollens_inv(self.selector(True)[0], f)
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1], self.historial2[-2]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.textopantalla2.insert(0, self.historial2[-2])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)

                else:
                    raise Exception("Numero de premisas equivocado")

        elif texto == "Tercio Excluso":
            if self.tprevia != "":
                f = log.traductor(self.sus(self.tprevia))
                self.historial1.terc_excl(f)
                self.textopantalla += [self.historial1[-1]]
                self.textopantalla += [self.historial1[-2]]
                self.limpiarPantalla()
                self.actualizapantalla(self.textopantalla)
                self.limpiarprevia()
                self.tprevia = ""
            else:
                self.limpiarprevia()
                self.mostrarEnprevia("Fórmula necesaria")
                raise Exception("Previa vacia")

        elif texto == "Red. Abs.":
            if self.selector_lado():
                seleccion = self.selector()
                if len(seleccion) == 1:
                    self.historial1.reduct_abs(seleccion[0])
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    raise Exception("Numero de premisas equivocado")
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.reduct_abs_inv(self.selector(True)[0])
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)

                else:
                    raise Exception("Numero de premisas equivocado")
        elif texto == "\u22A5"+"e":
            if self.selector_lado():
                seleccion = self.selector()
                f = log.traductor(self.sus(self.tprevia))
                if len(seleccion) == 1:
                    self.historial1.elim_contr(seleccion[0],f)
                    self.textopantalla += [self.historial1[-1]]
                    self.limpiarPantalla()
                    self.actualizapantalla(self.textopantalla)
                else:
                    raise Exception("Numero de premisas equivocado")
            else:
                if len(self.selector(True)) == 1:
                    c = self.historial2[self.selector(True)[0]]
                    self.historial2.elim_contr_inv()
                    try:
                        self.objetivo.remove(c)
                    finally:
                        self.objetivo += [self.historial2[-1]]
                        self.textopantalla2.insert(0, self.historial2[-1])
                        self.limpiarPantalla2()
                        self.limpiarEstado()
                        self.limpiarprevia()
                        self.tprevia = ""
                        self.actualizapantalla(self.textopantalla2, True)








            # comprobamos si ha terminado

        if self.asmpt == 0:
            self.objetivo = [i for i in self.objetivo if i not in self.historial1]
            if len(self.objetivo) == 0:
                self.limpiarprevia()
                self.mostrarEnprevia("Hemos terminado")
                self.limpiarEstado()
                self.mostrarEnestado("Hemos terminado")
            else:
                self.limpiarEstado()
                for i in self.objetivo:
                    self.mostrarEnestado(i)
                    self.mostrarEnestado("\n")


    def crearBotonVariable(self, valor, escribir=True, ancho=5, alto=1):
        return Button(self.vars, text=valor, width=ancho, height=alto, font=("Helvetica", 15),
                      command=lambda: self.click(valor, escribir)).grid()

    def crearBoton(self, valor, escribir=False, ancho=15, alto=1):
        return Button(self.frame, text=valor, width=ancho, height=alto, font=("Helvetica", 15),
                      command=lambda: self.click(valor, escribir))





    def limpiarprevia(self):
        self.previa.configure(state="normal")
        self.previa.delete("1.0", END)
        self.previa.configure(state="disabled")
        return

    def limpiarPantalla(self):
        self.pantalla.configure(state="normal")
        self.pantalla.delete("1.0", END)
        self.pantalla.configure(state="disabled")
        for i in self.checkbox.items():
            i[1].destroy()
        return


    def limpiarPantalla2(self):
        self.pantalla2.configure(state="normal")
        self.pantalla2.delete("1.0", END)
        self.pantalla2.configure(state="disabled")
        for i in self.checkbox2.items():
            i[1].destroy()
        return

    def limpiarEstado(self):
        self.estado.configure(state="normal")
        self.estado.delete("1.0", END)
        self.estado.configure(state="disabled")

    # Muestra en la previa de la calculadora el contenido de las operaciones y los resultados

    def mostrarEnprevia(self, valor):
        self.previa.configure(state="normal")
        self.previa.insert(END, valor)
        self.previa.configure(state="disabled")
        return

    def mostrarEnpantalla(self, valor,boton = None):
        self.pantalla.configure(state="normal")
        self.pantalla.insert(END, valor)
        self.pantalla.window_create(END,window = boton,align = "top")
        self.pantalla.configure(state="disabled")
        return

    def mostrarEnpantalla2(self, valor,boton = None):
        self.pantalla2.configure(state="normal")
        self.pantalla2.insert(END, valor)
        self.pantalla2.window_create(END, window=boton, align="top")
        self.pantalla2.configure(state="disabled")
        return

    def mostrarvariables(self, valor):
        self.pantalla2.configure(state="normal")
        self.pantalla2.insert(END, valor)
        self.pantalla2.configure(state="disabled")
        return

    def mostrarEnestado(self, valor):
        self.estado.configure(state="normal")
        self.estado.insert(END, valor)
        self.estado.configure(state="disabled")
        return

    @staticmethod
    def sus(texto):
        s = re.sub(negacion,"¬",texto)
        s = re.sub(conjuncion,"&",s)
        s = re.sub(disyuncion,"|",s)
        s = re.sub(implicacion,">",s)
        return s

    #Nos refresca las premisas que tenemos actualmente

    def selector(self, conclusion = False):
        if not conclusion:
            seleccion = []
            j = 0
            for premisa in self.variables.values():
                if premisa.get() != 0:
                    seleccion.append(j)
                j += 1
            return seleccion
        else:
            seleccion = []
            j = 0
            for premisa in self.variables2.values():
                if premisa.get() != 0:
                    seleccion.append(j)
                j += 1
            return seleccion

    def selector_lado(self):
        if all(map(lambda x: x.get()==0, self.variables.values())) and \
                all(map(lambda x: x.get() == 0, self.variables2.values())):
            self.limpiarprevia()
            self.tprevia =""
            self.mostrarEnprevia("Escoge alguna premisa")
        elif all(map(lambda x: x.get()==0,self.variables.values())) and \
                any(map(lambda x: x.get()!=0, self.variables2.values())):
            return False
        elif any(map(lambda x: x.get() !=0, self.variables.values())) and\
                all(map(lambda x: x.get() == 0, self.variables2.values())):
            return True
        else:
            self.limpiarprevia()
            self.tprevia = ""
            self.mostrarEnprevia("Solo puedes escoger premisas de un lado")

    def actualizapantalla(self, lineas, inversa=False):
        if not inversa:
            self.variables = {}
            self.checkbox = {}
            for i in lineas:
                if not isinstance(i,str):
                    self.variables[i] = IntVar()
                    self.checkbox[i] = Checkbutton(self.pantalla, text="", bg="lightgoldenrod4",
                                                         variable = self.variables[i])
                self.mostrarEnpantalla(i,self.checkbox[i] if not isinstance(i,str) else None)
                self.mostrarEnpantalla("\n")
        else:
            self.variables2 = {}
            self.checkbox2 = {}
            for i in lineas:
                if not isinstance(i, str):
                    self.variables2[i] = IntVar()
                    self.checkbox2[i] = Checkbutton(self.pantalla2, text="", bg="lightgoldenrod4",
                                                    variable=self.variables2[i])
                self.mostrarEnpantalla2(i,self.checkbox2[i] if not isinstance(i,str) else  None)
                self.mostrarEnpantalla2("\n")




        print(f"Premisas {self.historial1}")
        print(f"Asunciones {self.asunciones}")
        print(f"Texto {self.textopantalla}")
        print(f"Conclusiones {self.objetivo}")
        print(f"Botones {self.checkbox}")
        print("\n")


    def terminarpasopantalla(self,calculo):
        self.textopantalla += [calculo]
        self.limpiarprevia()
        self.limpiarPantalla()
        self.actualizapantalla(self.textopantalla)
        self.tprevia = ""

    def reinicio(self):
        self.tprevia = ""  # texto que está en la previa
        self.historial1 = self.copiaH1 # Lleva un registro de las premisas hasta ahora, hacia delante, es un objeto Premisa
        self.historial2 = Premisas(self.copiaH2)  # Lleva un registro de las premisas hacia atrás
        self.copiaH1= deepcopy(self.copiaH1)
        self.copiaH2 = deepcopy(self.copiaH2)
        self.objetivo = self.copiaObj  # La formulas que aun faltan por probar
        self.asmpt = 0  # contador de asunciones
        self.textopantalla = [i for i in self.historial1]  # una lista con los strings y Formulas a usar en pantalla
        self.textopantalla2 = [i for i in self.historial2]
        self.asunciones = Premisas()  # Lugar donde iremos colocando las premisas asumidas
        self.checkbox = {}
        self.variables = {}
        self.checkbox2 = {}
        self.variables2 = {}
        self.limpiarprevia()
        self.limpiarPantalla()
        self.limpiarEstado()
        self.limpiarPantalla2()
        self.actualizapantalla(self.historial1)
        self.actualizapantalla(self.historial2,True)
        self.mostrarEnestado(self.objetivo)




