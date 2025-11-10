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
        
        # Lista para almacenar el índice del tipo de imagen de cada caravana en el cuerpo
        self.caravans_type = []
        
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
        

    def grow(self, caravan_type_index):
        # Añade un nuevo segmento al final
        #self.body.append(self.body[-1])
        # Registra el tipo de imagen que debe usar el nuevo segmento
        self.caravans_type.append(caravan_type_index)

    def draw(self, screen):
        # Determinar el ángulo de rotación basado en la dirección actual
        #angle = 0
        #if self.direction == "UP":
        # angle = 90
        #elif self.direction == "DOWN":
            #angle = -90  # O 270 grados
        #elif self.direction == "LEFT":
            #angle = 180
        #rotated_amarok = pygame.transform.rotate(self.amarok_img, angle)
        # Las imágenes rotadas cambian de tamaño, por lo que es necesario recalcular el centro
        #new_rect = rotated_amarok.get_rect(center=self.amarok_img.get_rect(topleft=self.body[0]).center)
        # 3. Dibujar la Amarok rotada
        #screen.blit(rotated_amarok, new_rect.topleft)
        # Dibujar la Amarok (cabeza)
        screen.blit(self.amarok_img, self.body[0])

        # Dibujar las caravanas (cuerpo)
        for i, segment in enumerate(self.body[1:]): 
            # Usa el tipo de caravana registrado en self.caravans_type
            # i es el índice del segmento de caravana, que corresponde a caravans_type
            caravan_index = self.caravans_type[i] 
            caravan_to_draw = self.caravan_imgs[caravan_index]
            screen.blit(caravan_to_draw, segment)

    def check_collision(self):
        head = self.body[0]
        # Colisión con los límites de la pantalla
        if not (0 <= head[0] < SCREEN_WIDTH and 0 <= head[1] < SCREEN_HEIGHT):
            return True # Game Over (colisión con borde)
        
        # Colisión con el cuerpo (la Amarok se choca con una caravana)
        if head in self.body[2:]:
            return True # Game Over (colisión con el cuerpo)
            
        return False
    
    @property
    def head_rect(self):
        return pygame.Rect(self.body[0][0], self.body[0][1], self.amarok_img.get_width(), self.amarok_img.get_height())


# ----------------------------------------------------------------------
## Clase Screens: Maneja las pantallas de inicio y carga
# ----------------------------------------------------------------------

class Screens:
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

# ----------------------------------------------------------------------
## Clase Game: Controla el flujo del juego
# ----------------------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("la mandita amarok")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.font_score = pygame.font.Font(None, 36)
        # Inicialización de variables de imagen/estado a None/0 antes de la carga
        self.snake = None
        self.caravan_types_available = 0
        self.current_fruit_index = 0
        self.fruit_pos = (0, 0)
        self.amarok_game_img = None 
        self.loading_truck_img = None
        self.main_screen_bg = None # Usamos este nombre para la pantalla principal
        self.caravan_imgs = []
        self.fruit_img = None
        
        self.load_assets()
        # CORRECCIÓN: Usar self.main_screen_bg para ser coherente con la carga
        self.screens = Screens(self.screen, self.main_screen_bg, self.loading_truck_img) 

    def load_assets(self):
        # --- Carga de imágenes ---
        try:
            # CORRECCIÓN DE NOMBRES DE VARIABLE: Usar self.main_screen_bg
            self.main_screen_bg = pygame.image.load('imagen_amarock.jpg').convert() 
            self.main_screen_bg = pygame.transform.scale(self.main_screen_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Imagen para la pantalla de carga (usaremos la Amarok)
            self.loading_truck_img = pygame.image.load('amarok.png').convert_alpha() 
            self.loading_truck_img = pygame.transform.scale(self.loading_truck_img, (150, 75))
            
            # Assets del juego (Amarok y Caravanas)
            self.amarok_game_img = pygame.image.load('amarok.png').convert_alpha()
            
            # LISTA CASA RODANTES
            self.caravan_imgs = [
                pygame.image.load('casa1.png').convert_alpha(),
                pygame.image.load('casa2.png').convert_alpha(),
                pygame.image.load('casa3.png').convert_alpha(),
            ]
            
        except pygame.error as e:
            print(f"Error CRÍTICO al cargar el archivo de imagen: {e}")
            print("Verifica que el nombre del archivo y la extensión (por ejemplo, 'casa1.png') son correctos.")
            pygame.quit()
            sys.exit()

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

    def update(self):
        self.snake.move()
        
        # 1. Colisión con la Fruta (Comer la Caravana)
        fruit_rect = pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], CELL_SIZE, CELL_SIZE)
        if self.snake.head_rect.colliderect(fruit_rect):
            # ¡La camioneta come la caravana! La añade al cuerpo con su índice de tipo.
            self.snake.grow(self.current_fruit_index)
            self.fruit_pos = self.generate_fruit_pos() 
            self.score += 10
            # Generar nueva "fruta" (caravana)
            self.caravan_types_available = len(self.caravan_imgs)
            self.current_fruit_index = random.randrange(self.caravan_types_available)
            self.fruit_img = self.caravan_imgs[self.current_fruit_index] # Actualiza la imagen de la fruta
            self.fruit_img = pygame.transform.scale(self.fruit_img, (CELL_SIZE, CELL_SIZE)) # Re-escala la nueva imagen
            self.fruit_pos = self.generate_fruit_pos()
        else:
            # ¡IMPORTANTE!: Si NO come, la cola se elimina para simular el movimiento
            self.snake.body.pop()
            
        
        # 2. Colisión con Pared o Cuerpo (Game Over)
        if self.snake.check_collision():
            print(f"¡Game Over! Puntuación final: {self.score}")
            self.running = False

    def draw(self):
        # Dibujar el fondo
        self.screen.fill(GREEN)
        # Usar BLACK para la carretera, GREEN hace que se pierda
        pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH, 100)) # Camino
        
        # Dibujar la fruta
        self.screen.blit(self.fruit_img, self.fruit_pos)
        
        # CORRECCIÓN CLAVE: El dibujo del Snake (Amarok y Caravanas)
        # Lo hace todo el método self.snake.draw(self.screen)
        self.snake.draw(self.screen)
        
        # Dibujar la puntuación
        score_text = self.font_score.render(f"Puntuación: {self.score}", True, BLACK)
        self.screen.blit(score_text, (30, 30))
        
        pygame.display.flip()

    def run(self):
        # 1. Mostrar pantallas de inicio y carga
        self.screens.main_menu()
        self.screens.loading_screen()
        
        # 2. INICIALIZACIÓN POST-CARGA (SECUENCIA CLAVE)
        # PASO A: ¡Crear el objeto Snake primero!
        self.snake = Snake(CELL_SIZE, self.amarok_game_img, self.caravan_imgs)
        
        # PASO B: Inicializar la lógica de la "fruta" que depende de Snake
        self.caravan_types_available = len(self.caravan_imgs)
        self.current_fruit_index = random.randrange(self.caravan_types_available)
        
        # Actualizar la imagen y la posición de la fruta
        self.fruit_img = self.caravan_imgs[self.current_fruit_index] 
        self.fruit_img = pygame.transform.scale(self.fruit_img, (CELL_SIZE, CELL_SIZE)) 
        
        # PASO C: ¡Ahora podemos llamar a generate_fruit_pos() de forma segura!
        #self.fruit_pos = self.generate_fruit_pos()
        
        # 3. Bucle principal del juego
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(5) 

        pygame.quit()
        sys.exit()

# ----------------------------------------------------------------------
## Ejecución del Juego
# ----------------------------------------------------------------------

if __name__ == '__main__':
    game = Game()
    game.run()