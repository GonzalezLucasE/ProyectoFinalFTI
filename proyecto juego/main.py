import pygame
import sys
import time
import random


class Vista_pantalla(): #ajuste de pantalla
    def __init__(self, screen, main_screen, cargando_camioneta):
        self.screen = screen
        self.main_screen = main_screen
        self.cargando_camioneta = cargando_camioneta
        self.font_medium = pygame.font.Font(None, 50)  #para crear objetos para usar manejo de fuentes
        self.font_small = pygame.font.Font(None, 36)
        import pygame
import sys
import time
import random

# --- Constantes y Colores ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40 # Tamaño base para los segmentos del Snake
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (200, 0, 0)

# ----------------------------------------------------------------------
## Clase Snake: Maneja la lógica de la Amarok y las Caravanas
# ----------------------------------------------------------------------

class Snake(pygame.sprite.Sprite):
    def __init__(self, cell_size, amarok_img, caravan_imgs):
        super().__init__()
        self.cell_size = cell_size
        self.amarok_img = pygame.transform.scale(amarok_img, (cell_size * 2, cell_size))
        self.caravan_imgs = [pygame.transform.scale(img, (cell_size, cell_size)) for img in caravan_imgs]

        # Posición inicial: Centrada en el camino (Simplificado para el ejemplo)
        start_x = SCREEN_WIDTH // 2 - self.amarok_img.get_width() // 2
        start_y = SCREEN_HEIGHT // 2 - self.amarok_img.get_height() // 2
        
        # El cuerpo (body) almacena las coordenadas (x, y) de cada segmento
        self.body = [(start_x, start_y)]
        # Nueva lista para almacenar el tipo de imagen de cada caravana en el cuerpo
        self.caravans_type = []
        # Añadir 3 caravanas iniciales detrás de la Amarok (cabeza)
        #for i in range(1, 4):
            # Posiciona las caravanas inmediatamente detrás de la anterior
            #self.body.append((start_x - (cell_size * i), start_y))
        self.direction = "RIGHT"
        self.new_direction = self.direction

    def set_direction(self, direction):
        # Evita que el snake se mueva inmediatamente en la dirección opuesta
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
        
        # 1. Mover la cabeza (Amarok)
        head_x, head_y = self.body[0]
        
        if self.direction == "UP":
            head_y -= self.cell_size
        elif self.direction == "DOWN":
            head_y += self.cell_size
        elif self.direction == "LEFT":
            head_x -= self.cell_size
        elif self.direction == "RIGHT":
            head_x += self.cell_size

        # 2. Insertar la nueva posición de la cabeza
        new_head = (head_x, head_y)
        self.body.insert(0, new_head)
        
        # 3. Eliminar la cola (mantiene el mismo tamaño si no ha comido)
        self.body.pop()
    def grow(self, caravan_type_index):
        # Añade un nuevo segmento al final
        self.body.append(self.body[-1])
        # Registra el tipo de imagen que debe usar el nuevo segmento
        self.caravans_type.append(caravan_type_index)
    #def grow(self):
        # Añade un nuevo segmento (caravana) al final del cuerpo
        # La posición real se calculará automáticamente en el siguiente frame de movimiento
        # Usamos la posición del último elemento como marcador temporal
        #self.body.append(self.body[-1]) 
    def draw(self, screen):
    # Dibujar la Amarok (cabeza)
        screen.blit(self.amarok_img, self.body[0])

    # Dibujar las caravanas (cuerpo)
    # self.body[1:] son las caravanas, y self.caravans_type tiene el índice de la imagen
        for i, segment in enumerate(self.body[1:]): 
        # Usa el tipo de caravana registrado en self.caravans_type
            caravan_index = self.caravans_type[i] 
            caravan_to_draw = self.caravan_imgs[caravan_index]
            screen.blit(caravan_to_draw, segment)
    #def draw(self, screen):
        # Dibujar la Amarok (cabeza)
        #screen.blit(self.amarok_img, self.body[0])

        # Dibujar las caravanas (cuerpo)
        #for i, segment in enumerate(self.body[1:]): # Ignora el primer segmento (cabeza)
            # Cicla entre los diferentes diseños de caravana
            #caravan_to_draw = self.caravan_imgs[i % len(self.caravan_imgs)]
            #screen.blit(caravan_to_draw, segment)

    def check_collision(self):
        head = self.body[0]
        # Colisión con los límites de la pantalla
        if not (0 <= head[0] < SCREEN_WIDTH and 0 <= head[1] < SCREEN_HEIGHT):
            return True # Game Over (colisión con borde)
        
        # Colisión con el cuerpo (la Amarok se choca con una caravana)
        if head in self.body[1:]:
            return True # Game Over (colisión con el cuerpo)
            
        return False
    
    # Propiedad para obtener el rectángulo de la cabeza (útil para colisiones)
    @property
    def head_rect(self):
        return pygame.Rect(self.body[0][0], self.body[0][1], self.amarok_img.get_width(), self.amarok_img.get_height())


# ----------------------------------------------------------------------
## Clase Screens: Maneja las pantallas de inicio y carga
# ----------------------------------------------------------------------

class Screens:
    def __init__(self, screen, main_screen_bg, loading_truck_img):
        self.screen = screen
        self.main_screen_bg = main_screen_bg
        self.loading_truck_img = loading_truck_img
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 36)

    def main_menu(self):
        waiting = True
        while waiting:
            self.screen.blit(self.main_screen_bg, (0, 0))
            
            # Dibujar el texto de "Press Enter"
            start_text = self.font_medium.render("PRESIONA ENTER PARA EMPEZAR", True, BLACK)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.screen.blit(start_text, start_rect)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
    
    def loading_screen(self, load_time=2):
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
            progress = min(elapsed_time / load_time, 1.0) # Asegura que no pase de 100%

            self.screen.fill(LIGHT_GREEN) # Limpiar fondo
            
            # Dibujar carretera y Amarok
            pygame.draw.rect(self.screen, BLACK, (0, SCREEN_HEIGHT // 2 - 20, SCREEN_WIDTH, 40))
            self.screen.blit(self.loading_truck_img, (truck_x, truck_y))
            
            # Dibujar texto
            loading_text = self.font_small.render("CARGANDO...", True, BLACK)
            loading_text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(loading_text, loading_text_rect)

            # Dibujar barra de progreso
            pygame.draw.rect(self.screen, BLACK, bar_outline_rect, 3)
            filled_width = int(bar_outline_rect.width * progress)
            filled_rect = pygame.Rect(bar_outline_rect.x, bar_outline_rect.y, filled_width, bar_outline_rect.height)
            pygame.draw.rect(self.screen, GREEN, filled_rect)

            pygame.display.flip()

# ----------------------------------------------------------------------
## Clase Game: Controla el flujo del juego
# ----------------------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Caravan Convoy Snake")
        self.clock = pygame.time.Clock()
        self.running = True
        #self.snake = Snake(CELL_SIZE, self.amarok_game_img, self.caravan_imgs)
        #self.fruit_pos = self.generate_fruit_pos()
        self.score = 0
        self.font_score = pygame.font.Font(None, 36)
        #self.caravan_types_available = len(self.caravan_imgs)
        #self.current_fruit_index = random.randrange(self.caravan_types_available) # Índice de la caravana actual que aparece
        #self.fruit_pos = self.generate_fruit_pos()
        # Inicializamos estas variables a None para que existan
        self.snake = None
        self.caravan_types_available = 0
        self.current_fruit_index = 0
        self.fruit_pos = (0, 0)
        self.amarok_game_img = None 
        self.loading_truck_img = None
        self.main_screen_bg = None
        self.caravan_imgs = []
        self.load_assets()
        self.screens = Screens(self.screen, self.main_screen, self.loading_truck_img)
    def load_assets(self):
        # --- Carga de imágenes ---
        try:
            # Pantalla de inicio (necesitas guardarla como 'main_screen.png')
            self.main_screen= pygame.image.load('imagen_amarock.jpg').convert() 
            self.main_screen= pygame.transform.scale(self.main_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
            # Imagen para la pantalla de carga (usaremos la Amarok)
            self.loading_truck_img = pygame.image.load('amarok.png').convert_alpha() 
            self.loading_truck_img = pygame.transform.scale(self.loading_truck_img, (150, 75))
            # Assets del juego (Amarok y Caravanas)
            self.amarok_game_img = pygame.image.load('amarok.png').convert_alpha()
            #LISTA CASA RODANTES
            self.caravan_imgs = [
                pygame.image.load('casa1.png').convert_alpha(),
                pygame.image.load('casa2.png').convert_alpha(),
                pygame.image.load('casa3.png').convert_alpha(),
                # Asegúrate de tener estas imágenes guardadas
            ]
            self.fruit_img = self.caravan_imgs[0]
            self.fruit_img = pygame.transform.scale(self.fruit_img, (CELL_SIZE, CELL_SIZE))
            #self.fruit_img = pygame.image.load('casa1.png').convert_alpha() # Necesitas una imagen de "manzana" o "fruta"
            
            
        except pygame.error as e:
            print(f"Error al cargar la imagen. Asegúrate de que los archivos PNG existen en la carpeta: {e}")
            pygame.quit()
            sys.exit()


    def update(self):
        self.snake.move()
    # 1. Colisión con la Fruta (Comer la Caravana)
        fruit_rect = pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], CELL_SIZE, CELL_SIZE)
        if self.snake.head_rect.colliderect(fruit_rect):
        # ¡La camioneta come la caravana! La añade al cuerpo con su índice de tipo.
            self.snake.grow(self.current_fruit_index) 
            self.score += 10
        # Generar nueva "fruta" (caravana)
        self.current_fruit_index = random.randrange(self.caravan_types_available)
        self.fruit_img = self.caravan_imgs[self.current_fruit_index] # Actualiza la imagen de la fruta
        self.fruit_img = pygame.transform.scale(self.fruit_img, (CELL_SIZE, CELL_SIZE)) # Re-escala la nueva imagen
        self.fruit_pos = self.generate_fruit_pos()
        
    def generate_fruit_pos(self):
        # Genera una posición aleatoria que no esté ocupada por el cuerpo de la serpiente
        while True:
            # Genera posiciones en base a la cuadrícula del CELL_SIZE
            x = random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE
            y = random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE
            # Asegúrate de que la fruta no aparezca sobre el snake
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

    #def update(self):
        #self.snake.move()
        
        # 1. Colisión con la Fruta (Comer)
        # La Amarok "come" la fruta si sus rectángulos se superponen
        #fruit_rect = pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], CELL_SIZE, CELL_SIZE)
        #if self.snake.head_rect.colliderect(fruit_rect):
            #self.snake.grow(self.current_fruit_index)
            #self.score += 10
            #self.fruit_pos = self.generate_fruit_pos()
        # 2. Colisión con Pared o Cuerpo (Game Over)
        #if self.snake.check_collision():
            #print(f"¡Game Over! Puntuación final: {self.score}")
            #self.running = False

    def draw(self):
        # Dibujar el fondo
        self.screen.fill(GREEN)
        pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH, 100)) # Camino
        
        # Dibujar la fruta
        self.screen.blit(self.fruit_img, self.fruit_pos)
        # Dibujar el Snake (Amarok )
        self.screen.blit(self.amarok_game_img, self.body[0])
        self.snake.draw(self.screen)
        # Dibujar las caravanas (cuerpo)
        for i, segment in enumerate(self.body[1:]): 
        # Usa el tipo de caravana registrado en self.caravans_type
            caravan_index = self.caravans_type[i] 
            caravan_to_draw = self.caravan_imgs[caravan_index]
            self.screen.blit(caravan_to_draw, segment)
        # Dibujar la puntuación
        score_text = self.font_score.render(f"Puntuación: {self.score}", True, BLACK)
        self.screen.blit(score_text, (30, 30))
        pygame.display.flip()
    def run(self):
    # 1. Mostrar pantallas de inicio y carga (garantiza que load_assets ya se ejecutó)
        self.screens.main_menu()
        self.screens.loading_screen()
    # 2. **INICIALIZACIÓN POST-CARGA (NUEVO)**
    # Creamos el objeto Snake y la lógica de la fruta aquí, donde los assets ya están cargados.
        self.snake = Snake(CELL_SIZE, self.amarok_game_img, self.caravan_imgs)
    # Inicialización de la lógica de la "fruta" (caravana)
        self.caravan_types_available = len(self.caravan_imgs)
        self.current_fruit_index = random.randrange(self.caravan_types_available)
    # Actualizamos la imagen y la posición de la fruta
        self.fruit_img = self.caravan_imgs[self.current_fruit_index] 
        self.fruit_img = pygame.transform.scale(self.fruit_img, (CELL_SIZE, CELL_SIZE)) 
        self.fruit_pos = self.generate_fruit_pos()
        #self.fruit_img = self.caravan_imgs[0]
        #self.fruit_img = pygame.transform.scale(self.fruit_pos, (CELL_SIZE, CELL_SIZE))
    #def run(self):
        # Mostrar pantallas de inicio y carga
        #self.screens.main_menu()
        #self.screens.loading_screen()
        # Bucle principal del juego
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(8) # Velocidad del juego (8 segmentos por segundo)

        pygame.quit()
        sys.exit()

# ----------------------------------------------------------------------
## Ejecución del Juego
# ----------------------------------------------------------------------






if __name__ == '__main__':
    game = Game()
    game.run()