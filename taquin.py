import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import heapq
import time
import random
import threading
from typing import List, Tuple, Optional, Dict, Union, Any

# Type alias pour la clarté
State = Tuple[Tuple[int, ...], ...]


class TaquinSolver:
    def __init__(self) -> None:
        self.goal_state: State = (
            (1, 2, 3, 4),
            (5, 6, 7, 8),
            (9, 10, 11, 12),
            (13, 14, 15, 0),
        )
        self._abort: bool = False  # Drapeau pour arrêter le calcul

    def request_stop(self) -> None:
        self._abort = True

    def manhattan_distance(self, state: State) -> int:
        distance = 0
        for i in range(4):
            for j in range(4):
                val = state[i][j]
                if val != 0:
                    target_row, target_col = (val - 1) // 4, (val - 1) % 4
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance

    def misplaced_tiles(self, state: State) -> int:
        return sum(
            1
            for i in range(4)
            for j in range(4)
            if state[i][j] != 0 and state[i][j] != self.goal_state[i][j]
        )

    def is_solvable(self, state: State) -> bool:
        flat = [val for row in state for val in row if val != 0]
        inversions = sum(
            1
            for i in range(len(flat))
            for j in range(i + 1, len(flat))
            if flat[i] > flat[j]
        )

        # Trouver la ligne du vide (0) en partant du bas
        empty_row = -1
        for i in range(4):
            if 0 in state[i]:
                empty_row = 4 - i
                break

        if empty_row % 2 == 0:
            return inversions % 2 != 0
        else:
            return inversions % 2 == 0

    def solve(
        self,
        start_state: State,
        heuristic: str = "manhattan",
        algorithm: str = "astar",
        weight: float = 1.5,
    ) -> Dict[str, Any]:

        self._abort = False
        if not self.is_solvable(start_state):
            return {"success": False, "message": "Configuration insoluble."}

        open_set: List[Tuple[float, int, State]] = []
        h_func = (
            self.manhattan_distance
            if heuristic == "manhattan"
            else self.misplaced_tiles
        )

        p = weight if algorithm == "wastar" else 1.0
        heapq.heappush(open_set, (h_func(start_state) * p, 0, start_state))

        came_from: Dict[State, Optional[State]] = {start_state: None}
        g_score: Dict[State, int] = {start_state: 0}

        nodes_explored = 0
        start_time = time.time()

        while open_set:
            # VÉRIFICATION DE L'ARRÊT DEMANDÉ
            if self._abort:
                return {
                    "success": False,
                    "message": "Calcul interrompu par l'utilisateur.",
                }

            _, g, current = heapq.heappop(open_set)
            nodes_explored += 1

            if current == self.goal_state:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return {
                    "success": True,
                    "path": path[::-1],
                    "nodes": nodes_explored,
                    "time": (time.time() - start_time) * 1000,
                }

            # Génération des voisins
            r, c = -1, -1
            for i in range(4):
                for j in range(4):
                    if current[i][j] == 0:
                        r, c = i, j

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 4 and 0 <= nc < 4:
                    # Création rapide de l'état voisin
                    temp = [list(row) for row in current]
                    temp[r][c], temp[nr][nc] = temp[nr][nc], temp[r][c]
                    neighbor = tuple(tuple(row) for row in temp)

                    tentative_g = g + 1
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        g_score[neighbor] = tentative_g
                        f = tentative_g + (h_func(neighbor) * p)
                        came_from[neighbor] = current
                        heapq.heappush(open_set, (f, tentative_g, neighbor))

        return {"success": False, "message": "Aucune solution."}


class TaquinGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Taquin 15 Pro - Multithreaded")
        self.root.geometry("1000x750")
        self.root.configure(bg="#f0f2f5")

        self.solver = TaquinSolver()
        self.grid: List[List[int]] = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15],
        ]
        self.edit_mode: bool = False
        self.is_running: bool = False  # Calcul en cours ?

        self.setup_ui()
        self.update_grid_display()

    def setup_ui(self) -> None:
        # Style
        s = ttk.Style()
        s.configure("TButton", font=("Segoe UI", 10))

        main_container = ttk.Frame(self.root, padding=25)
        main_container.pack(expand=True, fill="both")

        # --- GAUCHE ---
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side="left", padx=20)

        self.grid_frame = tk.Frame(left_panel, bg="#bbada0", bd=8, relief="flat")
        self.grid_frame.pack()

        self.btn_matrix: List[List[tk.Label]] = []
        for i in range(4):
            row_btns = []
            for j in range(4):
                lbl = tk.Label(
                    self.grid_frame,
                    text="",
                    width=5,
                    height=2,
                    font=("Arial", 24, "bold"),
                    fg="white",
                    bd=0,
                )
                lbl.grid(row=i, column=j, padx=5, pady=5)
                lbl.bind("<Button-1>", lambda e, r=i, c=j: self.on_cell_click(r, c))
                row_btns.append(lbl)
            self.btn_matrix.append(row_btns)

        # Actions
        btn_box = ttk.Frame(left_panel, padding=15)
        btn_box.pack(fill="x")

        self.edit_btn = tk.Button(
            btn_box,
            text="✏️ Mode Édition",
            bg="#3498db",
            fg="white",
            command=self.toggle_edit_mode,
            relief="flat",
            padx=10,
        )
        self.edit_btn.pack(side="left", expand=True, fill="x", padx=5)

        ttk.Button(btn_box, text="Mélanger", command=self.shuffle).pack(
            side="left", expand=True, padx=5
        )
        ttk.Button(btn_box, text="Réinitialiser", command=self.reset).pack(
            side="left", expand=True, padx=5
        )

        # --- DROITE ---
        right_panel = ttk.LabelFrame(
            main_container, text=" Paramètres & Contrôle ", padding=20
        )
        right_panel.pack(side="right", fill="both", expand=True)

        ttk.Label(right_panel, text="Algorithme:").pack(anchor="w")
        self.algo_var = tk.StringVar(value="astar")
        ttk.Radiobutton(
            right_panel, text="A* (Optimal)", variable=self.algo_var, value="astar"
        ).pack(anchor="w")
        ttk.Radiobutton(
            right_panel,
            text="Weighted A* (Rapide)",
            variable=self.algo_var,
            value="wastar",
        ).pack(anchor="w")

        ttk.Label(right_panel, text="\nPoids WA* (1.0 - 5.0):").pack(anchor="w")
        self.weight_var = tk.DoubleVar(value=1.5)
        ttk.Scale(
            right_panel,
            from_=1.0,
            to=5.0,
            variable=self.weight_var,
            orient="horizontal",
        ).pack(fill="x", pady=5)

        ttk.Label(right_panel, text="\nHeuristique:").pack(anchor="w")
        self.heur_var = tk.StringVar(value="manhattan")
        ttk.Radiobutton(
            right_panel,
            text="Distance Manhattan",
            variable=self.heur_var,
            value="manhattan",
        ).pack(anchor="w")
        ttk.Radiobutton(
            right_panel, text="Mal placés", variable=self.heur_var, value="misplaced"
        ).pack(anchor="w")

        # BOUTONS DE CONTRÔLE
        self.solve_btn = tk.Button(
            right_panel,
            text="LANCER LA RÉSOLUTION",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.start_solving_thread,
            relief="flat",
            pady=10,
        )
        self.solve_btn.pack(fill="x", pady=(20, 10))

        self.stop_btn = tk.Button(
            right_panel,
            text="ARRÊTER LE CALCUL",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.stop_solving,
            relief="flat",
            pady=10,
        )
        self.stop_btn.pack(fill="x", pady=5)
        self.stop_btn.config(state="disabled")  # Désactivé par défaut

        self.log_box = tk.Text(
            right_panel,
            height=12,
            width=40,
            state="disabled",
            font=("Consolas", 9),
            bg="#f8f9fa",
        )
        self.log_box.pack(fill="both", expand=True, pady=15)

    def update_grid_display(self) -> None:
        for i in range(4):
            for j in range(4):
                val = self.grid[i][j]
                lbl = self.btn_matrix[i][j]
                if val == 0:
                    lbl.config(text="", bg="#cdc1b4")
                else:
                    lbl.config(
                        text=str(val),
                        bg="#edc22e" if val > 8 else "#eee4da",
                        fg="white" if val > 8 else "#776e65",
                    )
                lbl.config(
                    highlightthickness=2 if self.edit_mode else 0,
                    highlightbackground="#e74c3c",
                )

    def on_cell_click(self, r: int, c: int) -> None:
        if self.is_running:
            return
        if self.edit_mode:
            res = simpledialog.askinteger(
                "Édition", "Valeur (0-15):", minvalue=0, maxvalue=15
            )
            if res is not None:
                self.grid[r][c] = res
                self.update_grid_display()
        else:
            # Recherche du vide
            zr, zc = -1, -1
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] == 0:
                        zr, zc = i, j
            if abs(r - zr) + abs(c - zc) == 1:
                self.grid[zr][zc], self.grid[r][c] = self.grid[r][c], self.grid[zr][zc]
                self.update_grid_display()

    def toggle_edit_mode(self) -> None:
        if self.edit_mode:
            flat = [v for r in self.grid for v in r]
            if sorted(flat) != list(range(16)):
                messagebox.showerror(
                    "Erreur",
                    "La grille doit contenir les chiffres de 0 à 15 sans doublons.",
                )
                return
            self.edit_mode = False
            self.edit_btn.config(text="✏️ Mode Édition", bg="#3498db")
            self.log("Grille validée.")
        else:
            self.edit_mode = True
            self.edit_btn.config(text="💾 Valider Grille", bg="#f39c12")
        self.update_grid_display()

    def log(self, text: str) -> None:
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    # --- LOGIQUE MULTITHREAD ---

    def start_solving_thread(self) -> None:
        if self.edit_mode:
            return

        self.is_running = True
        self.solve_btn.config(state="disabled", bg="#95a5a6")
        self.stop_btn.config(state="normal")
        self.log("Début du calcul (Thread séparé)...")

        # Lancement du thread
        start_state = tuple(tuple(row) for row in self.grid)
        thread = threading.Thread(target=self._run_solver, args=(start_state,))
        thread.daemon = True  # Le thread s'arrête si on ferme la fenêtre
        thread.start()

    def _run_solver(self, start_state: State) -> None:
        # Cette fonction tourne en tâche de fond
        result = self.solver.solve(
            start_state,
            heuristic=self.heur_var.get(),
            algorithm=self.algo_var.get(),
            weight=self.weight_var.get(),
        )

        # On renvoie le résultat au thread principal de l'UI
        self.root.after(0, lambda: self._handle_result(result))

    def _handle_result(self, result: Dict[str, Any]) -> None:
        self.is_running = False
        self.solve_btn.config(state="normal", bg="#2ecc71")
        self.stop_btn.config(state="disabled")

        if result["success"]:
            self.log(f"Solution trouvée ! ({len(result['path'])-1} coups)")
            self._animate(result["path"])
        else:
            self.log(result["message"])
            messagebox.showinfo("Résultat", result["message"])

    def stop_solving(self) -> None:
        self.log("Demande d'arrêt envoyée...")
        self.solver.request_stop()

    def _animate(self, path: List[State]) -> None:
        if not path:
            return
        self.grid = [list(row) for row in path.pop(0)]
        self.update_grid_display()
        self.root.after(150, lambda: self._animate(path))

    def shuffle(self) -> None:
        if self.is_running:
            return
        for _ in range(100):
            r, c = -1, -1
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] == 0:
                        r, c = i, j
            # Mouvement aléatoire valide
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            dr, dc = random.choice(moves)
            if 0 <= r + dr < 4 and 0 <= c + dc < 4:
                self.grid[r][c], self.grid[r + dr][c + dc] = (
                    self.grid[r + dr][c + dc],
                    self.grid[r][c],
                )
        self.update_grid_display()

    def reset(self) -> None:
        if self.is_running:
            return
        self.grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        self.update_grid_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaquinGUI(root)
    root.mainloop()
