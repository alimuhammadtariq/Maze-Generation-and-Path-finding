import random
import pygame


# Grid class to generate a random maze using DFS
class Grid(object):
    def __init__(self, height, width):
        assert height % 2 == 1 and width % 2 == 1, "Must have odd height and width"
        assert height >= 3 and width >= 3, "Width, height too small"
        self.height = height
        self.width = width
        self.walls = [[1 for x in range(width)] for y in range(height)]
        self.direction_vectors = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

    def is_visited(self, node):
        (x, y) = node
        return self.walls[y][x] == 0

    def set_visited(self, node):
        (x, y) = node
        self.walls[y][x] = 0

    def out_of_grid(self, node):
        (x, y) = node
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def get_unvisited_neighbours(self, current_node):
        (x, y) = current_node
        neighbours = []
        for _, dir1 in self.direction_vectors.items():
            (dx, dy) = dir1
            potential_neighbour_node = (x + dx * 2, y + dy * 2)
            if not self.out_of_grid(potential_neighbour_node) and not self.is_visited(potential_neighbour_node):
                neighbours.append(potential_neighbour_node)
        return neighbours

    def remove_wall(self, current_node, other_node):
        (cx, cy) = current_node
        (ox, oy) = other_node
        self.walls[(cy + oy) // 2][(cx + ox) // 2] = 0

    def __str__(self):
        return '\n'.join([''.join(str(x)) for x in self.walls])


def build_maze_grid_dfs(n_rows, n_columns):
    grid = Grid(n_rows * 2 + 1, n_columns * 2 + 1)
    current_node = (1, 1)
    stack = [current_node]
    grid.set_visited(current_node)
    path = [current_node]
    while len(stack) > 0:
        current_node = stack.pop()
        neighbours = grid.get_unvisited_neighbours(current_node)
        univisted_neighbours = [n for n in neighbours if not grid.is_visited(n)]
        if len(neighbours) > 0:
            pick_random_node = random.choice(univisted_neighbours)
            grid.remove_wall(current_node, pick_random_node)
            grid.set_visited(pick_random_node)
            stack.append(pick_random_node)
            path.append(pick_random_node)
        else:
            if len(path) > 0:
                stack.append(path.pop())
    return grid.walls


# Dijkstra's algorithm for pathfinding in a maze
def calculate_neighbouring_nodes(node, maze):
    maze_height = len(maze)
    maze_width = len(maze[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    (x, y) = node
    result_neigbours = {}
    for (dx, dy) in directions:
        neighbour_y = y + dy
        neighbour_x = x + dx
        if 0 <= neighbour_y < maze_height and 0 <= neighbour_x < maze_width:
            if maze[neighbour_y][neighbour_x] == 0:
                result_neigbours[(neighbour_x, neighbour_y)] = 1
    return result_neigbours


def solve_maze(maze, start_node, end_node):
    maze_height = len(maze)
    maze_width = len(maze[0])
    assert maze[start_node[1]][start_node[0]] == 0, "Start node must point to a zero of the maze array"
    assert maze[end_node[1]][end_node[0]] == 0, "End node must point to a zero of the maze array"

    nodes = [(x, y) for x in range(maze_width) for y in range(maze_height) if maze[y][x] == 0]
    neighbouring_nodes = {node: calculate_neighbouring_nodes(node, maze) for node in nodes}

    open_nodes = [start_node]
    parentNodes = {start_node: None}
    nodeGValues = {start_node: 0}
    closed_list = []

    while len(open_nodes) > 0:
        sorted_open_nodes = sorted(open_nodes, key=lambda n: nodeGValues[n])
        current_node = sorted_open_nodes[0]
        current_distance = nodeGValues[current_node]
        closed_list.append(current_node)
        open_nodes.remove(current_node)

        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parentNodes[current_node]
            return path[::-1]

        for neighbour_node, neighbour_distance in neighbouring_nodes[current_node].items():
            if neighbour_node not in closed_list:
                tentative_gValue = current_distance + neighbour_distance
                if neighbour_node not in open_nodes:
                    open_nodes.append(neighbour_node)
                if neighbour_node not in nodeGValues or tentative_gValue < nodeGValues[neighbour_node]:
                    nodeGValues[neighbour_node] = tentative_gValue
                    parentNodes[neighbour_node] = current_node
    return None


# Display the maze graphically using pygame
def display_maze_graphically(walls, path=None):
    pygame.init()
    display_cell_size = 20
    green = (0, 155, 0)
    brown = (205, 133, 63)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    display_width = len(walls[0]) * display_cell_size
    display_height = len(walls) * display_cell_size

    pygame.display.set_caption("Maze Solver")
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    gameDisplay.fill(brown)

    for y, row_of_cells in enumerate(walls):
        for x, cell in enumerate(row_of_cells):
            color = green if cell == 1 else brown
            pygame.draw.rect(gameDisplay, color,
                             pygame.Rect(x * display_cell_size, y * display_cell_size, display_cell_size - 1,
                                         display_cell_size - 1))

    if path:
        for node in path:
            pygame.draw.rect(gameDisplay, blue, pygame.Rect(node[0] * display_cell_size, node[1] * display_cell_size,
                                                            display_cell_size - 1, display_cell_size - 1))

        start_node = path[0]
        end_node = path[-1]
        pygame.draw.rect(gameDisplay, red,
                         pygame.Rect(start_node[0] * display_cell_size, start_node[1] * display_cell_size,
                                     display_cell_size - 1, display_cell_size - 1))
        pygame.draw.rect(gameDisplay, red, pygame.Rect(end_node[0] * display_cell_size, end_node[1] * display_cell_size,
                                                       display_cell_size - 1, display_cell_size - 1))

    pygame.display.flip()
    input("Press Enter to quit...")


if __name__ == "__main__":
    size_x = 8
    size_y = 10
    maze_grid = build_maze_grid_dfs(size_y, size_x)

    start = (1, 1)  # Start position
    end = (size_x * 2 - 1, size_y * 2 - 1)  # End position

    path = solve_maze(maze_grid, start, end)

    print("Generated Maze:")
    for row in maze_grid:
        print(''.join(str(x) for x in row))

    print("Path:", path)

    display_maze_graphically(maze_grid, path)
