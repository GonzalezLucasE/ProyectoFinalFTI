import random
import tkinter

class controlador:
    
    def decidir(self, snake, direccion, casilla, columnas, filas):
        head = snake[0]
        snake_set(snake)
        
        def cell_free(pos):
            x, y = pos
            if x<0 or x>= columnas or y<0 or y>=filas:
                