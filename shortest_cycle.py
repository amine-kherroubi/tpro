import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from queue import Queue


class UndirectedGraph:
    __slots__ = ("_adjacency_matrix", "_vertices_count")

    def __init__(self, vertices_count: int) -> None:
        self._adjacency_matrix: list[list[bool]] = [
            [False for _ in range(vertices_count)] for _ in range(vertices_count)
        ]
        self._vertices_count: int = vertices_count

    def link(self, u: int, v: int) -> None:
        if u == v:
            return
        self._adjacency_matrix[u][v] = True
        self._adjacency_matrix[v][u] = True

    def unlink(self, u: int, v: int) -> None:
        self._adjacency_matrix[u][v] = False
        self._adjacency_matrix[v][u] = False

    def get_shortest_cycle(self) -> list[int]:
        shortest_cycle: list[int] = []

        @dataclass(slots=True)
        class VertexInfo:
            discovered: bool
            parent: int
            distance_from_root: int

        for root in range(self._vertices_count):
            bfs_queue: Queue[int] = Queue()
            vertex_info: list[VertexInfo] = [
                VertexInfo(False, -1, -1) for _ in range(self._vertices_count)
            ]

            vertex_info[root].discovered = True
            vertex_info[root].distance_from_root = 0
            bfs_queue.put(root)

            while not bfs_queue.empty():
                current_vertex: int = bfs_queue.get()
                for neighbor in range(self._vertices_count):
                    if self._adjacency_matrix[current_vertex][neighbor]:
                        if not vertex_info[neighbor].discovered:
                            bfs_queue.put(neighbor)
                            vertex_info[neighbor] = VertexInfo(
                                True,
                                current_vertex,
                                vertex_info[current_vertex].distance_from_root + 1,
                            )
                        elif neighbor != vertex_info[current_vertex].parent:
                            cycle_length = (
                                vertex_info[current_vertex].distance_from_root
                                + vertex_info[neighbor].distance_from_root
                                + 1
                            )

                            if not shortest_cycle or cycle_length < len(shortest_cycle):
                                path_from_current: list[int] = [current_vertex]
                                temp = current_vertex
                                while vertex_info[temp].parent != -1:
                                    temp = vertex_info[temp].parent
                                    path_from_current.append(temp)

                                path_from_neighbor: list[int] = [neighbor]
                                temp = neighbor
                                while vertex_info[temp].parent != -1:
                                    temp = vertex_info[temp].parent
                                    path_from_neighbor.append(temp)
                                    if temp in path_from_current:
                                        break

                                lca = temp
                                cycle: list[int] = path_from_neighbor
                                cycle.reverse()
                                cycle.extend(
                                    path_from_current[: path_from_current.index(lca)]
                                )
                                shortest_cycle = cycle

        return shortest_cycle


class GraphCycleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Cycle Finder")
        self.root.geometry("500x400")

        self.graph = None

        # Vertices input
        frame1 = ttk.Frame(root, padding=10)
        frame1.pack(fill=tk.X)

        ttk.Label(frame1, text="Number of vertices:").pack(side=tk.LEFT)
        self.vertices_entry = ttk.Entry(frame1, width=10)
        self.vertices_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame1, text="Create Graph", command=self.create_graph).pack(
            side=tk.LEFT
        )

        # Edges input
        frame2 = ttk.Frame(root, padding=10)
        frame2.pack(fill=tk.X)

        ttk.Label(frame2, text="Edge (u v):").pack(side=tk.LEFT)
        self.edge_entry = ttk.Entry(frame2, width=10)
        self.edge_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame2, text="Add Edge", command=self.add_edge).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(frame2, text="Remove Edge", command=self.remove_edge).pack(
            side=tk.LEFT
        )

        # Edge list display
        frame3 = ttk.Frame(root, padding=10)
        frame3.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame3, text="Current Edges:").pack(anchor=tk.W)
        self.edges_text = tk.Text(frame3, height=8, width=50)
        self.edges_text.pack(fill=tk.BOTH, expand=True)

        # Compute button
        frame4 = ttk.Frame(root, padding=10)
        frame4.pack(fill=tk.X)

        ttk.Button(frame4, text="Find Shortest Cycle", command=self.find_cycle).pack()

        # Result display
        frame5 = ttk.Frame(root, padding=10)
        frame5.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame5, text="Result:").pack(anchor=tk.W)
        self.result_text = tk.Text(frame5, height=4, width=50)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.edges = []

    def create_graph(self):
        try:
            n = int(self.vertices_entry.get())
            if n <= 0:
                raise ValueError
            self.graph = UndirectedGraph(n)
            self.edges = []
            self.edges_text.delete(1.0, tk.END)
            self.result_text.delete(1.0, tk.END)
            messagebox.showinfo("Success", f"Graph with {n} vertices created!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer")

    def add_edge(self):
        if self.graph is None:
            messagebox.showerror("Error", "Create a graph first")
            return

        try:
            parts = self.edge_entry.get().strip().split()
            if len(parts) != 2:
                raise ValueError
            u, v = int(parts[0]), int(parts[1])

            if (
                u < 0
                or v < 0
                or u >= self.graph._vertices_count
                or v >= self.graph._vertices_count
            ):
                messagebox.showerror(
                    "Error",
                    f"Vertices must be between 0 and {self.graph._vertices_count - 1}",
                )
                return

            self.graph.link(u, v)
            self.edges.append((u, v))
            self.edges_text.insert(tk.END, f"{u} - {v}\n")
            self.edge_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter edge as two integers (e.g., '0 1')")

    def remove_edge(self):
        if self.graph is None:
            messagebox.showerror("Error", "Create a graph first")
            return

        try:
            parts = self.edge_entry.get().strip().split()
            if len(parts) != 2:
                raise ValueError
            u, v = int(parts[0]), int(parts[1])

            self.graph.unlink(u, v)
            if (u, v) in self.edges:
                self.edges.remove((u, v))
            elif (v, u) in self.edges:
                self.edges.remove((v, u))

            self.edges_text.delete(1.0, tk.END)
            for edge in self.edges:
                self.edges_text.insert(tk.END, f"{edge[0]} - {edge[1]}\n")
            self.edge_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter edge as two integers (e.g., '0 1')")

    def find_cycle(self):
        if self.graph is None:
            messagebox.showerror("Error", "Create a graph first")
            return

        cycle = self.graph.get_shortest_cycle()
        self.result_text.delete(1.0, tk.END)

        if cycle:
            cycle_str = " → ".join(map(str, cycle))
            self.result_text.insert(
                tk.END, f"Shortest cycle (length {len(cycle)}):\n{cycle_str}"
            )
        else:
            self.result_text.insert(tk.END, "No cycle found in the graph")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphCycleGUI(root)
    root.mainloop()
