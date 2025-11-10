"""
La Mandita Amarok - Versión Mejorada con Pantallas
Integra: Pantalla de inicio, carga, juego con imágenes, y game over
"""

import pygame
import sys
import time
import random
import os

# --- Constantes ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (200, 0, 0)
DARK_GREEN = (0, 100, 0)


class Screens:
    """Maneja las pantallas de inicio, carga y game over"""
    
    def __init__(self, screen, main_screen_bg, loading_truck_img):
        self.screen = screen
        self.main_screen_bg = main_screen_bg
        self.loading_truck_img = loading_truck_img
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 80)

    def main_menu(self):
        """Pantalla de inicio con fondo e instrucciones"""
        waiting = True
        while waiting:
            self.screen.blit(self.main_screen_bg, (0, 0))
            
            start_text = self.font_medium.render("COMIENZA EL JUEGO", True, BLACK)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 84))
            self.screen.blit(start_text, start_rect)
            
            button_rect_inner = start_rect.inflate(40, 20)
            button_rect_outer = button_rect_inner.inflate(4, 4)
            
            pygame.draw.rect(self.screen, BLACK, button_rect_outer, border_radius=10)
            pygame.draw.rect(self.screen, GREEN, button_rect_inner, border_radius=10)
            self.screen.blit(start_text, start_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect_outer.collidepoint(event.pos):
                        waiting = False

    def loading_screen(self, load_time=2):
        """Pantalla de carga con barra de progreso"""
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
            
            pygame.draw.rect(self.screen, LIGHT_GREEN, (0, SCREEN_HEIGHT // 2 - 20, SCREEN_WIDTH, 40))
            self.screen.blit(self.loading_truck_img, (truck_x, truck_y))
            
            loading_text = self.font_small.render("CARGANDO....", True, BLACK)
            loading_text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(loading_text, loading_text_rect)

            pygame.draw.rect(self.screen, BLACK, bar_outline_rect, 3)
            filled_width = int(bar_outline_rect.width * progress)
            filled_rect = pygame.Rect(bar_outline_rect.x, bar_outline_rect.y, filled_width, bar_outline_rect.height)
            pygame.draw.rect(self.screen, GREEN, filled_rect)

            pygame.display.flip()

    def game_over_screen(self, score):
        """Pantalla de game over con puntuación"""
        waiting = True
        while waiting:
            self.screen.blit(self.main_screen_bg, (0, 0))
            
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(game_over_text, game_over_rect)
            
            score_text = self.font_medium.render(f"Puntuación: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(score_text, score_rect)
            
            restart_text = self.font_small.render("REINICIAR (ENTER)", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
            restart_button_inner = restart_rect.inflate(40, 20)
            restart_button_outer = restart_button_inner.inflate(4, 4)
            
            pygame.draw.rect(self.screen, BLACK, restart_button_outer, border_radius=10)
            pygame.draw.rect(self.screen, GREEN, restart_button_inner, border_radius=10)
            self.screen.blit(restart_text, restart_rect)
            
            exit_text = self.font_small.render("SALIR (ESC)", True, BLACK)
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


class Snake:
    """Clase para el snake/serpiente"""
    
    def __init__(self, cell_size, amarok_img, caravan_imgs):
        self.cell_size = cell_size
        self.amarok_img = pygame.transform.scale(amarok_img, (cell_size * 2, cell_size))
        self.caravan_imgs = [pygame.transform.scale(img, (cell_size, cell_size)) for img in caravan_imgs]
        
        start_x = SCREEN_WIDTH // 2 - self.amarok_img.get_width() // 2
        start_y = SCREEN_HEIGHT // 2 - self.amarok_img.get_height() // 2
        
        self.body = [(start_x, start_y)]
        self.caravans_type = []
        self.direction = "RIGHT"
        self.new_direction = self.direction

    def set_direction(self, direction):
        if direction == "UP" and self.direction != "DOWN":
            self.new_direction = direction
        elif direction == "DOWN" and self.direction != "UP":
            self.new_direction = direction
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.new_direction = direction
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.new_direction = direction

    def move(self):
        self.direction = self.new_direction
        head_x, head_y = self.body[0]
        
        if self.direction == "UP":
            head_y -= self.cell_size
        elif self.direction == "DOWN":
            head_y += self.cell_size
        elif self.direction == "LEFT":
            head_x -= self.cell_size
        elif self.direction == "RIGHT":
            head_x += self.cell_size
        
        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

    def grow(self, caravan_type_index):
        self.caravans_type.append(caravan_type_index)

    def draw(self, screen):
        screen.blit(self.amarok_img, self.body[0])
        
        for i, segment in enumerate(self.body[1:]):
            caravan_index = self.caravans_type[i]
            caravan_to_draw = self.caravan_imgs[caravan_index]
            screen.blit(caravan_to_draw, segment)

    def check_collision(self):
        head = self.body[0]
        if not (0 <= head[0] < SCREEN_WIDTH and 0 <= head[1] < SCREEN_HEIGHT):
            return True
        if head in self.body[2:]:
            return True
        return False

    @property
    def head_rect(self):
        return pygame.Rect(self.body[0][0], self.body[0][1], 
                          self.amarok_img.get_width(), self.amarok_img.get_height())


class Game:
    """Clase principal del juego"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("La Mandita Amarok")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.font_score = pygame.font.Font(None, 36)
        
        self.snake = None
        self.caravan_types_available = 0
        self.current_fruit_index = 0
        self.fruit_pos = (0, 0)
        self.amarok_game_img = None
        self.loading_truck_img = None
        self.main_screen_bg = None
        self.caravan_imgs = []
        self.fruit_img = None
        
        self.load_assets()
        self.screens = Screens(self.screen, self.main_screen_bg, self.loading_truck_img)

    def load_assets(self):
        """Cargar imágenes desde proyecto juego"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            proyecto_juego_dir = os.path.join(parent_dir, "proyecto juego")
            
            self.main_screen_bg = pygame.image.load(os.path.join(proyecto_juego_dir, 'imagen_amarock.jpg')).convert()
            self.main_screen_bg = pygame.transform.scale(self.main_screen_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            self.loading_truck_img = pygame.image.load(os.path.join(proyecto_juego_dir, 'amarok.png')).convert_alpha()
            self.loading_truck_img = pygame.transform.scale(self.loading_truck_img, (150, 75))
            
            self.amarok_game_img = pygame.image.load(os.path.join(proyecto_juego_dir, 'amarok.png')).convert_alpha()
            
            self.caravan_imgs = [
                pygame.image.load(os.path.join(proyecto_juego_dir, 'casa1.png')).convert_alpha(),
                pygame.image.load(os.path.join(proyecto_juego_dir, 'casa2.png')).convert_alpha(),
                pygame.image.load(os.path.join(proyecto_juego_dir, 'casa3.png')).convert_alpha(),
            ]
        except pygame.error as e:
            print(f"Error al cargar imágenes: {e}")
            pygame.quit()
            sys.exit()

    def generate_fruit_pos(self):
        while True:
            x = random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE
            y = random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake.body:
                return (x, y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.set_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.snake.set_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction("RIGHT")
                elif event.key == pygame.K_w:
                    self.snake.set_direction("UP")
                elif event.key == pygame.K_s:
                    self.snake.set_direction("DOWN")
                elif event.key == pygame.K_a:
                    self.snake.set_direction("LEFT")
                elif event.key == pygame.K_d:
                    self.snake.set_direction("RIGHT")

    def update(self):
        self.snake.move()
        
        fruit_rect = pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], CELL_SIZE, CELL_SIZE)
        if self.snake.head_rect.colliderect(fruit_rect):
            self.snake.grow(self.current_fruit_index)
            self.score += 10
            self.caravan_types_available = len(self.caravan_imgs)
            self.current_fruit_index = random.randrange(self.caravan_types_available)
            self.fruit_img = self.caravan_imgs[self.current_fruit_index]
            self.fruit_img = pygame.transform.scale(self.fruit_img, (CELL_SIZE, CELL_SIZE))
            self.fruit_pos = self.generate_fruit_pos()
        else:
            self.snake.body.pop()
        
        if self.snake.check_collision():
            return False
        return True

    def draw(self):
        self.screen.blit(self.main_screen_bg, (0, 0))
        
        road_surf = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
        road_surf.fill((0, 150, 0, 50))
        self.screen.blit(road_surf, (0, SCREEN_HEIGHT // 2 - 50))
        
        self.screen.blit(self.fruit_img, self.fruit_pos)
        self.snake.draw(self.screen)
        
        score_text = self.font_score.render(f"Puntuación: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(30, 30))
        score_bg = pygame.Surface((score_rect.width + 20, score_rect.height + 10), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 150))
        self.screen.blit(score_bg, (20, 20))
        self.screen.blit(score_text, score_rect)
        
        pygame.display.flip()

    def run(self):
        self.screens.main_menu()
        self.screens.loading_screen()
        
        while True:
            self.snake = Snake(CELL_SIZE, self.amarok_game_img, self.caravan_imgs)
            self.caravan_types_available = len(self.caravan_imgs)
            self.current_fruit_index = random.randrange(self.caravan_types_available)
            
            self.fruit_img = self.caravan_imgs[self.current_fruit_index]
            self.fruit_img = pygame.transform.scale(self.fruit_img, (CELL_SIZE, CELL_SIZE))
            self.fruit_pos = self.generate_fruit_pos()
            self.score = 0
            self.running = True
            
            while self.running:
                self.handle_events()
                if not self.update():
                    break
                self.draw()
                self.clock.tick(5)
            
            action = self.screens.game_over_screen(self.score)
            if action == "restart":
                continue
            else:
                break
        
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
