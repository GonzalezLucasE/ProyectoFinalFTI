import random
import tkinter as tk

class SnakeGame:
	def __init__(self, master, width=600, height=400, cell_size=20, controller=None, use_controller=False):
		self.master = master
		self.width = width
		self.height = height
		self.cell_size = cell_size
		self.columnas = self.width // self.cell_size
		self.filas = self.height // self.cell_size

		self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
		self.canvas.pack()

		self.score_var = tk.StringVar()
		self.score_var.set("Puntos: 0")
		self.score_label = tk.Label(master, textvariable=self.score_var, font=("Consolas", 12))
		self.score_label.pack()

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
		start_x = self.columnas // 2
		start_y = self.filas // 2
		self.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
		self.direccion = (1, 0)  # moviéndose a la derecha
		self.next_direction = self.direccion
		self.place_food()
		self.score = 0
		self.speed = 120  # ms por movimiento
		self.game_over = False

	def place_food(self):
		empty_cells = [(x, y) for x in range(self.columnas) for y in range(self.filas) if (x, y) not in getattr(self, 'snake', [])]
		if not empty_cells:
			self.food = None
			return
		self.food = random.choice(empty_cells)

	def change_direction(self, new_dir):
		# Evitar invertir la dirección directamente
		dx, dy = self.direccion
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
			decision = self.controller.decide(self.snake, self.direccion, self.food, self.columnas, self.filas)
			# evitar invertir directamente
			dx, dy = self.direccion
			if decision != (-dx, -dy):
				self.next_direction = decision

		self.direccion = self.next_direction
		dx, dy = self.direccion
		head_x, head_y = self.snake[0]
		new_head = (head_x + dx, head_y + dy)

		# Colisiones con paredes
		x, y = new_head
		if x < 0 or x >= self.columnas or y < 0 or y >= self.filas:
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
		# Dibujar comida
		if self.food:
			fx, fy = self.food
			self.draw_cell(fx, fy, "red")

		# Dibujar serpiente
		for i, (x, y) in enumerate(self.snake):
			color = "#00FF00" if i > 0 else "#007700"  # cabeza más oscura
			self.draw_cell(x, y, color)

		if self.game_over:
			self.canvas.create_text(self.width // 2, self.height // 2, text="GAME OVER",
					 fill="white", font=("Consolas", 32))
			self.canvas.create_text(self.width // 2, self.height // 2 + 40, text="Presiona espacio para reiniciar",
					 fill="white", font=("Consolas", 12))

	def draw_cell(self, x, y, color):
		x1 = x * self.cell_size
		y1 = y * self.cell_size
		x2 = x1 + self.cell_size
		y2 = y1 + self.cell_size
		# Pequeño padding para que se vea mejor
		pad = 1
		self.canvas.create_rectangle(x1 + pad, y1 + pad, x2 - pad, y2 - pad, fill=color, outline="")

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