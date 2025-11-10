import tkinter as tk
import SnakeGame
import AutomataSnake

def main():
	root = tk.Tk()
	root.title("Snake - Juego")
	# Evitar redimensionado que rompa las coordenadas
	root.resizable(False, False)
	# Crear controlador de autómata pero no habilitarlo por defecto
	controller = AutomataSnake.AutomataSnake()
	game = SnakeGame.SnakeGame(root, width=600, height=400, cell_size=20, controller=controller, use_controller=False)
	# Asegurar que la ventana/canvas tenga el foco para recibir teclas
	root.focus_set()
	game.canvas.focus_set()
	# Iniciar el loop del juego
	game.after_id = root.after(game.speed, game.step)
	root.mainloop()


if __name__ == "__main__":
	main()
