#!/usr/bin/env python3
"""
TSP Solver: Exact Enumeration and Bellman-Held-Karp Dynamic Programming
Enhanced GUI with improved ergonomics and visual feedback
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import itertools
import time
import random

# =============================================================================
# ALGORITHMS
# =============================================================================


def tsp_exact(dist: list[list[float]]) -> tuple[float, list[int]]:
    """
    Exact TSP solution using brute force enumeration.
    Complexity: O(n!)

    Args:
        dist: Distance matrix where dist[i][j] is distance from city i to j

    Returns:
        (min_cost, optimal_path) where path starts and ends at city 0
    """
    n: int = len(dist)
    if n == 0:
        return 0.0, []
    if n == 1:
        return 0.0, [0, 0]

    vertices: list[int] = list(range(1, n))
    best_cost: float = float("inf")
    best_perm: tuple[int, ...] | None = None

    # Try all permutations of cities 1 to n-1 (city 0 is fixed start)
    for perm in itertools.permutations(vertices):
        cost: float = dist[0][perm[0]]  # Start from city 0
        if cost == float("inf"):
            continue

        # Calculate total path cost
        valid: bool = True
        for i in range(len(perm) - 1):
            edge_cost: float = dist[perm[i]][perm[i + 1]]
            if edge_cost == float("inf"):
                valid = False
                break
            cost += edge_cost

        if not valid:
            continue

        # Add return to city 0
        return_cost: float = dist[perm[-1]][0]
        if return_cost == float("inf"):
            continue
        cost += return_cost

        # Update best solution
        if cost < best_cost:
            best_cost = cost
            best_perm = perm

    if best_perm is None:
        return float("inf"), []

    path: list[int] = [0] + list(best_perm) + [0]
    return best_cost, path


def tsp_held_karp(dist: list[list[float]]) -> tuple[float, list[int]]:
    """
    TSP solution using Bellman-Held-Karp dynamic programming.
    Complexity: O(n² × 2ⁿ)

    Args:
        dist: Distance matrix where dist[i][j] is distance from city i to j

    Returns:
        (min_cost, optimal_path) where path starts and ends at city 0
    """
    n = len(dist)
    if n == 0:
        return 0.0, []
    if n == 1:
        return 0.0, [0, 0]

    ALL = 1 << n

    # DP[mask][i] = minimum cost to visit cities in mask, end at i
    DP = [[float("inf")] * n for _ in range(ALL)]
    parent = [[-1] * n for _ in range(ALL)]

    # Base case: start at city 0
    DP[1 << 0][0] = 0

    # Build DP
    for mask in range(ALL):
        for i in range(n):
            if not (mask & (1 << i)):  # i not in mask
                continue
            if DP[mask][i] == float("inf"):  # unreachable state
                continue

            # Try extending to city j
            for j in range(n):
                if mask & (1 << j):  # j already visited
                    continue

                new_mask = mask | (1 << j)
                new_cost = DP[mask][i] + dist[i][j]

                if new_cost < DP[new_mask][j]:
                    DP[new_mask][j] = new_cost
                    parent[new_mask][j] = i

    # Find best tour ending at any city, then return to 0
    full = (1 << n) - 1
    best_cost = float("inf")
    best_last = None

    for i in range(1, n):
        total = DP[full][i] + dist[i][0]
        if total < best_cost:
            best_cost = total
            best_last = i

    if best_last is None:
        return float("inf"), []

    # Reconstruct path
    path = []
    mask = full
    curr = best_last

    while curr != 0:
        path.append(curr)
        prev = parent[mask][curr]
        mask ^= 1 << curr
        curr = prev

    path.reverse()
    return best_cost, [0] + path + [0]


# =============================================================================
# UTILITIES
# =============================================================================


def generate_random_graph(
    n: int, symmetric: bool = True, max_weight: int = 99
) -> list[list[float]]:
    """Generate a random complete graph."""
    mat: list[list[float]] = [
        [0.0 if i == j else 0.0 for j in range(n)] for i in range(n)
    ]

    for i in range(n):
        for j in range(i + 1, n):
            weight: int = random.randint(1, max_weight)
            mat[i][j] = float(weight)
            mat[j][i] = (
                float(weight) if symmetric else float(random.randint(1, max_weight))
            )

    return mat


def matrix_to_string(mat: list[list[float]]) -> str:
    """Convert distance matrix to formatted string."""
    if not mat:
        return ""

    n: int = len(mat)
    lines: list[str] = []

    for i in range(n):
        row: list[str] = []
        for j in range(n):
            val: float = mat[i][j]
            if val == float("inf"):
                row.append("∞")
            elif abs(val - int(val)) < 1e-9:
                row.append(f"{int(val):>4}")
            else:
                row.append(f"{val:>4.1f}")
        lines.append("  ".join(row))

    return "\n".join(lines)


# =============================================================================
# GUI APPLICATION
# =============================================================================


class TSPApplication:
    """Enhanced TSP Solver GUI with improved ergonomics."""

    MAX_GRID_SIZE: int = 15

    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        root.title("TSP Solver - Exact & Bellman-Held-Karp")
        root.geometry("900x700")

        # Variables
        self.n_var: tk.StringVar = tk.StringVar(value="6")
        self.symmetric_var: tk.BooleanVar = tk.BooleanVar(value=True)
        self.entries: list[list[tk.Entry]] = []
        self.current_matrix: list[list[float]] = []

        self._setup_ui()
        self.create_matrix_grid()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        # Control Panel
        control_frame: ttk.LabelFrame = ttk.LabelFrame(
            self.root, text="Configuration", padding=10
        )
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Size control
        size_frame: tk.Frame = tk.Frame(control_frame)
        size_frame.pack(fill=tk.X, pady=5)

        ttk.Label(size_frame, text="Number of cities (n):").pack(side=tk.LEFT, padx=5)
        size_spinbox: ttk.Spinbox = ttk.Spinbox(
            size_frame, from_=3, to=20, textvariable=self.n_var, width=5
        )
        size_spinbox.pack(side=tk.LEFT, padx=5)

        ttk.Checkbutton(
            size_frame, text="Symmetric (undirected)", variable=self.symmetric_var
        ).pack(side=tk.LEFT, padx=20)

        # Buttons
        button_frame: tk.Frame = tk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            button_frame, text="🔄 Create Grid", command=self.create_matrix_grid
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🎲 Random Fill", command=self.random_fill).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            button_frame, text="🚀 Run Algorithms", command=self.run_algorithms
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Benchmark", command=self.run_benchmark).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            button_frame, text="🗑️ Clear Results", command=self.clear_results
        ).pack(side=tk.LEFT, padx=5)

        # Matrix Frame
        matrix_label: ttk.LabelFrame = ttk.LabelFrame(
            self.root, text="Distance Matrix", padding=10
        )
        matrix_label.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

        # Canvas with scrollbar for large matrices
        self.canvas: tk.Canvas = tk.Canvas(matrix_label, height=250)
        scrollbar_y: ttk.Scrollbar = ttk.Scrollbar(
            matrix_label, orient=tk.VERTICAL, command=self.canvas.yview
        )
        scrollbar_x: ttk.Scrollbar = ttk.Scrollbar(
            matrix_label, orient=tk.HORIZONTAL, command=self.canvas.xview
        )

        self.matrix_frame: tk.Frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.matrix_frame, anchor=tk.NW)

        self.canvas.configure(
            yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.matrix_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Results Frame
        results_label: ttk.LabelFrame = ttk.LabelFrame(
            self.root, text="Results & Timings", padding=10
        )
        results_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.results_text: ScrolledText = ScrolledText(
            results_label, height=15, font=("Courier", 9)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var: tk.StringVar = tk.StringVar(value="Ready")
        status_bar: ttk.Label = ttk.Label(
            self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def create_matrix_grid(self) -> None:
        """Create the matrix input grid."""
        try:
            n: int = int(self.n_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for n")
            return

        if n < 3 or n > 20:
            messagebox.showerror("Error", "n must be between 3 and 20")
            return

        # Clear previous grid
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        if n > self.MAX_GRID_SIZE:
            ttk.Label(
                self.matrix_frame,
                text=f"⚠️ Matrix too large to display (n={n})\n"
                + "Use 'Random Fill' and 'Run Algorithms' directly.",
                foreground="red",
                font=("Arial", 11),
            ).pack(pady=20)
            self.entries = []
            self.status_var.set(
                f"Grid hidden (n={n}). Algorithms will work with random data."
            )
            return

        # Create grid
        self.entries = [[None for _ in range(n)] for _ in range(n)]  # type: ignore

        # Headers
        ttk.Label(self.matrix_frame, text="", width=4).grid(
            row=0, column=0, padx=2, pady=2
        )
        for j in range(n):
            ttk.Label(
                self.matrix_frame, text=str(j), width=6, style="Header.TLabel"
            ).grid(row=0, column=j + 1, padx=2, pady=2)
            ttk.Label(
                self.matrix_frame, text=str(j), width=4, style="Header.TLabel"
            ).grid(row=j + 1, column=0, padx=2, pady=2)

        # Matrix entries
        for i in range(n):
            for j in range(n):
                if i == j:
                    entry: tk.Entry = tk.Entry(
                        self.matrix_frame,
                        width=6,
                        justify=tk.CENTER,
                        state="readonly",
                        readonlybackground="#e0e0e0",
                    )
                    entry.insert(0, "0")
                else:
                    entry: tk.Entry = tk.Entry(
                        self.matrix_frame, width=6, justify=tk.CENTER
                    )

                entry.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                self.entries[i][j] = entry

        self.status_var.set(f"Grid created for {n} cities")

    def random_fill(self) -> None:
        """Fill the matrix with random values."""
        try:
            n: int = int(self.n_var.get())
        except ValueError:
            return

        symmetric: bool = self.symmetric_var.get()
        self.current_matrix = generate_random_graph(n, symmetric)

        if len(self.entries) == 0 or len(self.entries) != n:
            self.status_var.set(f"Random graph generated (n={n})")
            return

        # Fill visible grid
        for i in range(n):
            for j in range(n):
                entry: tk.Entry = self.entries[i][j]
                if i != j:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(int(self.current_matrix[i][j])))

        self.status_var.set(
            f"Random {'symmetric' if symmetric else 'asymmetric'} "
            + f"graph generated (n={n})"
        )

    def run_algorithms(self) -> None:
        """Run both TSP algorithms and display results."""
        try:
            n: int = int(self.n_var.get())
        except ValueError:
            return

        # Get matrix
        if len(self.entries) == n:
            mat: list[list[float]] = self._parse_matrix()
        else:
            mat: list[list[float]] = generate_random_graph(n, self.symmetric_var.get())

        self.current_matrix = mat

        # Display matrix
        self.results_text.insert(tk.END, "\n" + "=" * 70 + "\n")
        self.results_text.insert(tk.END, f"TSP SOLUTION FOR {n} CITIES\n")
        self.results_text.insert(tk.END, "=" * 70 + "\n\n")

        if n <= 10:
            self.results_text.insert(tk.END, "Distance Matrix:\n")
            self.results_text.insert(tk.END, matrix_to_string(mat) + "\n\n")

        # Run Bellman-Held-Karp
        self.status_var.set("Running Bellman-Held-Karp...")
        self.root.update()

        t_start: float = time.perf_counter()
        hk_cost, hk_path = tsp_held_karp(mat)
        t_end: float = time.perf_counter()
        hk_time: float = t_end - t_start

        self.results_text.insert(tk.END, "BELLMAN-HELD-KARP (Dynamic Programming)\n")
        self.results_text.insert(tk.END, f"  Cost: {hk_cost:.2f}\n")
        self.results_text.insert(tk.END, f"  Path: {' → '.join(map(str, hk_path))}\n")
        self.results_text.insert(tk.END, f"  Time: {hk_time:.6f} seconds\n")
        self.results_text.insert(tk.END, f"  Complexity: O(n² × 2ⁿ)\n\n")

        # Run Exact enumeration (only for small n)
        if n <= 10:
            self.status_var.set("Running Exact Enumeration...")
            self.root.update()

            t_start = time.perf_counter()
            ex_cost, ex_path = tsp_exact(mat)
            t_end = time.perf_counter()
            ex_time: float = t_end - t_start

            self.results_text.insert(tk.END, "EXACT ENUMERATION (Brute Force)\n")
            self.results_text.insert(tk.END, f"  Cost: {ex_cost:.2f}\n")
            self.results_text.insert(
                tk.END, f"  Path: {' → '.join(map(str, ex_path))}\n"
            )
            self.results_text.insert(tk.END, f"  Time: {ex_time:.6f} seconds\n")
            self.results_text.insert(tk.END, f"  Complexity: O(n!)\n\n")

            # Comparison
            speedup: float = ex_time / hk_time if hk_time > 0 else 0
            self.results_text.insert(
                tk.END, f"SPEEDUP: Held-Karp is {speedup:.2f}x faster\n"
            )
        else:
            self.results_text.insert(
                tk.END, "EXACT ENUMERATION: Skipped (n > 10, too slow)\n"
            )

        self.results_text.see(tk.END)
        self.status_var.set("Algorithms completed")

    def run_benchmark(self) -> None:
        """Run benchmark comparing both algorithms."""
        self.results_text.insert(tk.END, "\n" + "=" * 70 + "\n")
        self.results_text.insert(tk.END, "BENCHMARK: Symmetric Random Graphs\n")
        self.results_text.insert(tk.END, "=" * 70 + "\n\n")
        self.results_text.insert(
            tk.END, f"{'n':<5}{'Held-Karp (s)':<20}{'Exact (s)':<20}{'Speedup':<10}\n"
        )
        self.results_text.insert(tk.END, "-" * 70 + "\n")

        for n in range(3, 14):
            mat: list[list[float]] = generate_random_graph(n, symmetric=True)

            # Bellman-Held-Karp
            t0: float = time.perf_counter()
            _, _ = tsp_held_karp(mat)
            t1: float = time.perf_counter()
            hk_time: float = t1 - t0

            # Exact (only up to n=10)
            if n <= 10:
                t2: float = time.perf_counter()
                _, _ = tsp_exact(mat)
                t3: float = time.perf_counter()
                ex_time: float = t3 - t2
                speedup: float = ex_time / hk_time if hk_time > 0 else 0

                self.results_text.insert(
                    tk.END, f"{n:<5}{hk_time:<20.6f}{ex_time:<20.6f}{speedup:<10.2f}x\n"
                )
            else:
                self.results_text.insert(
                    tk.END, f"{n:<5}{hk_time:<20.6f}{'---':<20}{'---':<10}\n"
                )

            self.results_text.see(tk.END)
            self.root.update()

        self.results_text.insert(tk.END, "\n✅ Benchmark complete!\n")
        self.status_var.set("Benchmark completed")

    def clear_results(self) -> None:
        """Clear the results text area."""
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Results cleared")

    def _parse_matrix(self) -> list[list[float]]:
        """Parse matrix from entry widgets."""
        n: int = len(self.entries)
        mat: list[list[float]] = [[0.0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i == j:
                    mat[i][j] = 0.0
                    continue

                text: str = self.entries[i][j].get().strip()
                if text == "" or text.lower() == "inf":
                    mat[i][j] = float("inf")
                else:
                    try:
                        mat[i][j] = float(text)
                    except ValueError:
                        mat[i][j] = float("inf")

        return mat


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Entry point of the application."""
    root: tk.Tk = tk.Tk()
    app: TSPApplication = TSPApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
