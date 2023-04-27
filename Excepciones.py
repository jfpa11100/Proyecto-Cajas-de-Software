class FraseConTilde(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.mensaje = msg

class FraseVacia(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.mensaje = msg

class FraseNoPermitida(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.mensaje = msg

class PalabraNoExistente(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.mensaje = msg
        
class RequisitoFaltante(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.mensaje = msg

class NumeroNoPermitido(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.mensaje = msg

class NombreNoPermitido(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.mensaje = msg

class PalabrasAdivinadas(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.mensaje = msg


        