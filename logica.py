

"""
Este módulo será utilizado para crear las clases de las fórmulas proposicionales

Haremos esta definición de forma recursiva.

"""

"Funciones básicas"
def esVariable(var):


    """Comprueba si el string var es una variable,
     consideraremos como variables los caracteres a..z seguidos, o no, por
    un número"""
    return var[0] >= 'a' and var[0] <= 'z' and (len(var) == 1 or var[1:].isdecimal())

def esCte(var):
    """
    Comprueba  si es la formula contradiccion \u22A5 = ⊥"
    """
    return var == '\u22A5'

def esMonaria(var):
    """ Comprueba si la variable es el conector ¬"""
    return var == '¬'

def esBinaria(var):
    """ Comprueba si la variable es un conector binario (AND) &,(IF) > o (OR) |"""
    return var == '&' or var == '|' or var == '>'






class Formula:
    def __init__(self, raiz, izq=None, der=None):
        """
        :param raiz: conectiva monaria, binaria o variable (unitaria)
        :param izq: variable unitaria (si conector monario) o primera variable
        :param der: segunda variable
        """
        if esVariable(raiz) or esCte(raiz):
            self.raiz = raiz
        elif esMonaria(raiz) and isinstance(izq,Formula):
            self.raiz = raiz
            self.izq = izq
        elif esBinaria(raiz) and isinstance(izq,Formula) and isinstance(der,Formula):
            self.raiz = raiz
            self.izq = izq
            self.der = der
        else:
            raise Exception("Hubo problemas al crear la fórmula")

    def __str__(self):
        if esVariable(self.raiz) or esCte(self.raiz):
            return (self.raiz)
        elif esMonaria(self.raiz):
            return ''.join(map(str, [self.raiz, self.izq]))
        elif esBinaria(self.raiz):
            return ''.join(map(str, ['(', self.izq, self.raiz,
                                     self.der, ')']))

    def __repr__(self):
        if esVariable(self.raiz) or esCte(self.raiz):
            return self.raiz
        elif esMonaria(self.raiz):
            return ''.join(map(str, [self.raiz, self.izq]))
        elif esBinaria(self.raiz):
            return ''.join(map(str, ['(', self.izq, self.raiz,
                                     self.der, ')']))

    def __eq__(self, other):
        if esBinaria(self.raiz) and esBinaria(other.raiz):
            r = self.raiz == other.raiz
            i = self.izq == other.izq
            d = self.der == other.der
            return (r and i and d)
        elif esVariable(self.raiz) and esVariable(other.raiz) :
            return self.raiz == other.raiz
        elif esMonaria(self.raiz) and esMonaria(other.raiz):
            return self.izq == other.izq
        elif esCte(self.raiz) and esCte(other.raiz):
            return self.raiz == other.raiz
        else:
            return False
    def __hash__(self):
        return hash(repr(self))

    def variables(self):
        def recursivo_acum(f, acum):
            if esVariable(f.raiz):
                acum.append(f.raiz)
                return acum
            elif esCte(f.raiz):
                acum.append(f.raiz)
                return acum
            elif esMonaria(f.raiz):

                return recursivo_acum(f.izq, acum)
            else:

                rizq = recursivo_acum(f.izq, acum)
                return recursivo_acum(f.der, rizq)
        return list(set(recursivo_acum(self, [])))




    def es_conj(self):
        return self.raiz == "&"

    def es_disy(self):
        return self.raiz == "|"

    def es_neg(self):
        return self.raiz == "¬"

    def es_impl(self):
        return self.raiz == ">"

    def es_Cte(self):
        return self.raiz == "\u22A5"





class Premisas:
    def __init__(self, *args):
        if all(type(i) == Formula for i in args):
            self.premisas = [i for i in args]
        else:
            raise Exception("Algo salió mal,una de las premisas no era una fórmula")


    def __len__(self):
        return len(self.premisas)

    def __getitem__(self, i):
        return self.premisas[i]

    def __delitem__(self, key):

        del self.premisas[key]

    def __setitem__(self, i, formula):
        if type(formula) == Formula:
            self.premisas[i] = formula
        else:
            print("Lo siento, eso no era una fórmula")
        return self.premisas

    def __str__(self):
        return "{" + ', '.join(map(str, (self.premisas))) + "}"

    def une(self, f):
        """ Dado un conjunto de premisas le introducimos otra Formula """
        self.premisas = self.premisas + [f]
        return self

    def variables(self):
        vars = []
        for i in range(len(self)):
           vars += ((self.premisas[i]).variables())
        return list(set(vars))



    """
    REGLAS DE INFERENCIA
    -------------------
        CONJUNCIÓN 
    """

    def elim_conj1(self,premisa):
        f = self.premisas[premisa]
        if self.premisas[premisa].es_conj():
            return self.une(f.izq)

        else:
            raise Exception("Eso no era una conjunción")
    def elim_conj1_inv(self,conclusion,premisaN):
        f = self.premisas[conclusion]
        return self.une(Formula("&",f,premisaN))




    def elim_conj2(self, premisa):
        f = self.premisas[premisa]
        if self.premisas[premisa].es_conj():
            return self.une(f.der)

        else:
            raise Exception("Eso no era una conjunción")

    def elim_conj2_inv(self,conclusion, premisaN):
        f = self.premisas[conclusion]
        return self.une(Formula("&", premisaN, f))


    def intr_conj(self, p1, p2):
        f1 = self.premisas[p1]
        f2 = self.premisas[p2]
        return (Formula("&",f1,f2),Formula("&",f2,f1))

    def intr_conj_inv(self,conclusion):

        f = self.premisas[conclusion]
        if f.es_conj():
            self.une(f.izq)
            self.une(f.der)
            return self
        else:
            raise Exception("La premisa escogida no era una conjunción")


#   DISYUNCIÓN
    def intr_disy1(self,premisa,premisaN):
        """
    Devuelve la premisa elegida en el lado izquierdo de una disyunción con una premisa escrita en el previo
        """
        f = self.premisas[premisa]
        return self.une(Formula("|",f,premisaN))

    def intr_disy1_inv(self,conclusion):
        f = self.premisas[conclusion]
        if f.es_disy():
            return self.une(f.izq)
        else:
            raise Exception("Eso no era una disyunción")

    def intr_disy2(self, premisa, premisaN):
        """
     Devuelve la premisa elegida en el lado derecho de una disyunción con una premisa escrita en el previo
        """
        f = self.premisas[premisa]
        return self.une(Formula("|",premisaN,f))

    def intr_disy2_inv(self, conclusion):
        f = self.premisas[conclusion]
        return self.une(f.der)

    def elim_disy(self, premisa1, premisa2,premisa3):
        """
        :param premisa1: posicion de la disyuncion a trabajar

        :return: un elemento a partir de eliminar una disyuncion
        """
        f = [i for i in[self.premisas[premisa1],self.premisas[premisa2],self.premisas[premisa3]] if i.es_disy()][0]
        f1 = [i for i in[self.premisas[premisa1],self.premisas[premisa2],self.premisas[premisa3]] if not i.es_disy()][0]
        f2 = [i for i in[self.premisas[premisa1],self.premisas[premisa2],self.premisas[premisa3]] if not i.es_disy()][1]
        v1 = f.izq
        v2 = f.der
        if f.es_disy() and f1.es_impl() and f2.es_impl() :
            if v1 == f1.izq and v2 == f2.izq and f1.der == f2.der:
                    return self.une(f2.der)
            else:
                    raise Exception("Error, premisa equivocada")
        else:
                raise Exception("Error en las premisas")


    def elim_disy_inv(self,conclusion, conclusionN):
        """
        :param conclusion: Conclusion de la que partimos hacia atras
        :param conclusionN: Disyuncion escrita en la previa
        :return:
        """
        if conclusionN.es_disy():
            f1 = conclusionN.izq
            f2 = conclusionN.der
            c = self.premisas[conclusion]
            self.une(conclusionN)
            self.une(Formula(">",f1,c))
            self.une(Formula(">",f2,c))
            return
        else:
            raise Exception("La premisa escrita no era una disyunción")


    # IMPLICACIÓN
    def intr_impl(self,asuncion,conclusion):
        """

        Como nose hacerlo de otra forma cuando cerramos el cuadrado de asuncion usaremos este comando para borrar la
        asuncion de las premisas y la conclusión y añadir Formula := asuncion -> conclusion
        """
        self.une(Formula(">",asuncion,conclusion))



    def elim_impl(self,implicacion,consecuente):
        f1 = self.premisas[implicacion]
        f2 = self.premisas[consecuente]
        if f1.es_impl() and f1.izq == f2:
            return self.une(f1.der)
        elif f2.es_impl() and f2.izq == f1:
            return self.une(f2.der)
        else:
            raise Exception("Error en las premisas")

    def elim_impl_inv(self,consecuencia,consecuenteN):
        self.une(Formula(">",consecuenteN,self.premisas[consecuencia]))
        self.une(consecuenteN)
        return

#   NEGACIÓN


    def elim_neg(self,premisa1, premisa2):
        f1 = self.premisas[premisa1]
        f2 = self.premisas[premisa2]
        if f1 == Formula("¬",f2) or f2 == Formula("¬",f1):
            return self.une(Formula("\u22A5"))
        else:
            raise Exception("Premisas equivocadas")

    def elim_neg_inv(self,conclusion,premisaN): #Esta regla no se si es util hacia atras
        f = self.premisas[conclusion]
        if f == Formula("\u22A5"):
            self.une(Formula("¬" ,premisaN))
            return self.une(premisaN)
        else:
            raise Exception("Error en las premisas")


    def intr_neg(self,premisa):
        f = self.premisas[premisa]
        if f.es_impl() and f.der == Formula("\u22A5"):
            return self.une(Formula("¬",f.izq))
        else:
            raise Exception("Error en las premisas")

    def intr_neg_inv(self,conclusion):
        f = self.premisas[conclusion]
        return self.une(Formula(">",Formula("¬",f),Formula("\u22A5")))

    def elim_contr(self,premisa,premisaN):
        f = self.premisas[premisa]
        if f.es_Cte():
            self.une(premisaN)
        else:
            raise Exception("Eso no era una contradicción")
    def elim_contr_inv(self):
        return self.une(Formula("\u22A5"))


#   Reglas derivadas

    def intr_2neg(self, premisa):
        f = self.premisas[premisa]
        return self.une(Formula("¬",(Formula("¬",f))))

    def elim_2neg(self, premisa):
        f = self.premisas[premisa]
        if f.es_neg() and f.izq.es_neg():
           return self.une(f.izq.izq)
        else:
            raise Exception("No es una doble negación")


    # Modus Tollens
    def modus_tollens(self,p1,p2):
        f1 = self.premisas[p1]
        f2 = self.premisas[p2]
        if (f1.es_impl() and f2.es_neg() and f1.der == f2.izq) or \
                (f2.es_impl() and f1.es_neg() and f2.der == f1.izq):
            resultado = Formula("¬", f1.izq) if f1.es_impl() else Formula("¬", f2.izq)
            return self.une(resultado)
        else:
            raise Exception("No se puede aplicar Modus Tollens")
    def modus_tollens_inv(self,conclusion,premisaN):

        f = self.premisas[conclusion]
        if f.es_neg():
                self.une(Formula(">",Formula("¬",f),premisaN))
                self.une(Formula("¬",premisaN))
                return


        else:
            raise Exception("No puede aplicarse modus Tollens sin una negación")

    # Tercio excluso
    def terc_excl(self,premisaN):
        self.une(Formula("|",premisaN,Formula("¬",premisaN)))
        self.une(Formula("|",  Formula("¬", premisaN),premisaN))
        return
    # Reducción al absurdo
    def reduct_abs(self,premisa):
        f = self.premisas[premisa]
        if f.izq.es_neg and f.der.es_Cte and f.es_impl:
            return self.une(f.izq.izq)
        else:
            raise Exception("Hubo un error con la premisa")

    def reduct_abs_inv(self,conclusion):
        f = self.premisas[conclusion]
        return self.une(Formula(">",Formula("¬",f),"\u22A5"))



def buscaraiz(string):
    """
    Funcion auxiliar para el traductor de escritura humana a Formula, esta funcion buscara el operador que
    actua como raiz del grafo arbol de la Formula

    """
    if string[0] == "¬":
        indice = 2
        Nparentesis = 1
        while Nparentesis != 0:
            if string[indice] == "(":
                Nparentesis += 1
            elif string[indice] == ")":
                Nparentesis -= 1
            indice += 1
    elif string[0] == "(":
        indice = 1
        Nparentesis = 1
        while Nparentesis != 0:
            if string[indice] == "(":
                Nparentesis += 1
            elif string[indice] == ")":
                Nparentesis -= 1
            indice += 1
    else:
        indice = 1
    return indice

def buscarraizfinal(string):
    indice = 0
    estado = True
    while estado:
        if esBinaria(string[indice]):
            estado = False
        else:
            indice += 1
    return indice




def traductor(formula):
    """

    :param formula: String de la fórmula en escritura normal
    :return: traduccion al tipo Formula para poder hacer los calculos

    """
    if len(formula) == 1:
        return Formula(formula)
    elif formula[0] == "¬":
        return Formula("¬", traductor(formula[1:]))

    elif formula[0] == "(" and formula[-1] == ")" and "(" in formula[1:-1]:
        nucleo = buscaraiz(formula[1:-1])
        return Formula(formula[nucleo+1], traductor(formula[1:nucleo+1]), traductor(formula[nucleo+2:-1]))
    elif formula[0] == "(" and formula[-1] == ")" and "(" not in formula[1:-1]:
        nucleo = buscarraizfinal(formula)
        return Formula(formula[nucleo],traductor(formula[1:nucleo]),traductor(formula[nucleo+1:-1]))
    else:
        raise Exception("Posible error de paréntesis")



