"""
Launcher que muestra pantallas pygame (inicio/carga) y luego ejecuta
la lógica original basada en Tkinter (SnakeGame). Mantiene la lógica
inicial y la estética solicitada.
"""

import os
import sys
import pygame
import tkinter as tk

from SnakeGame import SnakeGame
from Pantallas import Pantallas


def load_images_from_proyecto():
	current_dir = os.path.dirname(os.path.abspath(__file__))
	parent_dir = os.path.dirname(current_dir)
	proyecto_juego_dir = os.path.join(parent_dir, "proyecto juego")

	try:
		bg = pygame.image.load(os.path.join(proyecto_juego_dir, 'imagen_amarock.jpg')).convert()
		amarok = pygame.image.load(os.path.join(proyecto_juego_dir, 'amarok.png')).convert_alpha()
		casa1 = pygame.image.load(os.path.join(proyecto_juego_dir, 'casa1.png')).convert_alpha()
		casa2 = pygame.image.load(os.path.join(proyecto_juego_dir, 'casa2.png')).convert_alpha()
		casa3 = pygame.image.load(os.path.join(proyecto_juego_dir, 'casa3.png')).convert_alpha()
	except Exception as e:
		print(f"Error cargando imágenes desde '{proyecto_juego_dir}': {e}")
		raise

	return bg, amarok, [casa1, casa2, casa3]


def main():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('La Mandita Amarok - Pantallas')

	# Cargar imágenes para pantallas y luego para pasar al juego tkinter
	try:
		bg, amarok_img, caravan_imgs = load_images_from_proyecto()
	except Exception:
		pygame.quit()
		sys.exit(1)

	# Escalar/background
	bg = pygame.transform.scale(bg, (800, 600))
	loading_truck = pygame.transform.scale(amarok_img, (150, 75))

	# Mostrar pantalla de inicio y carga usando Pantallas
	pantallas = Pantallas(screen, bg, loading_truck)
	pantallas.main_menu()
	pantallas.loading_screen(load_time=1.5)

	# Cerrar pygame antes de crear la interfaz Tk (evita conflictos)
	pygame.quit()

	# Inicializar Tkinter y la versión original del Snake (lógica intacta)
	root = tk.Tk()
	root.title('La Mandita Amarok - Juego')
	root.resizable(False, False)

	# Tkinter SnakeGame espera imágenes en formato pygame.Surface; ya las cargamos antes
	# Reabrimos pygame brevemente para convertir/asegurar objetos (sin mostrar ventana)
	pygame.init()
	# Pasamos las imágenes tal cual; SnakeGame las transforma con pygame.transform

	game = SnakeGame(root, cell_size=40, amarok_img=amarok_img, caravan_imgs=caravan_imgs, controller=None, use_controller=False)

	# Asegurar foco y comenzar loop de Tk
	root.focus_set()
	game.canvas.focus_set()
	if not game.after_id:
		game.after_id = root.after(game.speed, game.step)
	root.mainloop()


if __name__ == '__main__':
	main()
