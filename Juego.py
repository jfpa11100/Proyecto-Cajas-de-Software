import copy
import time
from Frase import Frase
from Letra import Letra
from Palabra import Palabra
from Interfaz import Interfaz
from Excepciones import *
import random

class Juego:
    def __init__(self, Administrador) -> None:
        self.Administrador = Administrador
        self.Frases:list = []
        self.Jugadores: list = []
        self.Tiempo_limite: int = None
        self.Frase_objetivo: Frase
        self.Palabra_objetivo:Palabra = None
        self.Intentos_palabra: int = 5
        self.Intentos_Frase: int = 2
        self.diccionario: list = []
        self.__Cargar_diccionario()
        Interfaz.Menu_screen(self)

    def __Cargar_diccionario(self):
        with open("spanish.txt") as file:
            lines = file.readlines()
            self.diccionario = [line.rstrip() for line in lines]
            for i in range(len(self.diccionario)):
                if "Ã±" in self.diccionario[i]:
                    self.diccionario[i] = self.diccionario[i].replace("Ã±","ñ")

    def Guardar_frase(self, frase = ""):
        xfrase = frase.split(" ")
        tildes = ["á", "é", "í", "ó", "ú"]

        #Chequeo Frase vacía
        if len(frase) == 0:
            raise FraseVacia("La frase no puede estar vacía")

        #Chequeo tildes
        elif [i for i in frase if i in tildes]:
            raise FraseConTilde("La frase no debe tener tildes")

        #Chequo si existen las palabras
        elif  [i for i in xfrase if i.lower() not in self.diccionario]:
            raise PalabraNoExistente("La frase tiene palabras inexistentes")

        #Chequeo Longitud de frase
        elif len([i for i in xfrase if len(i) > 2]) < 4 or len([i for i in xfrase if len(i) > 2]) > 6:
            raise FraseNoPermitida("La frase no cumple con la longitud requerida")

        else:
            self.Frases.append(Frase(frase))

    def Guardar_Jugador(self, jugador):
        self.Jugadores.append(jugador)
    
    def Guardar_tiempo_limite(self, tiempo):
        self.Tiempo_limite = int(tiempo)

    def Asignar_Frase_Objetivo(self):
        frases = [i for i in self.Frases if i.Adivinada == False]
        if len(frases) > 0:
            self.Frase_objetivo = random.choice(self.Frases)
            self.Frase_objetivo.Adivinada = True
            return True
        else:
            return False

    def Asignar_Palabra_objetivo(self):
        frases = [i for i in self.Frase_objetivo.Frase if i.Adivinada == False]
        if len(frases) > 0:
            self.Palabra_objetivo = random.choice(frases)
        else:
            raise PalabrasAdivinadas("El jugador ha adivinado todas las palabras de la frase!")

    def Longitud_Palabra_objetivo(self):
        return len(self.Palabra_objetivo) 

    def Existente_numero_jugador(self, numero):
        for jugador in self.Jugadores: 
            if numero == jugador.Numero:
                return True
        return False

    def Verificar_intento(self, intento, jugador):
        if self.Palabra_objetivo == intento:
            for i in range (len(intento)):
                Interfaz.Pintar_letra(intento[i], "#6aaa64")
            self.Palabra_objetivo.Adivinada = True
            todas = True
            for i in self.Frase_objetivo.Frase:
                if i.Adivinada is False:
                    todas = False
            if todas != True:
                time.sleep(3)
                Interfaz.Jugar_screen(self, self.Palabra_objetivo.Get_palabraStr(), True, jugador)
            else:
                Interfaz.Jugar_screen(self, self.Palabra_objetivo.Get_palabraStr(), True, jugador)
        else:
            target = copy.deepcopy(self.Palabra_objetivo)
            for l in range(len(self.Palabra_objetivo)):
                if intento[l].letra == target.Get_palabraStr()[l]:
                    Interfaz.Pintar_letra(intento[l], "#6aaa64")
                    target.Palabra[l].letra="0"

            for k in range(len(self.Palabra_objetivo)):                                    
                if intento[k].letra in target.Get_palabraStr():
                    indx = [i.letra for i in target.Palabra if isinstance(i, Letra)].index(intento[k].letra)
                    if intento[k].color_fondo == "white":
                        Interfaz.Pintar_letra(intento[k], "#c9b458")
                        target.Palabra[indx].letra = "1"+str(k)
                else:
                    if intento[k].color_fondo == "white":
                        Interfaz.Pintar_letra(intento[k], "#787c7e")

    def Verificar_frase(self, frase):
        if self.Frase_objetivo == frase:
            return
        else:
            raise

    def Siguiente_turno(self):
        jugadores = [i for i in self.Jugadores if i.Participo == False]
        if self.Asignar_Frase_Objetivo():
            if len(jugadores) > 0:
                jugador = random.choice(jugadores)
                jugador.Participo = True
                Interfaz.Jugar_screen(self, None, False, jugador)
            else:
                for jugador in self.Jugadores:
                    jugador.Participo = False
                jugadores = [i for i in self.Jugadores if i.Participo == False]
                jugador = random.choice(jugadores)
                jugador.Participo = True
                Interfaz.Jugar_screen(self, None, False, jugador)     
        else:
            Interfaz.Resultados_screen(self)


    def Get_Frases(self):
        return self.Frases
        
    def Get_Jugadores(self):
        return self.Jugadores

    def Get_Tiempo_limite(self):
        return self.Tiempo_limite
    
    def Get_Administrador(self):
        return self.Administrador

    def Get_Intentos_palabra(self):
        return self.Intentos_palabra

    def Get_diccionario(self):
        return self.diccionario

    def Get_Palabra_objetivo(self):
        return self.Palabra_objetivo