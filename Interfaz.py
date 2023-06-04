import gc
import time
from Button import Button
from Jugador import Jugador
from Excepciones import *
from Letra import Letra
import pygame
import pygame_gui
import sys

global guesses, guesses_count, current_guess, current_guess_string, current_letter_bg_x, indicators, game_result, palabras_adivinadas
guesses, guesses_count, current_guess, current_guess_string, current_letter_bg_x, indicators, game_result, palabras_adivinadas = None, 0, [], "", 0, [], "", []
class Interfaz:
    Pantalla = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    Ancho_pantalla, Altura_pantalla = pygame.display.get_surface().get_size()
    Manager = None
    Clock = None

    def Menu_screen(Juego):
        pygame.init()
        Interfaz.Manager = pygame_gui.UIManager(Interfaz.Pantalla.get_size())
        Interfaz.Clock = pygame.time.Clock()
        Icono = pygame.image.load("Icono.png")
        pygame.display.set_caption("Cajas de Software")
        pygame.display.set_icon(Icono)
        while True:
            Interfaz.Pantalla.fill("White")
            menu_mouse_pos = pygame.mouse.get_pos()

            Interfaz.Añadir_texto("Menú Principal", 50, (Interfaz.Ancho_pantalla/2,200), pygame.Color("#000240"))

            inicio_btn = Button(image=None, pos=(Interfaz.Ancho_pantalla/2, 450), text_input="INICIAR",
                                font=Interfaz.Get_font(40), base_color=pygame.Color("#000240"), hovering_color="White")

            instrucciones_btn = Button(image=pygame.image.load("Ins.png"), pos=(70, 700), text_input="            ",
                                font=Interfaz.Get_font(40), base_color="#d7fcd4", hovering_color="White")
                            
            logo = Button(image=pygame.image.load("Icono.png"), pos=(25, 20), text_input="   ",
                                font=Interfaz.Get_font(20), base_color="#d7fcd4", hovering_color="White")

            for button in [inicio_btn, instrucciones_btn, logo]:
                button.Update(Interfaz.Pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if inicio_btn.CheckForInput(menu_mouse_pos):
                        Interfaz.__Ingreso_Estructura_Juego(Juego)
                    if instrucciones_btn.CheckForInput(menu_mouse_pos):
                        Interfaz.__Instrucciones_screen(Juego)

            pygame.display.update()

    def __Ingreso_Estructura_Juego(Juego):
        pygame.display.set_caption("Cajas de Software")
        input_frases = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(Interfaz.Ancho_pantalla/3, 200, 500, 60),
                                                            manager=Interfaz.Manager, object_id="#entrada_frases",
                                                            placeholder_text="Admin ingrese una o varias frases")
        input_tiempo = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(Interfaz.Ancho_pantalla/3, 400, 500, 60),
                                                            manager=Interfaz.Manager, object_id="#entrada_tiempo",
                                                            placeholder_text="Admin ingrese el valor del tiempo (número entero) en minutos")
        error_txt = None
        while True:
            Interfaz.Pantalla.fill("white")
            menu_mouse_pos = pygame.mouse.get_pos()

            logo = Button(image=pygame.image.load("Icono.png"), pos=(25, 20), text_input="   ",
                                font=Interfaz.Get_font(20), base_color="#d7fcd4", hovering_color="White")

            Seguir_btn = Button(image=None, pos=(Interfaz.Ancho_pantalla/2, 650), text_input="SEGUIR",
                                font=Interfaz.Get_font(35), base_color="#000240", hovering_color="White")

            for button in [Seguir_btn, logo]:
                button.Update(Interfaz.Pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Seguir_btn.CheckForInput(menu_mouse_pos): 
                        try:
                            if Juego.Get_Tiempo_limite() != None and len(Juego.Get_Frases()) > 0:
                                Interfaz.__Registro_jugador_screen(Juego)
                            else:
                                raise RequisitoFaltante("El juego no puede continuar sin los requisitos pedidos")
                        except RequisitoFaltante as error:
                            error_txt = Interfaz.Get_font(8).render(error.mensaje, True, "Red")
                            rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2, 700))
                            error_start_time = pygame.time.get_ticks()

                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#entrada_frases":
                    try:
                        Juego.Get_Administrador().Asignar_Frases(Juego, event.text)
                    except FraseConTilde as error:
                        error_txt = Interfaz.Get_font(10).render(error.mensaje, True, "Red")

                    except PalabraNoExistente as error:
                        error_txt = Interfaz.Get_font(10).render(error.mensaje, True, "Red")

                    except FraseNoPermitida as error:
                        error_txt = Interfaz.Get_font(10).render(error.mensaje, True, "Red")
                    else:
                        input_frases.set_text("")
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,pos=(400,100))) 
                        time.sleep(0.1) 
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1,pos=(400,100)))
                        error_txt = Interfaz.Get_font(10).render("Frase guardada exitosamente", True, "Green")
                    rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2, 300))
                    error_start_time = pygame.time.get_ticks()

                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#entrada_tiempo":
                    try:
                        Juego.Get_Administrador().Asignar_tiempo_limite(Juego, event.text)
                    except ValueError:
                        error_txt = Interfaz.Get_font(10).render("El tiempo no pudo ser guardado, el valor ingresado no es entero", True, "Red")
                        rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2, 500))
                    else:
                        error_txt = Interfaz.Get_font(10).render("Tiempo guardado exitosamente", True, "Green")
                        rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2, 500))
                    error_start_time = pygame.time.get_ticks()
                
                Interfaz.Manager.process_events(event)
                
            if error_txt is not None:
                Interfaz.Pantalla.blit(error_txt, rect_error)
                time_since_error = pygame.time.get_ticks() - error_start_time
                if time_since_error >= 2000:
                    error_txt = None

            UI_REFRESH_RATE = Interfaz.Clock.tick(60)/1000
            Interfaz.Manager.update(UI_REFRESH_RATE)
            Interfaz.Manager.draw_ui(Interfaz.Pantalla)
            pygame.display.update()
        
    def __Registro_jugador_screen(Juego):
        id_existentes = []
        pygame.display.set_caption("Registro de Jugadores")
        Interfaz.Manager = pygame_gui.UIManager(Interfaz.Pantalla.get_size())
        input_nombre = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((Interfaz.Ancho_pantalla/3, 200), (500, 60),),
                                                            manager=Interfaz.Manager, object_id="#entrada_nombre",
                                                            placeholder_text="Ingrese el nombre")
        
        input_numero = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((Interfaz.Ancho_pantalla/3, 400), (500, 60)),
                                                            manager=Interfaz.Manager, object_id="#entrada_numero",
                                                            placeholder_text="Ingrese el número identificador  (máximo dos dígitos tipo entero)")

        error_txt = None
        jugador = [None, None]
        while True:
            Interfaz.Pantalla.fill("white")
            menu_mouse_pos = pygame.mouse.get_pos()

            Interfaz.Añadir_texto("Registro de equipos", 25, (Interfaz.Ancho_pantalla/2,100), pygame.Color("#000240"))

            logo = Button(image=pygame.image.load("Icono.png"), pos=(25, 20), text_input="   ",
                                font=Interfaz.Get_font(20), base_color="#d7fcd4", hovering_color="White")

            jugar_btn = Button(image=None, pos=(Interfaz.Ancho_pantalla/2, 690), text_input="JUGAR",
                                font=Interfaz.Get_font(35), base_color="#000240", hovering_color="White")

            for button in [jugar_btn, logo]:
                button.Update(Interfaz.Pantalla)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if jugar_btn.CheckForInput(menu_mouse_pos):
                        try:
                            if len(Juego.Get_Jugadores()) > 0:
                                Juego.Siguiente_turno()
                            else:
                                raise RequisitoFaltante("El juego no puede continuar sin jugadores registrados")
                        except RequisitoFaltante as error:
                            error_txt = Interfaz.Get_font(10).render(error.mensaje, True, "Red")
                            rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2, 730))
                            error_start_time = pygame.time.get_ticks()

                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#entrada_nombre":
                    try:
                        if len(event.text) == 0:
                            raise NombreNoPermitido("El nombre debe tener al menos una letra")
                    except NombreNoPermitido as error:
                        error_txt = Interfaz.Get_font(10).render(error.mensaje, True, "Red")
                    else:
                        jugador[0] = event.text
                        error_txt = Interfaz.Get_font(10).render("Nombre guardado", True, "Green")
                    rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2, 300))
                    error_start_time = pygame.time.get_ticks()

                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#entrada_numero":
                    numero_jugador = event.text
                    try:
                        int(numero_jugador)
                        if len(numero_jugador) > 2 or len(numero_jugador) == 0:
                            raise NumeroNoPermitido("Este número no es permitido por su tamaño")
                        existente = Juego.Existente_numero_jugador(numero_jugador)
                        if existente == True:
                            raise NumeroNoPermitido("Este número ya fue ingresado, intente con uno diferente")
                    except ValueError:
                        error_txt = Interfaz.Get_font(10).render("El valor ingresado no es del tipo pedido", True, "Red")

                    except NumeroNoPermitido as error:
                        error_txt = Interfaz.Get_font(10).render(error.mensaje, True, "Red")

                    else:
                        id_existentes.append(numero_jugador)
                        jugador[1] = numero_jugador
                        error_txt = Interfaz.Get_font(10).render("Número guardado", True, "Green")
                    rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2, 360))
                    error_start_time = pygame.time.get_ticks()
                
                Interfaz.Manager.process_events(event)

                if jugador[0] != None and jugador[1] != None:
                    Jugador(jugador[0],jugador[1]).Registrar(Juego)
                    jugador[0], jugador[1] = None, None
                    error_txt = Interfaz.Get_font(20).render("Jugador Registrado", True, "Green")
                    input_nombre.set_text("")
                    input_numero.set_text("")
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,pos=(400,100))) 
                    time.sleep(0.1) 
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1,pos=(400,100)))
                    rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla / 2, 500))
                    error_start_time = pygame.time.get_ticks()

            if error_txt is not None:
                Interfaz.Pantalla.blit(error_txt, rect_error)
                time_since_error = pygame.time.get_ticks() - error_start_time
                if time_since_error >= 2000:
                    error_txt = None

            UI_REFRESH_RATE = Interfaz.Clock.tick(60)/1000
            Interfaz.Manager.update(UI_REFRESH_RATE)
            Interfaz.Manager.draw_ui(Interfaz.Pantalla)
            pygame.display.update()

    def Jugar_screen(Juego, palabra_adivinada=None, flag=False, jugador=None):
        global guesses, current_letter_bg_x, guesses_count, current_guess_string, current_guess, palabras_adivinadas, timer
        pygame.display.set_caption("Jugar")
        Interfaz.Pantalla.fill("white")

        if palabra_adivinada != None:
            palabras_adivinadas.append(palabra_adivinada)

        if flag == False:
            palabras_adivinadas = []
            timer = pygame.time.get_ticks()
            flag=True

        try:
            Juego.Asignar_Palabra_objetivo()
        except PalabrasAdivinadas as e:
            #Adivinó todas las palabras de la frase
            Interfaz.Añadir_texto(e.mensaje, 15, (Interfaz.Ancho_pantalla/2+40, 500), "green")
            pygame.display.update()
            time.sleep(3)
            Interfaz.Adivinar_frase_screen(Juego, jugador, palabras_adivinadas)

        indicator_x = (Interfaz.Ancho_pantalla/2)+420
        indicator_y = 120
        for palabra in palabras_adivinadas:
            Interfaz.Añadir_texto("Palabras Acertadas", 15, (Interfaz.Ancho_pantalla/2+470,90), pygame.Color("#000240"))
            new_indicator = Letra(palabra, indicator_x, indicator_y)
            new_indicator.color_fondo = "#6aaa64"
            new_indicator.dibujar(Interfaz.Pantalla)
            indicator_y += 55

        Interfaz.Añadir_texto("Turno de:", 20, (210,80), "#000240")
        Interfaz.Añadir_texto(f"Jugador {jugador.Nombre}, num: {jugador.Numero}", 10, (200,150), "#000240")
        Longitud_palabra = Juego.Longitud_Palabra_objetivo()
        guesses_count = 0
        guesses = [[]] * Juego.Get_Intentos_palabra()
        current_guess = []
        current_guess_string = ""

        # show time
        Interfaz.Añadir_texto("Tiempo restante", 17, (Interfaz.Ancho_pantalla/2+470, 20), "#000240")

        ALPHABET = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"]
        indicator_x = Interfaz.Ancho_pantalla/3
        indicator_y = 550
        for i in range(3):
            for letra in ALPHABET[i]:
                new_indicator = Letra(letra, indicator_x, indicator_y)
                indicators.append(new_indicator)
                new_indicator.dibujar(Interfaz.Pantalla)
                indicator_x += 50
            indicator_y += 70
            if i == 0:
                indicator_x = Interfaz.Ancho_pantalla/3
            elif i == 1:
                indicator_x = (Interfaz.Ancho_pantalla/3)+80

        indicator_y = 130
        for i in range(Juego.Get_Intentos_palabra()):
            if Longitud_palabra == 1:
                indicator_x = (Interfaz.Ancho_pantalla/3)+220
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+220
            if Longitud_palabra == 2:
                indicator_x = (Interfaz.Ancho_pantalla/3)+195
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+195
            elif Longitud_palabra == 3:
                indicator_x = (Interfaz.Ancho_pantalla/3)+165
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+165
            elif Longitud_palabra == 4:
                indicator_x = (Interfaz.Ancho_pantalla/3)+147
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+147
            elif Longitud_palabra == 5:
                indicator_x = (Interfaz.Ancho_pantalla/3)+120
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+120
            elif Longitud_palabra == 6:
                indicator_x = (Interfaz.Ancho_pantalla/3)+100
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+100
            elif Longitud_palabra == 7:
                indicator_x = (Interfaz.Ancho_pantalla/3)+78
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+78
            elif Longitud_palabra == 8:
                indicator_x = (Interfaz.Ancho_pantalla/3)+48
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+48
            elif Longitud_palabra == 9:
                indicator_x = (Interfaz.Ancho_pantalla/3)+18
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+18
            elif Longitud_palabra == 10:
                indicator_x = (Interfaz.Ancho_pantalla/3)-5
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-5
            elif Longitud_palabra == 11:
                indicator_x = (Interfaz.Ancho_pantalla/3)-30
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-30
            elif Longitud_palabra == 12:
                indicator_x = (Interfaz.Ancho_pantalla/3)-55
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-55
            elif Longitud_palabra == 13:
                indicator_x = (Interfaz.Ancho_pantalla/3)-75
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-75
            else:
                indicator_x = (Interfaz.Ancho_pantalla/3)
                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)

            for letra in Juego.Palabra_objetivo.Palabra:
                new_indicator = Letra('   ', indicator_x, indicator_y)
                new_indicator.color_fondo = "#999999"
                new_indicator.dibujar(Interfaz.Pantalla)
                indicator_x += 50
            indicator_y += 70

        error_txt = None
        while True:
            logo = Button(image=pygame.image.load("Icono.png"), pos=(25, 20), text_input="   ",
                                font=Interfaz.Get_font(20), base_color="#d7fcd4", hovering_color="White")

            for button in [logo]:
                button.Update(Interfaz.Pantalla)
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(current_guess_string) == Longitud_palabra and current_guess_string.lower() in Juego.Get_diccionario():
                            jugador.AdivinarPalabra(current_guess, Juego)
                            guesses_count += 1
                            current_guess = []
                            current_guess_string = ""
                            if Juego.Longitud_Palabra_objetivo() == 1:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+220
                            elif Juego.Longitud_Palabra_objetivo() == 2:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+195
                            elif Juego.Longitud_Palabra_objetivo() == 3:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+165
                            elif Juego.Longitud_Palabra_objetivo() == 4:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+147
                            elif Juego.Longitud_Palabra_objetivo() == 5:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+120
                            elif Juego.Longitud_Palabra_objetivo() == 6:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+100
                            elif Juego.Longitud_Palabra_objetivo() == 7:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+78
                            elif Juego.Longitud_Palabra_objetivo() == 8:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+48
                            elif Juego.Longitud_Palabra_objetivo() == 9:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)+18
                            elif Juego.Longitud_Palabra_objetivo() == 10:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-5
                            elif Juego.Longitud_Palabra_objetivo() == 11:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-30
                            elif Juego.Longitud_Palabra_objetivo() == 12:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-55
                            elif Juego.Longitud_Palabra_objetivo() == 13:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-75
                            else:
                                current_letter_bg_x = (Interfaz.Ancho_pantalla/3)-100

                            if guesses_count == Juego.Intentos_palabra:
                                Interfaz.Añadir_texto("Has perdido", 40, (Interfaz.Ancho_pantalla/2+30, 500), "#FF0000")
                                pygame.display.update()
                                time.sleep(3)
                                Juego.Siguiente_turno()
                        elif current_guess_string.lower() not in Juego.Get_diccionario() and len(current_guess_string)>0:
                            error_txt = Interfaz.Get_font(17).render("Palabra inexistente", True, "Red")
                            rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2+20, 500))
                            error_start_time = pygame.time.get_ticks()
                        elif len(current_guess_string) < Longitud_palabra and len(current_guess_string):
                            error_txt = Interfaz.Get_font(17).render("Palabra demasiada corta", True, "Red")
                            rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2+20, 500))
                            error_start_time = pygame.time.get_ticks()


                    elif event.key == pygame.K_BACKSPACE:
                        if len(current_guess_string) > 0:
                            Interfaz.__borrar_letra(guesses)
                    else:
                        key_pressed = event.unicode.upper()
                        if key_pressed in "QWERTYUIOPASDFGHJKLÑZXCVBNM" and key_pressed != "":
                            if len(current_guess_string) < Longitud_palabra:
                                Interfaz.__Mostrar_letra(key_pressed)

            
            if error_txt is not None:
                Interfaz.Pantalla.blit(error_txt, rect_error)
                time_since_error = pygame.time.get_ticks() - error_start_time
                if time_since_error >= 2000:
                    error_txt = None
                    Interfaz.Añadir_texto("                                              ", 40, (Interfaz.Ancho_pantalla/2+20, 500), "white", "white")
                    pygame.display.update()

            UI_REFRESH_RATE = Interfaz.Clock.tick(60)/1000
            Interfaz.Manager.update(UI_REFRESH_RATE)
            # Interfaz.Manager.draw_ui(Interfaz.Pantalla)

            # timer
            current_timer = pygame.time.get_ticks()
            if current_timer - timer > Juego.Tiempo_limite*60000:
                Interfaz.Pantalla.fill("white")
                Interfaz.Añadir_texto("Has perdido", 50, (Interfaz.Ancho_pantalla/2+30, 500), "#FF0000")
                pygame.display.update()
                time.sleep(3)
                Interfaz.Menu_screen(Juego)
            Interfaz.Añadir_texto(f"{(Juego.Tiempo_limite*60000-(current_timer - timer))/1000} sec", 15, (Interfaz.Ancho_pantalla/2+470, 50), "#000240", None, False)


    
    def Adivinar_frase_screen(Juego, jugador, palabrasAdivinadas):
        pygame.display.set_caption("Adivinar frase")
        Interfaz.Manager = pygame_gui.UIManager(Interfaz.Pantalla.get_size())
        input_frase = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((Interfaz.Ancho_pantalla/3, 250), (500, 60),),
                                                            manager=Interfaz.Manager, object_id="#entrada_frase",
                                                            placeholder_text="Ingresa la frase con las palabras encontradas")
        intentos=0
        error_txt = None
        while True:
            Interfaz.Pantalla.fill("white")
            Interfaz.Añadir_texto(f"Intentos: {2-intentos}", 17, (Interfaz.Ancho_pantalla/2+500, 50), pygame.Color("#000240"))

            Interfaz.Añadir_texto("Adivina la frase con las palabras", 25, (Interfaz.Ancho_pantalla/2,100), pygame.Color("#000240"))
            indicator_x = (Interfaz.Ancho_pantalla/2)-300
            indicator_y = 130
            for palabra in palabrasAdivinadas:
                new_indicator = Letra(palabra, indicator_x, indicator_y)
                new_indicator.color_fondo = "#6aaa64"
                new_indicator.dibujar(Interfaz.Pantalla, False)
                indicator_x += 150
            

            logo = Button(image=pygame.image.load("Icono.png"), pos=(25, 20), text_input="   ",
                            font=Interfaz.Get_font(35), base_color="#000240", hovering_color="White")
            
            for button in [logo]:
                button.Update(Interfaz.Pantalla)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#entrada_frase":
                    try:
                        Juego.Verificar_frase(event.text)
                    except:
                        error_txt = Interfaz.Get_font(30).render("Has fallado", True, "Red")
                        intentos += 1
                        input_frase.set_text("")
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1,pos=(500,600))) 
                        time.sleep(0.1) 
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1,pos=(500,600)))
                        if intentos == 2:
                            Interfaz.Añadir_texto("Has perdido", 40, (Interfaz.Ancho_pantalla/2+30, 500), "#FF0000")
                            pygame.display.update()
                            time.sleep(3)
                            Juego.Siguiente_turno()
                    else:
                        Interfaz.Añadir_texto("Has acertado!", 20, (Interfaz.Ancho_pantalla/2+50, 400), "#6aaa64")
                        Interfaz.Añadir_texto(f"Jugador {jugador.Nombre}, num: {jugador.Numero}", 20, (Interfaz.Ancho_pantalla/2+50, 500), pygame.Color("#000240"))
                        jugador.Puntuacion += 1
                        Interfaz.Añadir_texto(f"Ahora tu puntaje es {jugador.Puntuacion}", 20, (Interfaz.Ancho_pantalla/2+50, 600), "#6aaa64")
                        pygame.display.update()
                        time.sleep(3)

                        # Seguir otro jugador adivinar palabras
                        Juego.Frase_objetivo.Adivinada = True
                        Juego.Siguiente_turno()

                    rect_error = error_txt.get_rect(center=(Interfaz.Ancho_pantalla/2, 450))
                    error_start_time = pygame.time.get_ticks()

                Interfaz.Manager.process_events(event)
            
            if error_txt is not None:
                Interfaz.Pantalla.blit(error_txt, rect_error)
                time_since_error = pygame.time.get_ticks() - error_start_time
                if time_since_error >= 2000:
                    error_txt = None

            UI_REFRESH_RATE = Interfaz.Clock.tick(60)/1000
            Interfaz.Manager.update(UI_REFRESH_RATE)
            Interfaz.Manager.draw_ui(Interfaz.Pantalla)
            pygame.display.update()


    def Resultados_screen(Juego):
        pygame.display.set_caption("Resultados")
        Interfaz.Pantalla.fill("white")
        admin = Juego.Administrador
        Interfaz.Añadir_texto("Resultados", 25, (Interfaz.Ancho_pantalla/2,90), pygame.Color("#000240"))
        Interfaz.Añadir_texto("Jugador", 20, (Interfaz.Ancho_pantalla/2,180), pygame.Color("#000240"))
        
        indicator_y = 220
        for jugador in Juego.Jugadores:
            Interfaz.Añadir_texto(jugador.Nombre+" :"+" "*10+str(jugador.Puntuacion), 15, (Interfaz.Ancho_pantalla/2, indicator_y), pygame.Color("#000240"))
            indicator_y += 30
            Reiniciar = Button(image=None, pos=(Interfaz.Ancho_pantalla / 2, 700), text_input="REINICIAR JUEGO",
                                font=Interfaz.Get_font(30), base_color="#000240", hovering_color="White")

        logo = Button(image=pygame.image.load("Icono.png"), pos=(25, 20), text_input="   ",
                            font=Interfaz.Get_font(20), base_color="#d7fcd4", hovering_color="White")

        for button in [Reiniciar, logo]:
            button.Update(Interfaz.Pantalla)
        pygame.display.update()

        while True:
            menu_mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Reiniciar.CheckForInput(menu_mouse_pos):
                        gc.collect()
                        admin.Iniciar_juego()


            # pygame.display.update()



    def __Instrucciones_screen(Juego):
        pygame.display.set_caption("Instrucciones")
        while True:
            Interfaz.Pantalla.fill("white")
            menu_mouse_pos = pygame.mouse.get_pos()

            Interfaz.Añadir_texto("INSTRUCCIONES:", 35, (Interfaz.Ancho_pantalla / 2, 100), pygame.Color("#000240"))
            
            Interfaz.Añadir_texto("1. Se deben definir los roles del juego ( admin y jugadores ).",
                                     12, (Interfaz.Ancho_pantalla / 2, 170), "black")

            Interfaz.Añadir_texto("2. El admin debe ingresar la estructura base del juego ( frases y tiempo límite ).",
                                     12, (Interfaz.Ancho_pantalla / 2, 210), "black")

            Interfaz.Añadir_texto("Tener en cuenta que las frases deben ser mínimo 4 y máximo 6 palabras. (conectores COMO 'en', 'lo', 'de' no cuentan como palabra pero son permitidas).",
                                     8, (Interfaz.Ancho_pantalla / 2, 235), "black")

            Interfaz.Añadir_texto("3. Los jugadores deben registrarse con nombre y número identificador.",
                                     12, (Interfaz.Ancho_pantalla / 2, 270), "black")

            Interfaz.Añadir_texto("Para que se guarden los datos, debes presionar 'ENTER' al terminar de llenar el campo.",
                                     12, (Interfaz.Ancho_pantalla / 2, 660), "red")

            volver_btn = Button(image=None, pos=(Interfaz.Ancho_pantalla / 2, 700), text_input="VOLVER",
                                font=Interfaz.Get_font(30), base_color="#000240", hovering_color="White")

            logo = Button(image=pygame.image.load("Icono.png"), pos=(25, 20), text_input="   ",
                                font=Interfaz.Get_font(20), base_color="#d7fcd4", hovering_color="White")

            for button in [volver_btn, logo]:
                button.Update(Interfaz.Pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if volver_btn.CheckForInput(menu_mouse_pos):
                        Interfaz.Menu_screen(Juego)
            pygame.display.update()

    def Get_font(size):
        return pygame.font.Font("Retro Team.otf", size+10)

    def __Mostrar_letra(tecla):
        global current_guess_string, current_letter_bg_x
        current_guess_string += tecla
        pos_y = 132
        for i in range(guesses_count):
            pos_y += 70
        new_letter = Letra(tecla, current_letter_bg_x, pos_y)
        current_letter_bg_x += 50
        guesses[guesses_count].append(new_letter)
        current_guess.append(new_letter)
        for guess in guesses:
            for letter in guess:
                letter.dibujar(Interfaz.Pantalla)

    def __borrar_letra(intento):
        # Deletes the last letra from the guess.
        global guesses_count, current_guess_string, current_letter_bg_x
        intento[guesses_count][-1].eliminar(Interfaz.Pantalla)
        intento[guesses_count].pop()
        current_guess_string = current_guess_string[:-1]
        current_guess.pop()
        current_letter_bg_x -= 50

    def Pintar_letra(letra, color):
        global indicators
        letra.color_fondo = color
        for indicator in indicators:
            if indicator == letra:
                if indicator.color_fondo == "white" or  indicator.color_fondo == "#d3d6da":
                    indicator.color_fondo = color
                elif color == "#6aaa64":
                    indicator.color_fondo = color
                elif color == "#c9b458" and indicator.color_fondo != "#6aaa64": 
                    indicator.color_fondo = color
                indicator.dibujar(Interfaz.Pantalla)
        letra.color_texto = "white"
        letra.dibujar(Interfaz.Pantalla)

    def Añadir_texto(texto="", tamaño:int=0, posicion:tuple=(0,0), colorLetra="black", colorFondo=None, punto=True):
        if "." in texto and punto == False:
            texto = texto.split(".")
            unit = texto[1].split(" ")
            texto = texto[0] + " "+unit[1]
            blanquear = Interfaz.Get_font(tamaño).render("         ", True, "white", "white")
            rect_blanq = blanquear.get_rect(center=posicion)
            Interfaz.Pantalla.blit(blanquear, rect_blanq)
        textoAñadir = Interfaz.Get_font(tamaño).render(texto, True, colorLetra, colorFondo)
        rect_texto = textoAñadir.get_rect(center=posicion)
        Interfaz.Pantalla.blit(textoAñadir, rect_texto)