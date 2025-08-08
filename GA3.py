import random
from turtle import rt
import matplotlib.pyplot as plt
from Flip_Transpose import HamiltonianSTL
import tkinter as tk
from tkinter import filedialog
from matplotlib.widgets import Button

class HamiltonianZoningWithEdges:
    def __init__(self, hamiltonian_stl):
        self.h = hamiltonian_stl
        self.width = self.h.width
        self.height = self.h.height
        self.zones = {
            (x, y): 1 if x < self.width // 2 else 2
            for y in range(self.height)
            for x in range(self.width)
        }
        self.path = self.generate_path_from_edges()

    def generate_path_from_edges(self):
        neighbors = {pt: [] for pt in self.zones}
        for y in range(self.height):
            for x in range(self.width - 1):
                if self.h.H[y][x]:
                    a, b = (x, y), (x + 1, y)
                    neighbors[a].append(b)
                    neighbors[b].append(a)
        for y in range(self.height - 1):
            for x in range(self.width):
                if self.h.V[y][x]:
                    a, b = (x, y), (x, y + 1)
                    neighbors[a].append(b)
                    neighbors[b].append(a)

        def dfs(current, visited, path):
            if len(path) == self.width * self.height:
                return path
            for nxt in neighbors[current]:
                if nxt not in visited:
                    visited.add(nxt)
                    result = dfs(nxt, visited, path + [nxt])
                    if result:
                        return result
                    visited.remove(nxt)
            return None

        for start in neighbors:
            result = dfs(start, {start}, [start])
            if result:
                return result
        return []


    def compute_fitness(self):
        crossings = 0
        for y in range(self.height):
            for x in range(self.width - 1):
                if self.h.H[y][x] and self.zones[(x, y)] != self.zones[(x + 1, y)]:
                    crossings += 1
        for y in range(self.height - 1):
            for x in range(self.width):
                if self.h.V[y][x] and self.zones[(x, y)] != self.zones[(x, y + 1)]:
                    crossings += 1
        return crossings
    
    def plot(self, title="Hamiltonian Path"):
        fig, ax = plt.subplots()
        self.ax = ax 
        plt.subplots_adjust(bottom=0.3)
        self._plot_on_ax(ax)

        btn_load_ax = plt.axes([0.1, 0.05, 0.2, 0.075])
        btn_load = Button(btn_load_ax, 'Load File', color='lightgray', hovercolor='gray')
        btn_load.on_clicked(lambda event: self.load_edges_from_file(self.ax))

        btn_save_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
        btn_save = Button(btn_save_ax, 'Save Path', color='lightgray', hovercolor='gray')
        btn_save.on_clicked(lambda event: self.save_path_to_file())

        btn_run_ax = plt.axes([0.7, 0.05, 0.2, 0.075])
        btn_run = Button(btn_run_ax, '▶ Run', color='#98FB98', hovercolor='#90EE90')
        btn_run.on_clicked(lambda event: self.run_method_placeholder())

        plt.show()


    def save_path_to_file(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            print("Save cancelled.")
            return

        with open(file_path, 'w') as f:
            for i in range(len(self.path) - 1):
                x1, y1 = self.path[i]
                x2, y2 = self.path[i + 1]
                f.write(f"{x1},{y1},{x2},{y2}\n")

        print(f"Path saved to {file_path}")


    def run_method_placeholder(self):
        # Top-right transpose
        x_top, y_top = self.width - 3, 0
        if x_top >= 0 and y_top + 2 < self.height:
            subgrid_top = self.h.get_subgrid_by_corners((x_top, y_top), (x_top + 2, y_top + 2))
            self.ax.clear()
            self._plot_on_ax(self.ax)
            self._highlight_subgrid(self.ax, subgrid_top, color='orange')
            plt.draw()
            plt.pause(1.5)

            _, result_top = self.h.transpose_subgrid(subgrid_top)
            print("Top-right transpose result:", result_top)

            self.ax.clear()
            self.path = self.generate_path_from_edges()
            self._plot_on_ax(self.ax)
            self._highlight_subgrid(self.ax, subgrid_top, color='green')
            plt.draw()
            plt.pause(1.0)

            x = self.width - 3
            y = self.height - 4 

            if x < 0 or y < 0 or x + 2 >= self.width or y + 2 >= self.height:
                print("Corrected Bottom-right 3x3 subgrid is out of bounds.")
                return

            subgrid = self.h.get_subgrid_by_corners((x, y), (x + 2, y + 2))

            self.ax.clear()
            self._plot_on_ax(self.ax)
            self._highlight_subgrid(self.ax, subgrid, color='orange')
            plt.draw()
            plt.pause(1.5)

            _, result = self.h.transpose_subgrid(subgrid)
            print("Corrected Bottom-right transpose result:", result)

            self.ax.clear()
            self.path = self.generate_path_from_edges()
            self._plot_on_ax(self.ax)
            self._highlight_subgrid(self.ax, subgrid, color='green')
            plt.draw()


    def mutate(self):
        operation = random.choice(['flip', 'transpose'])
        if operation == 'flip':
            w, h = (3, 2) if random.random() < 0.5 else (2, 3)
        else:
            w, h = 3, 3

        x = random.randint(0, self.width - w)
        y = random.randint(0, self.height - h)

        subgrid = self.h.get_subgrid_by_corners((x, y), (x + w - 1, y + h - 1))

        Copy_H = [row[:] for row in self.h.H]
        Copy_V = [row[:] for row in self.h.V]

        before = self.compute_fitness()
        if operation == 'flip':
            _, result = self.h.flip_subgrid(subgrid)
        else:
            _, result = self.h.transpose_subgrid(subgrid)

        after = self.compute_fitness()

        if result not in ['flipped', 'transposed'] or after > before:
            self.h.H = Copy_H
            self.h.V = Copy_V
            return before
        return after

    def evolve(self, generations=10):
        best_fitness = self.compute_fitness()
        for _ in range(generations):
            new_fitness = self.mutate()
            if new_fitness < best_fitness:
                best_fitness = new_fitness
            if best_fitness == 0:
                break
        self.path = self.generate_path_from_edges()
        return best_fitness

    def load_edges_from_file(self, ax):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            print("No file selected.")
            return

        print("Loading file:", file_path)

        max_x = max_y = 0
        edges = []

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    x1, y1, x2, y2 = map(int, line.split(','))
                    max_x = max(max_x, x1, x2)
                    max_y = max(max_y, y1, y2)
                    edges.append(((x1, y1), (x2, y2)))
                except ValueError:
                    print("Invalid line:", line)

        new_width = max_x + 1
        new_height = max_y + 1
        print(f"Resizing grid to {new_width}x{new_height}")

        self.h = HamiltonianSTL(new_width, new_height, use_zigzag=False)
        self.width = new_width
        self.height = new_height

        for (p1, p2) in edges:
            self.h.set_edge(p1, p2, True)

        self.zones = {
            (x, y): 1 if x < self.width // 2 else 2
            for y in range(self.height)
            for x in range(self.width)
        }

        self.path = self.generate_path_from_edges()
        print(f"Generated path length: {len(self.path)}")

        ax.clear()
        self._plot_on_ax(ax)
        plt.draw()


    def _plot_on_ax(self, ax):
        ax.set_title("Hamiltonian Path", fontsize=14, fontweight='bold')

        for i in range(len(self.path) - 1):
            x0, y0 = self.path[i]
            x1, y1 = self.path[i + 1]
            zone0 = self.zones.get((x0, y0), 1)
            zone1 = self.zones.get((x1, y1), 1)
            color = "red" if zone0 != zone1 else "black"
            ax.plot([x0, x1], [y0, y1], color=color, linewidth=2, zorder=1)

        for (x, y), zone in self.zones.items():
            ax.scatter(x, y, s=50, c="royalblue" if zone == 1 else "seagreen", edgecolors='k', zorder=2)

        ax.set_aspect('equal')
        ax.grid(True, which='major', linestyle='--', alpha=0.4)
        ax.set_facecolor('#f8f9fa')
        ax.invert_yaxis()

    
    def animate_transposes(self, ax):
        fig = ax.figure

        for _ in range(3):
            x = random.randint(0, self.width - 3)
            y = random.randint(0, self.height - 3)
            subgrid = self.h.get_subgrid_by_corners((x, y), (x + 2, y + 2))

            ax.clear()
            self._plot_on_ax(ax)
            self._highlight_subgrid(ax, subgrid, color='orange')
            plt.draw()
            plt.pause(2)

            _, result = self.h.transpose_subgrid(subgrid)

            ax.clear()
            self._plot_on_ax(ax)
            self._highlight_subgrid(ax, subgrid, color='green')
            plt.draw()
            plt.pause(1)

        self.path = self.generate_path_from_edges()

        ax.clear()
        self._plot_on_ax(ax)
        plt.draw()


    def _highlight_subgrid(self, ax, subgrid, color='orange'):
        for row in subgrid:
            for pt in row:
                if pt:
                    x, y = pt
                    circle = plt.Circle(
                        (x, y), 
                        0.4, 
                        color=color, 
                        alpha=0.4, 
                        ec='black', 
                        lw=1.5, 
                        zorder=0
                    )
                    ax.add_patch(circle)

if __name__ == "__main__":
    h = HamiltonianSTL(10, 10, use_zigzag=False)
    z = HamiltonianZoningWithEdges(h)
    z.plot("Empty Grid")