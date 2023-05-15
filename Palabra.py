from Letra import Letra
class Palabra:
    def __init__(self, palabra) -> None:
        self.Palabra = []
        self.Adivinada = False
        for i in palabra:
            self.Palabra.append(Letra(i))

    def Get_Palabra(self):
        return self.Palabra

    def Get_palabraStr(self):
        palabra = ""
        for i in self.Palabra:
            palabra += i.letra
        return palabra

    def Get_Adivinada(self):
        return self.Adivinada

    def __len__(self):
        return len(self.Palabra)

    def __repr__(self) -> str:
        palabra = ""
        for i in self.Palabra:
            palabra += i.letra
        return repr(palabra)

    def __eq__(self, __o) -> bool:
        if __o == None:
            return True
        else:
            pal1 , pal2 = "", ""
            for i in range(len(self.Palabra)):
                pal1 += self.Palabra[i].letra
                pal2 += __o[i].letra
            return True if pal1 == pal2 else False 

    def __ne__(self, __o: object) -> bool:
        if isinstance(__o, Palabra):
            pal1 , pal2 = "", ""
            for i in range(len(self.Palabra)):
                pal1 += self.Palabra[i].letra
                pal2 += __o[i].letra

            return False if pal1 == pal2 else True 
        else:
            pal1= ""
            for i in range(len(self.Palabra)):
                pal1 += self.Palabra[i].letra
            return False if pal1 == __o else True 