import pygame
class Letra:
    def __init__(self, letra, x=None, y=None):
        self.pos_x = x
        self.pos_y = y
        self.letra = letra.upper()
        self.color_fondo = "white"
        if len(self.letra) != 1 and self.letra != '   ':
            self.rect = (self.pos_x, self.pos_y, 100, 40)
        else:
            self.rect = (self.pos_x, self.pos_y, 45, 55)

    def dibujar(self, pantalla, update=True):
        pygame.draw.rect(pantalla, self.color_fondo, self.rect)
        if self.letra == '   ':
            self.text_surface = pygame.font.Font(size=60).render(self.letra, True, "black", "white")
            self.text_rect = self.text_surface.get_rect(center=(self.pos_x+21.5, self.pos_y+27.5))
        elif len(self.letra) != 1:
            self.text_surface = pygame.font.Font(size=28).render(self.letra, True, "black")
            self.text_rect = self.text_surface.get_rect(center=(self.pos_x+50, self.pos_y+20))
        else:
            self.text_surface = pygame.font.Font(size=28).render(self.letra, True, "black")
            self.text_rect = self.text_surface.get_rect(center=(self.pos_x+21.5, self.pos_y+27))
        pantalla.blit(self.text_surface, self.text_rect)
        if update == True:
            pygame.display.update()

    def eliminar(self, pantalla):
        pygame.draw.rect(pantalla, "white", self.rect)
        pygame.draw.rect(pantalla, "#d3d6da", self.rect, 3)
        pygame.display.update()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Letra):
            return True if self.letra == __o.letra else False
        else: 
            return True if self.letra == __o else False

    def Get_Letra(self):
        return self.Letra