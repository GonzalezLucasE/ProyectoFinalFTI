import random
import pygame
import sys
import tkinter as tk
import Pantallas

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40 # Tamaño base para los segmentos del Snake
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

        self.reset()

    def reset(self):
    # Serpiente: lista de (x, y) en coordenadas de celda
        start_x = self.columns // 2
        start_y = self.rows // 2
        self.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = (1, 0)  # moviéndose a la derecha
        self.next_direction = self.direction
        self.place_food()
        self.score = 0
        self.speed = 120  # ms por movimiento
        self.game_over = False

    def place_food(self):
        empty_cells = [(x, y) for x in range(self.columns) for y in range(self.rows) if (x, y) not in getattr(self, 'snake', [])]
        if not empty_cells:
            self.food = None
            return
        self.food = random.choice(empty_cells)

    def change_direction(self, new_dir):
        # Evitar invertir la dirección directamente
        dx, dy = self.direction
        ndx, ndy = new_dir
        if (ndx, ndy) == (-dx, -dy):
            return
        # Guardar como next para aplicar en el siguiente tick
        self.next_direction = (ndx, ndy)

    def toggle_controller(self):
        # Solo tiene efecto si hay un controller
        if not self.controller:
            return
        self.use_controller = not self.use_controller
        self.mode_label.config(text="Modo: autómata" if self.use_controller else "Modo: teclado")

    def step(self):
        if self.game_over:
            return

        # Si está habilitado el controlador, pedir su decisión
        if self.use_controller and self.controller:
            decision = self.controller.decide(self.snake, self.direction, self.food, self.columns, self.rows)
            # evitar invertir directamente
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
            # Aumentar velocidad con límite
            if self.speed > 40:
                self.speed = max(40, int(self.speed * 0.95))
            self.place_food()
        else:
            self.snake.pop()

        self.redraw()
        # Programar siguiente paso
        self.after_id = self.master.after(self.speed, self.step)

    def redraw(self):
        self.canvas.delete("all")
        
        # Dibujar fondo con patrón de carretera
        road_start = self.height // 2 - 50
        road_end = self.height // 2 + 50
        self.canvas.create_rectangle(0, road_start, self.width, road_end, fill="#228B22", outline="")
        
        # Dibujar línea divisoria de la carretera
        for y in range(road_start, road_end, 40):
            self.canvas.create_line(0, y, self.width, y, fill="yellow", dash=(4, 4), width=2)
        
        # Dibujar comida (fruta)
        if self.food:
            fx, fy = self.food
            self.draw_cell(fx, fy, "#FF4444")  # Rojo más vibrante para fruta

        # Dibujar serpiente con mejor estética
        for i, (x, y) in enumerate(self.snake):
            if i == 0:  # Cabeza (Amarok)
                color = "#00AA00"  # Verde brillante para cabeza
                width = 1.5
            else:  # Cuerpo (caravanas)
                color = "#00DD00"  # Verde más claro para caravanas
                width = 1
            self.draw_cell(x, y, color, width)

        if self.game_over:
            # Dibujo mejorado de GAME OVER
            self.canvas.create_rectangle(150, 150, 650, 450, fill="black", outline="white", width=3)
            self.canvas.create_text(self.width // 2, self.height // 2, text="GAME OVER",
                fill="red", font=("Consolas", 40, "bold"))
            self.canvas.create_text(self.width // 2, self.height // 2 + 70, 
                text=f"Puntuación Final: {self.score}",
                fill="white", font=("Consolas", 16))
            self.canvas.create_text(self.width // 2, self.height // 2 + 110, 
                text="Presiona ESPACIO para reiniciar",
                fill="yellow", font=("Consolas", 14))

    def draw_cell(self, x, y, color, width=1):
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        # Pequeño padding para que se vea mejor
        pad = 1
        self.canvas.create_rectangle(x1 + pad, y1 + pad, x2 - pad, y2 - pad, fill=color, outline="white", width=width)

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