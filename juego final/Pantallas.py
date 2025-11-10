import pygame
import sys
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40 # Tamaño base para los segmentos del Snake
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (200, 0, 0)

class Pantallas:
    # Usaremos main_screen_bg para mayor claridad
    def __init__(self, screen, main_screen_bg, loading_truck_img): 
        self.screen = screen
        self.main_screen_bg = main_screen_bg
        self.loading_truck_img = loading_truck_img
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 36)

    def main_menu(self):
        waiting = True
        while waiting:
            self.screen.blit(self.main_screen_bg, (0, 0)) # Usa self.main_screen_bg
            
            # Dibujar el texto de "Press Enter"
            start_text = self.font_medium.render("COMIENZA EL JUEGO ", True, BLACK)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 84))
            self.screen.blit(start_text, start_rect)
            # Define el radio de las esquinas (puedes ajustar este valor)
            # 2. Definir el área del botón (ligeramente más grande que el texto)
            #button_rect = start_rect.inflate(40, 20)  # Expande el rectángulo 40px a los lados, 20px arriba/abajo
            button_rect_inner = start_rect.inflate(40, 20)
            button_rect_outer = button_rect_inner.inflate(4, 4)
            radio_esquina = 10
            #Spygame.draw.rect(self.screen, GREEN, button_rect, border_radius=radio_esquina)  # Dibuja un rectángulo rojo
            pygame.draw.rect(self.screen, BLACK, button_rect_outer, border_radius=radio_esquina)
            pygame.draw.rect(self.screen, GREEN, button_rect_inner, border_radius=radio_esquina)
            
            
            # Dibujar el texto EN EL CENTRO del rectángulo
            self.screen.blit(start_text, start_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    #if button_rect.collidepoint(mouse_pos):
                        #waiting = False
                    if button_rect_outer.collidepoint(mouse_pos): 
                        waiting = False
       
    
    def loading_screen(self, load_time=2):
        # ... (La lógica de carga está correcta y no se modifica) ...
        self.screen.fill(LIGHT_GREEN)
        
        # Posiciones fijas para los elementos de la carga
        bar_outline_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100, 400, 30)
        truck_x = (SCREEN_WIDTH // 2) - (self.loading_truck_img.get_width() // 2)
        truck_y = (SCREEN_HEIGHT // 2) - self.loading_truck_img.get_height() - 30

        start_time = time.time()
        elapsed_time = 0
        
        while elapsed_time < load_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            elapsed_time = time.time() - start_time
            progress = min(elapsed_time / load_time, 1.0) 

            self.screen.fill(LIGHT_GREEN)
            
            # Dibujar carretera y Amarok
            pygame.draw.rect(self.screen, LIGHT_GREEN, (0, SCREEN_HEIGHT // 2 - 20, SCREEN_WIDTH, 40))
            self.screen.blit(self.loading_truck_img, (truck_x, truck_y))
            
            # Dibujar texto
            loading_text = self.font_small.render("CARGANDO....", True, BLACK)
            loading_text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(loading_text, loading_text_rect)

            # Dibujar barra de progreso
            pygame.draw.rect(self.screen, BLACK, bar_outline_rect, 3)
            filled_width = int(bar_outline_rect.width * progress)
            filled_rect = pygame.Rect(bar_outline_rect.x, bar_outline_rect.y, filled_width, bar_outline_rect.height)
            pygame.draw.rect(self.screen, GREEN, filled_rect)

            pygame.display.flip()
    
    def game_over_screen(self, score):
        """Pantalla de game over con puntuación (versión reutilizable)"""
        waiting = True
        font_large = pygame.font.Font(None, 80)
        font_medium = pygame.font.Font(None, 50)
        font_small = pygame.font.Font(None, 36)

        while waiting:
            self.screen.blit(self.main_screen_bg, (0, 0))

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(game_over_text, game_over_rect)

            score_text = font_medium.render(f"Puntuación: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(score_text, score_rect)

            restart_text = font_small.render("REINICIAR (ENTER)", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
            restart_button_inner = restart_rect.inflate(40, 20)
            restart_button_outer = restart_button_inner.inflate(4, 4)

            pygame.draw.rect(self.screen, BLACK, restart_button_outer, border_radius=10)
            pygame.draw.rect(self.screen, GREEN, restart_button_inner, border_radius=10)
            self.screen.blit(restart_text, restart_rect)

            exit_text = font_small.render("SALIR (ESC)", True, BLACK)
            exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
            exit_button_inner = exit_rect.inflate(40, 20)
            exit_button_outer = exit_button_inner.inflate(4, 4)

            pygame.draw.rect(self.screen, BLACK, exit_button_outer, border_radius=10)
            pygame.draw.rect(self.screen, RED, exit_button_inner, border_radius=10)
            self.screen.blit(exit_text, exit_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "restart"
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button_outer.collidepoint(event.pos):
                        return "restart"
                    elif exit_button_outer.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()