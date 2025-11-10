class AutomataSnake:

	def decidir(self, snake, direccion, casilla, columnas, filas):
		cabeza = snake[0]
		snake_set = set(snake)

		def celda_libre(pos):
			x, y = pos
			if x < 0 or x >= columnas or y < 0 or y >= filas:
				return False
			return pos not in snake_set

		# helpers de dirección
		dx, dy = direccion
		right = (-dy, dx)
		left = (dy, -dx)

		# Intentar mover hacia la comida si está en línea
		if casilla is not None:
			fx, fy = casilla
			hx, hy = cabeza
			if fx == hx:
				piso = (0, 1) if fy > hy else (0, -1)
				# evitar invertir
				if piso != (-dx, -dy) and celda_libre((hx + piso[0], hy + piso[1])):
					return piso
			if fy == hy:
				piso = (1, 0) if fx > hx else (-1, 0)
				if piso != (-dx, -dy) and celda_libre((hx + piso[0], hy + piso[1])):
					return piso

		# Wall-following local: adelante, derecha, izquierda
		adelante = (dx, dy)
		for cand in (adelante, right, left):
			nx, ny = cabeza[0] + cand[0], cabeza[1] + cand[1]
			if celda_libre((nx, ny)):
				# evitar invertir
				if cand == (-dx, -dy):
					continue
				return cand

		# Si no hay otra opción (muy raro), intentar cualquier celda libre en orden fijo
		for cand in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
			nx, ny = cabeza[0] + cand[0], cabeza[1] + cand[1]
			if celda_libre((nx, ny)) and cand != (-dx, -dy):
				return cand

		# No hay movimiento seguro -> devolver la dirección actual (caerá en colisión luego)
		return direccion