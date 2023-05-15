from Palabra import Palabra
class Frase:
    def __init__(self, frase) -> None:
        xfrase = frase.split(" ")
        self.Frase = [Palabra(i) for i in xfrase]
        self.Adivinada = False
        
    def __len__(self):
        return len(self.Frase)

    def Get_Frase(self):
        return self.Frase

    def Get_Adivinada(self):
        return self.Adivinada

    def Set_Adivinada(self, value):
        self.Adivinada = value

    def __eq__(self, __o ) -> bool:
        if isinstance(__o, Frase):
            if len(self) != len(__o):
                return False
            for i in range(len(self.Frase)):
                if len(self.Frase[i]) != len(__o.Frase[i]):
                    return False
                elif self.Frase[i] != __o.Frase[i]:
                    return False
            return True
        else:
            __o = __o.upper()
            __o = __o.split(" ")
            for i in range(len(self.Frase)):
                if len(self.Frase[i]) != len(__o[i]):
                    return False
                elif self.Frase[i] != __o[i]:
                    return False
            return True

    def __repr__(self) -> str:
        frase = ""
        for i in self.Frase:
            for l in i.Palabra:
                frase += l.letra
            frase += " "
        return repr(frase)