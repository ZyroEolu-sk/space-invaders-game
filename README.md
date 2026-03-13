# Space Invaders (pygame)

Un clon modernizado del clásico *Space Invaders* desarrollado en Python utilizando la librería **Pygame**. ¡Defiende la galaxia de múltiples oleadas alienígenas, recoge power-ups y enfréntate al temible jefe final!

## Características

* **4 Niveles de Dificultad:** Progresión de niveles con mecánicas que se vuelven más desafiantes.
* **Diversidad de Enemigos:** * *Aliens básicos* y *Healers* (que sueltan vidas extra).
  * *Tech Aliens* que se teletransportan por el mapa.
  * **Batalla de Jefe (Braincell):** Un enemigo final con múltiples formas, barras de vida y más de 5 patrones de ataque diferentes.
* **Sistema de High Score:** Tu puntuación máxima se guarda automáticamente de forma persistente.

---

## Vista general

Juego inspirado en el clásico *Space Invaders*:

- Pantalla de inicio con animación de “press to start”.
- Oleadas / niveles con enemigos diferentes.
- Sistema de disparos y colisiones.
- Power-ups de vida.
- Efectos/animaciones (explosiones, teleports).
- Guardado del **récord** (high score) en `score.json`.

La entrada principal es: **`src/main.py`**.

---

## Requisitos

- **Python 3.11+** (según `pyproject.toml`)
- **pygame 2.6.1+**
- **uv** (opcional, recomendado para gestionar entorno y dependencias)
- Windows / macOS / Linux

---

## Instalación (paso a paso)

### 1) Clonar el repositorio

```bash
git clone https://github.com/ZyroEolu-sk/space-invaders-game.git
cd space-invaders-game
```

### 2) (Recomendado) Crear entorno virtual

#### Opción A: `venv` (estándar de Python)

**Windows (PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Opción B: `uv` (rápido y reproducible)

Si no tienes `uv`, instálalo desde la documentación oficial:

- https://docs.astral.sh/uv/

Luego, desde la raíz del proyecto:

```bash
uv venv
uv sync
```

Esto crea el entorno en `.venv` y sincroniza dependencias según `pyproject.toml` y `uv.lock`.

### 3) Instalar dependencias

```bash
pip install -U pip
pip install pygame
```

Con `uv`, este paso queda cubierto con:

```bash
uv sync
```

---

## Ejecutar el juego

### Ejecutar (desde la raíz del repo)

**macOS/Linux:**
```bash
python3 src/main.py
```

**Windows:**
```bash
python src/main.py
```

Con `uv` (sin activar entorno manualmente):

```bash
uv run src/main.py
```

Si por alguna razón tu Python no resuelve imports como `settings`, ejecútalo desde `src/`:

```bash
cd src
python main.py
```

---

## Controles

- **Moverse:** Flecha **Izquierda (←)** / **Derecha (→)**
- **Disparar:** **Espacio (SPACE)**
- **Pausar/Reanudar:** **ESC**
- En menús (pausa / game over): puedes usar el **mouse** para pulsar botones (`Resume`, `Quit`, `Retry`).

---

## Estructura del proyecto

```text
.
├─ assets/
│  ├─ animations/     # animaciones (explosiones, teleport, etc.)
│  ├─ audio/          # sonidos / música
│  ├─ backgrounds/    # fondos
│  ├─ sprites/        # sprites principales (nave, enemigos, estrellas...)
│  └─ ui/             # imágenes de UI (score, lives, game over, etc.)
├─ src/
│  ├─ main.py         # juego principal (loop, estados, lógica principal)
│  ├─ settings.py     # constantes, tamaños, colores, rutas, etc.
│  ├─ entities.py     # entidades: aliens, enemigos especiales / boss
│  ├─ effects.py      # balas, explosiones, powerups, animaciones
│  └─ ui.py           # botones y UI basada en pygame
├─ score.json         # récord / score guardado
├─ pyproject.toml     # python>=3.11, pygame>=2.6.1
└─ README.md
```

---

## Detalles técnicos 

### `src/settings.py`
Constantes de:
- Tamaño de ventana, FPS
- Colores
- Parámetros del jugador (velocidad, vidas)
- Parámetros de juego (velocidad de balas, estrellas, etc.)
- Rutas dinámicas (por ejemplo `ASSETS_PATH`) para cargar recursos desde `assets/`

### `src/main.py`
Clase principal del juego con:
- Inicialización de pygame y ventana
- Carga de recursos desde `assets/`
- Loop principal y estados: inicio → jugando → pausa → game over
- Manejo de input:
  - Flechas para mover
  - SPACE para disparar
  - ESC para pausar

### `src/entities.py`
Enemigos y entidades (aliens y variantes), con movimiento y disparo.

### `src/effects.py`
Efectos y objetos auxiliares:
- Balas (`Bullet`)
- Explosiones (`Explosion`)
- Power-up de vida (`Power`)
- Animaciones de teleport

### `src/ui.py`
Botones simples hechos con pygame para pausa / game over.

---

## Solución de problemas (Troubleshooting)

### “No module named 'pygame'”
```bash
pip install pygame
```

Si usas `uv`:

```bash
uv sync
```

### Error cargando imágenes / `FileNotFoundError`
- Ejecuta el juego desde la **raíz** del repo (recomendado).
- Verifica que exista la carpeta `assets/` con sus subcarpetas (`sprites`, `ui`, etc.).

---

## Git y entorno (recomendado)

- **Sí** conviene versionar `pyproject.toml` y `uv.lock`.
- `.venv/` **no** debe subirse al repositorio (ya está ignorado en `.gitignore`).
- `.python-version` es opcional: súbelo si quieres fijar de forma explícita Python 3.11 para colaboradores que usen `pyenv`/`uv`.

---

## Créditos

Hecho por:

- [ZyroEolu-sk](https://github.com/ZyroEolu-sk)
- [pvinas23](https://github.com/pvinas23)

Proyecto de nuestros primeros pasos dentro de la programación creando un juego con Python y Pygame. Lo hemos ordenado respecto al código original. 
