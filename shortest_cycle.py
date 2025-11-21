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

        # BFS State
        @dataclass(slots=True)
        class VertexInfo:
            discovered: bool
            parent: int
            distance_from_root: int

        # Perform BFS from each vertex as root
        for root in range(self._vertices_count):
            bfs_queue: Queue[int] = Queue()
            vertex_info: list[VertexInfo] = [
                VertexInfo(False, -1, -1) for _ in range(self._vertices_count)
            ]

            # Initialize BFS root
            vertex_info[root].discovered = True
            vertex_info[root].distance_from_root = 0
            bfs_queue.put(root)

            while not bfs_queue.empty():
                current_vertex: int = bfs_queue.get()

                for neighbor in range(self._vertices_count):
                    if self._adjacency_matrix[current_vertex][neighbor]:
                        if not vertex_info[neighbor].discovered:
                            # Discover new vertex
                            bfs_queue.put(neighbor)
                            vertex_info[neighbor] = VertexInfo(
                                True,
                                current_vertex,
                                vertex_info[current_vertex].distance_from_root + 1,
                            )
                        elif neighbor != vertex_info[current_vertex].parent:
                            # Back edge found, cycle exists
                            cycle_length = (
                                vertex_info[current_vertex].distance_from_root
                                + vertex_info[neighbor].distance_from_root
                                + 1
                            )

                            # Update shortest cycle if it's smaller than the current one
                            if not shortest_cycle or cycle_length < len(shortest_cycle):
                                # Trace path from current vertex to root
                                path_from_current: list[int] = [current_vertex]
                                temp = current_vertex
                                while vertex_info[temp].parent != -1:
                                    temp = vertex_info[temp].parent
                                    path_from_current.append(temp)

                                # Trace path from neighbor to root until first common ancestor
                                path_from_neighbor: list[int] = [neighbor]
                                temp = neighbor
                                while vertex_info[temp].parent != -1:
                                    temp = vertex_info[temp].parent
                                    path_from_neighbor.append(temp)
                                    if temp in path_from_current:
                                        break

                                # Construct cycle
                                lca = temp
                                cycle: list[int] = path_from_neighbor
                                cycle.reverse()
                                cycle.extend(
                                    path_from_current[: path_from_current.index(lca)]
                                )
                                shortest_cycle = cycle

        return shortest_cycle
