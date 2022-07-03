#! \bin\usr\env python3
"""Uma implementação em python do Jogo da Vida de Conway que roda no terminal"""

import random
import time
import curses

# ============================ Cell =====================================
DEAD = 0
LIVE = 1
m_state = {
        DEAD: ".",
        LIVE: "#"
}

# ============================= Grid ====================================
class Grid:
    def __init__(self, *args, **kwargs):
        """Retorna uma nova grade à partir de uma string ou das dimensões da mesma"""
        if len(args) == 1 and type(args[0]) == str:
            self._cells = [[int(v) for v in row] for row in args[0].split("\n")]
        elif len(args) == 2 and type(args[0]) == type(args[1]) == int:
            w, h = args
            if "random_fill" in kwargs and kwargs["random_fill"]:
                self._cells = [[random.choice([DEAD, LIVE]) for _ in range(w)] for __ in range(h)]
            else:
                self._cells = [[DEAD for _ in range(w)] for __ in range(h)]
        else:
            raise Exception("Argumentos inválidos.")
    
    def __str__(self):
        """Retorna a representação em forma de string da grade"""
        return "\n".join(["".join([m_state[v] for v in row]) for row in self._cells])

    def __getitem__(self, key):
        """Retorna o estado da célula na linha row e coluna col"""
        row, col = key
        return self._cells[row][col]

    def __setitem__(self, key, newstate):
        """Seta o estado da célula na linha row e coluna col"""
        row, col = key
        self._cells[row][col] = newstate

    @property
    def width(self):
        """retorna a largura da grade"""
        return len(self._cells[0])
    
    @property
    def height(self):
        """retorna a altura da grade"""
        return len(self._cells)

    def get_live_neighbors_count(self, row, col):
        """Retorna o número de vizinhos vivos da célula na linha row e coluna col"""
        count = 0
        for drow in range(-1, 2):
            for dcol in range(-1, 2):
                if drow != 0 or dcol != 0:
                    nrow, ncol = (row + drow) % self.height , (col + dcol) % self.width
                    count += self[nrow, ncol]
        return count

    def step(self):
        """Avança a simulação em uma etapa"""
        new_grid = Grid(self.width, self.height)
        for row in range(self.height):
           for col in range(self.width):
               state = self[row, col]
               live_neighbors = self.get_live_neighbors_count(row, col)
               if state == LIVE and live_neighbors < 2:
                   new_grid[row, col] = DEAD
               elif state == LIVE and live_neighbors > 3:
                   new_grid[row, col] = DEAD
               elif state == DEAD and live_neighbors == 3:
                   new_grid[row, col] = LIVE
               else:
                   new_grid[row, col] = state
        self._cells = new_grid._cells

# =========================== Tests ====================================
class Demo:
    def __init__(self):
        self.simulation_config()
        self.ncurses_config()

    def ncurses_config(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.pad = curses.newpad(self.grid.height+3, self.grid.width+20)
        self.calc_drawing_area()

    def calc_drawing_area(self):
        self.maxrow, self.maxcol = self.stdscr.getmaxyx()

    def simulation_config(self): 
        self.grid = Grid(20, 30, random_fill=True)
        self.paused = False
        self.running = True

    def draw(self):
        self.pad.clear()
        self.pad.addstr(str(self.grid))
        self.pad.addstr(f"\nquit [q]    reset [r]   {'play' if self.paused else 'pause'} [p]   step [s]")
        self.pad.refresh(0, 0, 0, 0, self.maxrow-4, self.maxcol-5)
        self.stdscr.refresh()

    def update(self):
        if not self.paused:
            self.grid.step()
        time.sleep(.1)

    def process_input(self):
        key = self.stdscr.getch()
        if key:
            if key == ord("q"):
                self.running = False
            elif key == ord("r"):
                self.grid = Grid(20, 30, random_fill=True)
            elif key == ord("p"):
                self.paused = not self.paused
            elif key == ord("s"):
                self.paused = True
                self.grid.step()
            elif key == curses.KEY_RESIZE:
                self.calc_drawing_area()

    def run(self):
        while self.running:
            self.process_input()
            self.draw()
            self.update()

        curses.endwin()

if __name__ == "__main__":
    Demo().run()
