import pygame   
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color) -> None:
        self.image = image
        self.x_posicion = pos[0]
        self.y_posicion = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_posicion, self.y_posicion))
        self.text_rect = self.text.get_rect(center=(self.x_posicion, self.y_posicion))
    
    def Update(self, pantalla):
        if self.image is not None:
            pantalla.blit(self.image, self.rect)
        pantalla.blit(self.text, self.text_rect)

    def CheckForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # def ChangeColor(self, position):
    #     pass