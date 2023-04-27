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

    def __repr__(self) -> str:
        frase = ""
        for i in self.Frase:
            for l in i.Palabra:
                frase += l.letra
            frase += " "
        return repr(frase)