class Jugador:
    def __init__(self, nombre, numero) -> None:
        self.Nombre = nombre
        self.Numero = numero
        self.Puntuacion = 0
        self.Participo = False

    def Registrar(self, Juego):
        Juego.Guardar_Jugador(self)

    def AdivinarPalabra(self, intento, Juego):
        Juego.Verificar_intento(intento, self)
    
    def AdivinarFrase(self, intento, Juego):
        Juego.Verificar_frase(intento)

    def __repr__(self) -> str:
        return repr(f"Jugador {self.Nombre}, num: {self.Numero}")