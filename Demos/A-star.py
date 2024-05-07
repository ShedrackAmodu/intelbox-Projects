import tkinter as tk
from pyamaze import maze, COLOR, agent
from queue import PriorityQueue

# Define the heuristic function for A* search
def heuristic(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

# A* search algorithm
def astar_search(start, goal, maze):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_node in maze.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                frontier.put(next_node, priority)
                came_from[next_node] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# Function to initialize GUI and start the simulation
def initialize_gui():
    window = tk.Tk()
    window.title("Maze Solver")

    def solve_maze():
        m = maze(10, 25)
        m.CreateMaze(loopPercent=100)
        start = (1, 1)
        goal = (9, 23)
        path = astar_search(start, goal, m)
        a = agent(m, footprints=True, filled=True)
        m.addLabel('PATH FINDER', location='bottom', color='white', size=30)
        m.tracePath({a:m.path}, delay=200)
        m.run()

    solve_button = tk.Button(window, text="Solve Maze", command=solve_maze)
    solve_button.pack(pady=20)

    window.mainloop()

initialize_gui()


