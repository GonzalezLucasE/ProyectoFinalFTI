import random
import pygame
import sys
import os
import tkinter as tk
import Pantallas

try:
    from PIL import Image, ImageTk
    _PIL_AVAILABLE = True
except Exception:
    _PIL_AVAILABLE = False

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 150
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (200, 0, 0)
DARK_GREEN = (0, 100, 0)


class MooreMachine:
    
    def __init__(self, initial_state, transitions, outputs):
        self.state = initial_state
        self.transitions = transitions
        self.outputs = outputs

    def input(self, symbol):
        state_trans = self.transitions.get(self.state, {})
        self.state = state_trans.get(symbol, self.state)
        out = self.outputs.get(self.state)
        if callable(out):
            out()

class SnakeGame(pygame.sprite.Sprite):
    
    def __init__(self, master, cell_size, amarok_img, caravan_imgs, controller=None, use_controller=False):
        super().__init__()
        self.master = master
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.cell_size = cell_size
        self.columns = self.width // self.cell_size
        self.rows = self.height // self.cell_size

        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="#90EE90", highlightthickness=0)
        self.canvas.pack()

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
                self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw', tags='bg')
        except Exception:
            self.bg_image = None
        
        self.tk_head_imgs = {}
        self.tk_caravan_imgs = {}
        try:
            if _PIL_AVAILABLE:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(current_dir)
                proyecto_juego_dir = os.path.join(parent_dir, "proyecto juego")
                head_path = os.path.join(proyecto_juego_dir, 'amarok.png')
                if os.path.exists(head_path):
                    h = Image.open(head_path).convert('RGBA')
                    base_size = (self.cell_size, self.cell_size)
                    h_resized = h.resize(base_size, Image.LANCZOS)
                    self.tk_head_imgs['right'] = ImageTk.PhotoImage(h_resized)

                    up_img = h_resized.rotate(90, expand=True).resize(base_size, Image.LANCZOS)
                    left_img = h_resized.transpose(Image.FLIP_LEFT_RIGHT).resize(base_size, Image.LANCZOS)
                    down_img = h_resized.rotate(270, expand=True).resize(base_size, Image.LANCZOS)
                    self.tk_head_imgs['up'] = ImageTk.PhotoImage(up_img)
                    self.tk_head_imgs['left'] = ImageTk.PhotoImage(left_img)
                    self.tk_head_imgs['down'] = ImageTk.PhotoImage(down_img)
                for name in ('casa1.png', 'casa2.png', 'casa3.png'):
                    p = os.path.join(proyecto_juego_dir, name)
                    if os.path.exists(p):
                        im = Image.open(p).convert('RGBA')
                        large_size = int(self.cell_size * 1.5)
                        im_resized = im.resize((large_size, large_size), Image.LANCZOS)
                        
                        caravan_dict = {}
                        caravan_dict['right'] = ImageTk.PhotoImage(im_resized)
                        
                        up_img = im_resized.rotate(90, expand=False).resize((large_size, large_size), Image.LANCZOS)
                        down_img = im_resized.rotate(270, expand=False).resize((large_size, large_size), Image.LANCZOS)
                        left_img = im_resized.transpose(Image.FLIP_LEFT_RIGHT).resize((large_size, large_size), Image.LANCZOS)
                        
                        caravan_dict['up'] = ImageTk.PhotoImage(up_img)
                        caravan_dict['down'] = ImageTk.PhotoImage(down_img)
                        caravan_dict['left'] = ImageTk.PhotoImage(left_img)
                        
                        self.tk_caravan_imgs[name.replace('.png', '')] = caravan_dict
        except Exception:
            self.tk_head_imgs = {}
            self.tk_caravan_imgs = {}

        self.score_var = tk.StringVar()
        self.score_var.set("Puntos: 0")
        self.score_label = tk.Label(master, textvariable=self.score_var, font=("Consolas", 14, "bold"), 
                    bg="white", fg="#004400",
                    pady=10, padx=10)
        self.score_label.pack(side=tk.BOTTOM, fill=tk.X)

        transitions = {
            'IDLE': {'UP': 'UP', 'DOWN': 'DOWN', 'LEFT': 'LEFT', 'RIGHT': 'RIGHT', 'RESTART': 'IDLE', 'TOGGLE': 'IDLE'},
            'UP':   {'UP': 'UP',   'DOWN': 'UP',   'LEFT': 'LEFT',  'RIGHT': 'RIGHT', 'RESTART': 'UP', 'TOGGLE': 'UP'},
            'DOWN': {'UP': 'DOWN', 'DOWN': 'DOWN', 'LEFT': 'LEFT',  'RIGHT': 'RIGHT', 'RESTART': 'DOWN', 'TOGGLE': 'DOWN'},
            'LEFT': {'UP': 'UP',   'DOWN': 'DOWN', 'LEFT': 'LEFT',  'RIGHT': 'LEFT',  'RESTART': 'LEFT', 'TOGGLE': 'LEFT'},
            'RIGHT':{'UP': 'UP',   'DOWN': 'DOWN', 'LEFT': 'RIGHT', 'RIGHT': 'RIGHT', 'RESTART': 'RIGHT','TOGGLE': 'RIGHT'},
        }
        outputs = {
            'UP': lambda: self.change_direction((0, -1)),
            'DOWN': lambda: self.change_direction((0, 1)),
            'LEFT': lambda: self.change_direction((-1, 0)),
            'RIGHT': lambda: self.change_direction((1, 0)),
            'IDLE': lambda: None,
        }
        try:
            self.moore = MooreMachine('IDLE', transitions, outputs)
        except NameError:
            self.moore = None

        master.bind_all("<Key>", self._on_key)

        self.running = False
        self.after_id = None
        self.controller = controller
        self.use_controller = bool(use_controller) and (controller is not None)

        self.mode_label = tk.Label(master, text="Modo: teclado" if not self.use_controller else "Modo: autómata", font=("Consolas", 10))
        self.mode_label.pack()

        self.caravans_type = []
        self.caravans_direction = []
        self.reset()

    def reset(self):
        start_x = self.columns // 2
        start_y = self.rows // 2
        self.snake = [(start_x, start_y)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.place_food()
        self.score = 0
        self.speed = 300
        self.game_over = False
        self.caravans_direction = []

    def place_food(self):
        empty_cells = [(x, y) for x in range(self.columns) for y in range(self.rows) if (x, y) not in getattr(self, 'snake', [])]
        if not empty_cells:
            self.food = None
            self.food_type = None
            return
        self.food = random.choice(empty_cells)
        if self.tk_caravan_imgs:
            self.food_type = random.choice(list(self.tk_caravan_imgs.keys()))
        else:
            self.food_type = 'casa1'


    def change_direction(self, new_dir):
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

        x, y = new_head
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
            self.end_game()
            return

        if new_head in self.snake:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if self.food and new_head == self.food:
            self.score += 1
            self.score_var.set(f"Puntos: {self.score}")
            if self.speed > 40:
                self.speed = max(40, int(self.speed * 0.95))
            self.caravans_type.append(self.food_type)
            self.caravans_direction.append(self.direction)
            self.place_food()
        else:
            self.snake.pop()
            if self.caravans_direction:
                self.caravans_direction.pop(0)

        self.redraw()
        self.after_id = self.master.after(self.speed, self.step)

    def redraw(self):
        self.canvas.delete('sprites')

        if not getattr(self, 'bg_image', None):
            road_start = self.height // 2 - 50
            road_end = self.height // 2 + 50
            self.canvas.create_rectangle(0, road_start, self.width, road_end, fill="#228B22", outline="", tags=('sprites',))
            for y in range(road_start, road_end, 40):
                self.canvas.create_line(0, y, self.width, y, fill="yellow", dash=(4, 4), width=2, tags=('sprites',))

        if self.food:
            fx, fy = self.food
            px = fx * self.cell_size
            py = fy * self.cell_size
            if getattr(self, 'tk_caravan_imgs', None) and self.food_type is not None and len(self.tk_caravan_imgs) > 0:
                key = self.food_type if self.food_type in self.tk_caravan_imgs else list(self.tk_caravan_imgs.keys())[0]
                caravan_dict = self.tk_caravan_imgs.get(key, {})
                img = caravan_dict.get('right') if 'right' in caravan_dict else next(iter(caravan_dict.values()))
                if img:
                    off_x = (self.cell_size - img.width()) // 2
                    off_y = (self.cell_size - img.height()) // 2
                    self.canvas.create_image(px + off_x, py + off_y, image=img, anchor='nw', tags=('sprites',))
            else:
                self.draw_cell(fx, fy, "#FF4444")

        for i, (x, y) in enumerate(self.snake):
            px = x * self.cell_size
            py = y * self.cell_size
            if i == 0:
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
                    self.canvas.create_image(px + off_x, py + off_y, image=img, anchor='nw', tags=('sprites',))
                else:
                    self.draw_cell(x, y, "#00AA00", width=1.5)
            else:
                idx = self.caravans_type[i-1] if i-1 < len(self.caravans_type) else None
                if getattr(self, 'tk_caravan_imgs', None) and len(self.tk_caravan_imgs) > 0 and idx is not None:
                    # idx may be a key (string) stored previously. Resolve to a caravan dict.
                    if isinstance(idx, str) and idx in self.tk_caravan_imgs:
                        caravan_dict = self.tk_caravan_imgs[idx]
                    else:
                        # fallback: pick first caravan dict
                        caravan_dict = next(iter(self.tk_caravan_imgs.values()))

                    # determine orientation from stored caravan directions when available
                    dir_key = 'right'
                    if i-1 < len(self.caravans_direction):
                        d = self.caravans_direction[i-1]
                        if d == (1, 0):
                            dir_key = 'right'
                        elif d == (-1, 0):
                            dir_key = 'left'
                        elif d == (0, -1):
                            dir_key = 'up'
                        elif d == (0, 1):
                            dir_key = 'down'

                    img = caravan_dict.get(dir_key) if dir_key in caravan_dict else next(iter(caravan_dict.values()))
                    if img:
                        off_x = (self.cell_size - img.width()) // 2
                        off_y = (self.cell_size - img.height()) // 2
                        self.canvas.create_image(px + off_x, py + off_y, image=img, anchor='nw', tags=('sprites',))
                else:
                    self.draw_cell(x, y, "#00DD00", width=1)

        if self.game_over:
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
        pad = 1
        self.canvas.create_rectangle(x1 + pad, y1 + pad, x2 - pad, y2 - pad, fill=color, outline="white", width=width, tags=('sprites',))

    def end_game(self):
        self.game_over = True
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.redraw()

    def restart(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.reset()
        self.score_var.set(f"Puntos: {self.score}")
        self.game_over = False
        self.redraw()
        self.after_id = self.master.after(self.speed, self.step)

    def _on_key(self, event):
        key = (event.keysym or '').lower()
        
        if self.game_over:
            if key == 'space':
                self.restart()
                return
            elif key == 'escape':
                self.master.quit()
                return
        
        key_to_symbol = {
            'up': 'UP', 'w': 'UP',
            'down': 'DOWN', 's': 'DOWN',
            'left': 'LEFT', 'a': 'LEFT',
            'right': 'RIGHT', 'd': 'RIGHT',
            'space': 'RESTART',
            't': 'TOGGLE',
        }
        symbol = key_to_symbol.get(key)
        if not symbol:
            return

        if hasattr(self, 'moore') and self.moore is not None:
            self.moore.input(symbol)
        else:
            fallback = {
                'UP': lambda: self.change_direction((0, -1)),
                'DOWN': lambda: self.change_direction((0, 1)),
                'LEFT': lambda: self.change_direction((-1, 0)),
                'RIGHT': lambda: self.change_direction((1, 0)),
                'RESTART': lambda: self.restart(),
                'TOGGLE': lambda: self.toggle_controller(),
            }
            action = fallback.get(symbol)
            if action:
                action()