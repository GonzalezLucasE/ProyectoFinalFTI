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
		loadbg = pygame.image.load(os.path.join(proyecto_juego_dir, 'fondo_carga.png')).convert()
		amarok = pygame.image.load(os.path.join(proyecto_juego_dir, 'amarok.png')).convert_alpha()
		casa1 = pygame.image.load(os.path.join(proyecto_juego_dir, 'casa1.png')).convert_alpha()
		casa2 = pygame.image.load(os.path.join(proyecto_juego_dir, 'casa2.png')).convert_alpha()
		casa3 = pygame.image.load(os.path.join(proyecto_juego_dir, 'casa3.png')).convert_alpha()
	except Exception as e:
		print(f"Error cargando imágenes desde '{proyecto_juego_dir}': {e}")
		raise

	return bg, loadbg, amarok, [casa1, casa2, casa3]


def main():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('Snake Amarok')

	try:
		bg, loadbg, amarok_img, caravan_imgs = load_images_from_proyecto()
	except Exception:
		pygame.quit()
		sys.exit(1)

	bg = pygame.transform.scale(bg, (800, 600))
	loadbg = pygame.transform.scale(loadbg, (800, 800))
	loading_truck = pygame.transform.scale(amarok_img, (300, 250))

	pantallas = Pantallas(screen, bg, loadbg, loading_truck)
	pantallas.main_menu()
	pantallas.loading_screen(load_time=1.5)

	pygame.quit()

	root = tk.Tk()
	root.title('Snake Amarok - Juego')
	root.resizable(False, False)

	pygame.init()

	game = SnakeGame(root, cell_size=80, amarok_img=amarok_img, caravan_imgs=caravan_imgs, controller=None, use_controller=False)

	root.focus_set()
	game.canvas.focus_set()
	if not game.after_id:
		game.after_id = root.after(game.speed, game.step)
	root.mainloop()


if __name__ == '__main__':
	main()
