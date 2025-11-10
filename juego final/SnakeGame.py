import random
import pygame
import sys
import os
import tkinter as tk
import Pantallas

# Pillow (opcional) para cargar JPG y escalar
try:
    from PIL import Image, ImageTk
    _PIL_AVAILABLE = True
except Exception:
    _PIL_AVAILABLE = False

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 150 # Tamaño base para los segmentos del Snake
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (200, 0, 0)
DARK_GREEN = (0, 100, 0)

class SnakeGame(pygame.sprite.Sprite):
    
    def __init__(self, master, cell_size, amarok_img, caravan_imgs, controller=None, use_controller=False):
        super().__init__()
        self.master = master
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.cell_size = cell_size
        self.amarok_img = pygame.transform.scale(amarok_img, (cell_size * 2, cell_size))
        self.caravan_imgs = [pygame.transform.scale(img, (cell_size, cell_size)) for img in caravan_imgs]
        self.columns = self.width // self.cell_size
        self.rows = self.height // self.cell_size

        # Crear canvas con fondo verde claro (según estética solicitada)
        # Usamos el color LIGHT_GREEN definido arriba (#90EE90)
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="#90EE90", highlightthickness=0)
        self.canvas.pack()

        # Intentar cargar imagen de fondo (pantalla_fondo.png) desde ../proyecto juego/
        self.bg_image = None
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            proyecto_juego_dir = os.path.join(parent_dir, "proyecto juego")
            bg_path = os.path.join(proyecto_juego_dir, 'pantalla_fondo.png')
            if _PIL_AVAILABLE and os.path.exists(bg_path):
                img = Image.open(bg_path).convert('RGBA')
                img = img.resize((self.width, self.height), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                # Dibujar fondo (tag 'bg' para mantenerlo)
                self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw', tags='bg')
        except Exception:
            # Si falla la carga, seguimos con el color de fondo
            self.bg_image = None
        
        # Intentar cargar imágenes para cabeza y caravanas en formato Tk (si Pillow está disponible)
        self.tk_head_imgs = {}  # dict con orientaciones: 'up','down','left','right'
        self.tk_caravan_imgs = []
        try:
            if _PIL_AVAILABLE:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(current_dir)
                proyecto_juego_dir = os.path.join(parent_dir, "proyecto juego")
                head_path = os.path.join(proyecto_juego_dir, 'amarok.png')
                if os.path.exists(head_path):
                    h = Image.open(head_path).convert('RGBA')
                    # Redimensionar base para la cabeza (derecha) sin fondo blanco
                    base_size = (self.cell_size * 2, self.cell_size)
                    h_resized = h.resize(base_size, Image.LANCZOS)
                    self.tk_head_imgs['right'] = ImageTk.PhotoImage(h_resized)

                    # Crear otras orientaciones a partir de la base
                    up_img = h_resized.rotate(90, expand=True).resize(base_size, Image.LANCZOS)
                    left_img = h_resized.rotate(180, expand=True).resize(base_size, Image.LANCZOS)
                    down_img = h_resized.rotate(270, expand=True).resize(base_size, Image.LANCZOS)
                    self.tk_head_imgs['up'] = ImageTk.PhotoImage(up_img)
                    self.tk_head_imgs['left'] = ImageTk.PhotoImage(left_img)
                    self.tk_head_imgs['down'] = ImageTk.PhotoImage(down_img)
                for name in ('casa1.png', 'casa2.png', 'casa3.png'):
                    p = os.path.join(proyecto_juego_dir, name)
                    if os.path.exists(p):
                        im = Image.open(p).convert('RGBA')
                        # Agrandar imágenes de casa: 1.5x el tamaño de la celda
                        large_size = int(self.cell_size * 1.5)
                        im_resized = im.resize((large_size, large_size), Image.LANCZOS)
                        self.tk_caravan_imgs.append(ImageTk.PhotoImage(im_resized))
        except Exception:
            # Si falla, simplemente no tendremos imágenes Tk y usaremos rectángulos
            self.tk_head_imgs = {}
            self.tk_caravan_imgs = []

        self.score_var = tk.StringVar()
        self.score_var.set("Puntos: 0")
        # Sector blanco de puntos en la parte inferior (estilo inicial)
        self.score_label = tk.Label(master, textvariable=self.score_var, font=("Consolas", 14, "bold"), 
                    bg="white", fg="#004400",  # Verde oscuro para el texto
                    pady=10, padx=10)
        # Colocar el contador en la parte inferior, ocupando todo el ancho
        self.score_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind teclas
        master.bind("<Up>", lambda e: self.change_direction((0, -1)))
        master.bind("<Down>", lambda e: self.change_direction((0, 1)))
        master.bind("<Left>", lambda e: self.change_direction((-1, 0)))
        master.bind("<Right>", lambda e: self.change_direction((1, 0)))
        master.bind("w", lambda e: self.change_direction((0, -1)))
        master.bind("s", lambda e: self.change_direction((0, 1)))
        master.bind("a", lambda e: self.change_direction((-1, 0)))
        master.bind("d", lambda e: self.change_direction((1, 0)))
        # Usar la secuencia <space> en lugar de un espacio literal para evitar
        # el error TclError: no events specified in binding
        master.bind("<space>", lambda e: self.restart())
        # Alternar control por autómata/manual con la tecla t
        master.bind("t", lambda e: self.toggle_controller())

        self.running = False
        self.after_id = None
        # controlador (puede ser None)
        self.controller = controller
        self.use_controller = bool(use_controller) and (controller is not None)

        self.mode_label = tk.Label(master, text="Modo: teclado" if not self.use_controller else "Modo: autómata", font=("Consolas", 10))
        self.mode_label.pack()

        # Inicializar estado del juego
        # Lista de índices de caravana (uno por segmento excepto la cabeza)
        self.caravans_type = []
        self.reset()

    def reset(self):
        """Inicializa la serpiente con sólo la cabeza y velocidad inicial lenta."""
        start_x = self.columns // 2
        start_y = self.rows // 2
        self.snake = [(start_x, start_y)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.place_food()
        self.score = 0
        self.speed = 300  # ms por movimiento (lento al inicio)
        self.game_over = False

    def place_food(self):
        empty_cells = [(x, y) for x in range(self.columns) for y in range(self.rows) if (x, y) not in getattr(self, 'snake', [])]
        if not empty_cells:
            self.food = None
            self.food_type = None
            return
        self.food = random.choice(empty_cells)
        # Elegir tipo de fruta/caravana que aparecerá (índice)
        if self.tk_caravan_imgs:
            self.food_type = random.randrange(len(self.tk_caravan_imgs))
        else:
            # fallback: usar el conjunto de caravan_imgs (pygame) si existen
            self.food_type = random.randrange(len(self.caravan_imgs)) if self.caravan_imgs else 0

    def change_direction(self, new_dir):
        # Evitar invertir la dirección directamente
        dx, dy = self.direction
        ndx, ndy = new_dir
        if (ndx, ndy) == (-dx, -dy):
            return
        self.next_direction = (ndx, ndy)

    def toggle_controller(self):
        if not self.controller:
            return
        self.use_controller = not self.use_controller
        self.mode_label.config(text="Modo: autómata" if self.use_controller else "Modo: teclado")

    def step(self):
        """Un tick del juego: mover, comer, chequear colisiones y reprogramar."""
        if self.game_over:
            return

        if self.use_controller and self.controller:
            decision = self.controller.decide(self.snake, self.direction, self.food, self.columns, self.rows)
            dx, dy = self.direction
            if decision != (-dx, -dy):
                self.next_direction = decision

        self.direction = self.next_direction
        dx, dy = self.direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        # Colisiones con paredes
        x, y = new_head
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
            self.end_game()
            return

        # Colisión con sí misma
        if new_head in self.snake:
            self.end_game()
            return

        # Mover
        self.snake.insert(0, new_head)

        # Comer comida
        if self.food and new_head == self.food:
            self.score += 1
            self.score_var.set(f"Puntos: {self.score}")
            # Aumentar velocidad (reducir intervalo) hasta un tope mínimo
            if self.speed > 40:
                self.speed = max(40, int(self.speed * 0.9))
            # Registrar tipo de caravana para el nuevo segmento
            if self.tk_caravan_imgs:
                idx = random.randrange(len(self.tk_caravan_imgs))
            else:
                # fallback: si no hay Tk images, usar índice 0
                idx = 0
            self.caravans_type.append(idx)
            self.place_food()
        else:
            # No comer -> eliminar la última celda (movimiento)
            self.snake.pop()

        self.redraw()
        # Programar siguiente paso
        self.after_id = self.master.after(self.speed, self.step)

    def redraw(self):
        # Borramos solo los sprites (mantener background si existe)
        self.canvas.delete('sprites')

        # Si no hay background cargado, dibujar la franja de carretera como antes
        if not getattr(self, 'bg_image', None):
            road_start = self.height // 2 - 50
            road_end = self.height // 2 + 50
            self.canvas.create_rectangle(0, road_start, self.width, road_end, fill="#228B22", outline="", tags=('sprites',))
            # Dibujar línea divisoria de la carretera
            for y in range(road_start, road_end, 40):
                self.canvas.create_line(0, y, self.width, y, fill="yellow", dash=(4, 4), width=2, tags=('sprites',))

        # Dibujar comida (fruta) — preferir imagen Tk si está disponible
        if self.food:
            fx, fy = self.food
            px = fx * self.cell_size
            py = fy * self.cell_size
            if getattr(self, 'tk_caravan_imgs', None) and self.food_type is not None and len(self.tk_caravan_imgs) > 0:
                img = self.tk_caravan_imgs[self.food_type % len(self.tk_caravan_imgs)]
                # centrar la imagen dentro de la celda
                off_x = (self.cell_size - img.width()) // 2
                off_y = (self.cell_size - img.height()) // 2
                self.canvas.create_image(px + off_x, py + off_y, image=img, anchor='nw', tags=('sprites',))
            else:
                self.draw_cell(fx, fy, "#FF4444")  # Rojo más vibrante para fruta

        # Dibujar serpiente con imágenes si están disponibles
        for i, (x, y) in enumerate(self.snake):
            px = x * self.cell_size
            py = y * self.cell_size
            if i == 0:  # Cabeza (Amarok)
                # Elegir la orientación según la dirección actual
                dir_key = 'right'
                dx, dy = self.direction
                if dx == 1 and dy == 0:
                    dir_key = 'right'
                elif dx == -1 and dy == 0:
                    dir_key = 'left'
                elif dx == 0 and dy == -1:
                    dir_key = 'up'
                elif dx == 0 and dy == 1:
                    dir_key = 'down'

                if self.tk_head_imgs and dir_key in self.tk_head_imgs:
                    img = self.tk_head_imgs[dir_key]
                    off_x = (self.cell_size - img.width()) // 2
                    off_y = (self.cell_size - img.height()) // 2
                    # Para cabeza más ancha (2*cells) centramos respecto a la celda x
                    self.canvas.create_image(px + off_x, py + off_y, image=img, anchor='nw', tags=('sprites',))
                else:
                    self.draw_cell(x, y, "#00AA00", width=1.5)
            else:  # Cuerpo (caravanas)
                idx = self.caravans_type[i-1] if i-1 < len(self.caravans_type) else 0
                if getattr(self, 'tk_caravan_imgs', None) and len(self.tk_caravan_imgs) > 0:
                    img = self.tk_caravan_imgs[idx % len(self.tk_caravan_imgs)]
                    # Centrar imagen agrandada dentro de la celda
                    off_x = (self.cell_size - img.width()) // 2
                    off_y = (self.cell_size - img.height()) // 2
                    self.canvas.create_image(px + off_x, py + off_y, image=img, anchor='nw', tags=('sprites',))
                else:
                    self.draw_cell(x, y, "#00DD00", width=1)

        if self.game_over:
            # Dibujo mejorado de GAME OVER (encima de sprites)
            self.canvas.create_rectangle(150, 150, 650, 450, fill="black", outline="white", width=3, tags=('sprites',))
            self.canvas.create_text(self.width // 2, self.height // 2, text="GAME OVER",
                fill="red", font=("Consolas", 40, "bold"), tags=('sprites',))
            self.canvas.create_text(self.width // 2, self.height // 2 + 70, 
                text=f"Puntuación Final: {self.score}",
                fill="white", font=("Consolas", 16), tags=('sprites',))
            self.canvas.create_text(self.width // 2, self.height // 2 + 110, 
                text="Presiona ESPACIO para reiniciar",
                fill="yellow", font=("Consolas", 14), tags=('sprites',))

    def draw_cell(self, x, y, color, width=1):
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        # Pequeño padding para que se vea mejor
        pad = 1
        self.canvas.create_rectangle(x1 + pad, y1 + pad, x2 - pad, y2 - pad, fill=color, outline="white", width=width, tags=('sprites',))

    def end_game(self):
        self.game_over = True
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.redraw()

    def restart(self):
        # Reiniciar el juego
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.reset()
        self.score_var.set(f"Puntos: {self.score}")
        self.game_over = False
        self.redraw()
        self.after_id = self.master.after(self.speed, self.step)