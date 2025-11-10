# ✅ La Mandita Amarok - Juego Snake Mejorado

## 🎮 Estado Actual

✅ **COMPLETADO Y FUNCIONANDO**

- Estética de `proyecto juego` aplicada a `juego final`
- Lógica original de `juego final` intacta
- Sector blanco de puntos totales conservado
- Pantalla de game over mejorada
- Imágenes cargadas correctamente desde `proyecto juego`

---

## 🚀 Cómo Ejecutar

### Desde PowerShell

```powershell
cd "c:\Users\feder\OneDrive\Documents\GitHub\ProyectoFinalFTI\juego final"
python main.py
```

### Resultado Esperado

```
pygame-ce 2.5.6 (SDL 2.32.10, Python 3.14.0)
Buscando imágenes en: C:\Users\feder\...\proyecto juego
✓ Imágenes cargadas correctamente
```

Luego se abrirá una ventana con:
- Canvas temático verde oscuro con línea punteada amarilla (carretera)
- Sector blanco de puntos en la parte inferior
- Controles WASD o flechas para mover

---

## 🎨 Cambios Visuales

| Elemento | Antes | Ahora |
|----------|-------|-------|
| **Canvas** | Negro | Verde oscuro (#1a5c1a) |
| **Cabeza** | Verde oscuro | Verde brillante (#00AA00) |
| **Cuerpo** | Verde claro | Verde claro mejorado (#00DD00) |
| **Fruta** | Rojo básico | Rojo vibrante (#FF4444) |
| **Carretera** | No tenía | Línea punteada amarilla |
| **Puntos** | Label oscuro | **Sector blanco con borde** |
| **Game Over** | Texto simple | Marco negro + puntuación final |

---

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| **↑ / W** | Mover arriba |
| **↓ / S** | Mover abajo |
| **← / A** | Mover izquierda |
| **→ / D** | Mover derecha |
| **ESPACIO** | Reiniciar (en Game Over) |
| **T** | Alternar modo manual/automata |

---

## 📁 Archivos Modificados

### ✏️ `main.py`
- ✅ Carga automática de imágenes desde `proyecto juego/`
- ✅ Rutas absolutas correctas con `os.path`
- ✅ Manejo de errores mejorado
- ✅ Inicialización correcta de pygame para `convert_alpha()`

### ✏️ `SnakeGame.py`
- ✅ Canvas verde oscuro temático (#1a5c1a)
- ✅ Carretera con línea punteada amarilla
- ✅ Colores mejorados para snake, fruta y fondo
- ✅ Sector de puntos **blanco con estilo mejorado**
- ✅ Pantalla de Game Over mejorada con marco y puntuación

### 📄 `Pantallas.py`
- Sin cambios (compatible)

### 📄 `AutomataSnake.py`
- Sin cambios (compatible)

---

## ✨ Características Conservadas de `juego final`

✅ Lógica de serpiente
✅ Detección de colisiones  
✅ Sistema de puntuación
✅ Aumento progresivo de velocidad
✅ Modo automata/manual (tecla T)
✅ Reinicio desde Game Over
✅ **Sector blanco de puntos totales**
✅ **Pantalla de Game Over interactiva**

---

## 🔧 Configuración

Si deseas personalizar el juego, edita estos valores en `SnakeGame.py`:

```python
# Constantes
SCREEN_WIDTH = 800      # Ancho de pantalla
SCREEN_HEIGHT = 600     # Alto de pantalla
CELL_SIZE = 40          # Tamaño de cada celda

# En reset():
self.speed = 120        # ms por movimiento (menor = más rápido)
```

---

## 📦 Dependencias

```
tkinter (incluido con Python)
pygame-ce 2.5.6+
Pillow (no necesario con la versión actual)
```

---

## 🎯 Resumen Final

| Requisito | Estado |
|-----------|--------|
| Estética proyecto juego | ✅ Aplicada |
| Lógica juego final | ✅ Intacta |
| Puntos en blanco | ✅ Conservado |
| Game Over visual | ✅ Mejorado |
| Carga de imágenes | ✅ Funcionando |
| Controles | ✅ Operacionales |
| Modo automata | ✅ Disponible |

---

**Versión**: 2.0 Final
**Última actualización**: 10 de Noviembre de 2025
**Estado**: ✅ LISTO PARA USAR
