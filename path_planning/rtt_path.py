import random
import math
from matplotlib.patches import Rectangle, Circle
from mapping.map_builder import create_map

def rtt_path_planning():
    import matplotlib.pyplot as plt

    class Node:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.parent = None

    def distance(node1, node2):
        return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

    def get_random_node(arena_width, arena_height):
        return Node(random.uniform(0, arena_width), random.uniform(0, arena_height))

    def is_collision(node, obstacles):
        for obs in obstacles:
            if obs.contains_point((node.x, node.y)):
                return True
        return False

    def get_nearest_node(node_list, random_node):
        nearest_node = node_list[0]
        min_dist = distance(nearest_node, random_node)
        for node in node_list:
            dist = distance(node, random_node)
            if dist < min_dist:
                nearest_node = node
                min_dist = dist
        return nearest_node

    def steer(from_node, to_node, extend_length=10.0):
        new_node = Node(from_node.x, from_node.y)
        dist = distance(from_node, to_node)
        if dist > extend_length:
            theta = math.atan2(to_node.y - from_node.y, to_node.x - from_node.x)
            new_node.x += extend_length * math.cos(theta)
            new_node.y += extend_length * math.sin(theta)
        else:
            new_node = to_node
        new_node.parent = from_node
        return new_node

    def generate_path(goal_node):
        path = []
        node = goal_node
        while node is not None:
            path.append((node.x, node.y))
            node = node.parent
        return path[::-1]

    def rtt_path_planning(start, goal, obstacles, arena_width, arena_height, max_iter=500):
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])
        node_list = [start_node]

        for _ in range(max_iter):
            random_node = get_random_node(arena_width, arena_height)
            nearest_node = get_nearest_node(node_list, random_node)
            new_node = steer(nearest_node, random_node)

            if not is_collision(new_node, obstacles):
                node_list.append(new_node)

            if distance(new_node, goal_node) < 10.0:
                goal_node.parent = new_node
                node_list.append(goal_node)
                break

        path = generate_path(goal_node)
        return path

    def plot_path(path, obstacles):
        fig, ax = plt.subplots()
        create_map()
        for obs in obstacles:
            ax.add_patch(obs)
        path_x, path_y = zip(*path)
        ax.plot(path_x, path_y, '-r')
        plt.show()

    # Example usage
    start = (10, 10)
    goal = (1000, 1000)
    obstacles = [
        Rectangle((943, 0), 200, 300, color="blue", alpha=0.5),
        Rectangle((943, 0), 100, 200, color="green", alpha=0.5),
        Circle((0, 0), 230.5, color="blue", alpha=0.5),
        Circle((0, 0), 200, color="green", alpha=0.5),
        Circle((0, 0), 150.5, color="red", alpha=0.5)
    ]
    path = rtt_path_planning(start, goal, obstacles, arena_width, arena_height)
    plot_path(path, obstacles)