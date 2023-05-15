from Juego import Juego

class Administrador:
    def __init__(self) -> None:
        self.Iniciar_juego()

    def Iniciar_juego(self):
        Juego(self)

    def Asignar_Frases(self, Juego, frase = ""):
        Juego.Guardar_frase(frase)

    def Asignar_tiempo_limite(self, Juego, tiempo=""):
        Juego.Guardar_tiempo_limite(tiempo)
