import sys
import csv
from random import random


class MovieEnvironment:
    def __init__(self):
        filepath = r"disney-movies-data.csv"
        self.titles = []
        self.length = 0
        self.__tdict = {}
        self.__adj_list = {}

        self.__read_movie_data(filepath)
        self.__generate_graph()

    def __read_movie_data(self, filepath):
        file = open(filepath, "r")
        data = list(csv.reader(file, delimiter=","))
        self.titles = [row[0] for row in data]
        file.close()
        self.length = len(self.titles)

    def __generate_graph(self):
        i = 0
        while i < 500:  # number of edges in the graph.
            r1 = int(random() * self.length)
            r2 = int(random() * self.length)
            while r2 == r1:
                r2 = int(random() * self.length)

            while (r1, r2) in self.__tdict.keys() or (r2, r1) in self.__tdict.keys():
                r2 = int(random() * self.length)

            self.__tdict[(r1, r2)] = 1
            self.__tdict[(r2, r1)] = 1

            weight = random()
            self.__adj_list.setdefault(self.titles[r1], {})[self.titles[r2]] = (
                round(weight, 2) * 100
            )
            self.__adj_list.setdefault(self.titles[r2], {})[self.titles[r1]] = (
                round(weight, 2) * 100
            )
            i += 1

    def get_neighbours(self, m1):
        """
        Returns the neighbours (similar movies) for a movie.

        :param str m1: The movie name whose neighbours to find.
        :return dict[str,float]: The dictionary of neighbour nodes and their link weights (0-100) as float which show similarity (lower value means more similar).
        """
        return self.__adj_list[m1]

    def display_graph(self):
        import networkx as nx

        g = nx.DiGraph(self.__adj_list)
        nx.draw(g, with_labels=True, font_weight="bold")
        import matplotlib.pyplot as plt

        plt.show()


""" Your code starts here   """


def breadth_first_search(env, movie1, movie2):
    """
    Returns the shortest path from movie1 to movie2 (ignore the weights).
    """
    frontier = [(movie1, [movie1])]  # Using a tuple to store both node and path
    visited = []
    search_tree_nodes = 0
    moves_to_goal = 0
    dead_ends = 0

    while frontier:
        node, path = frontier.pop(0)

        if node == movie2:
            return {
                "path": path,
                "search_tree_nodes": search_tree_nodes,
                "moves_to_goal": moves_to_goal,
                "dead_ends": dead_ends,
            }

        visited.append(node)
        search_tree_nodes += 1

        neighbours = env.get_neighbours(node)

        if not neighbours:
            dead_ends += 1
            continue

        for neighbour in neighbours:
            if neighbour not in visited:
                frontier.append((neighbour, path + [neighbour]))
                moves_to_goal += 1

    return False

    # frontier = [movie1]
    # visited = []

    # while len(frontier) > 0:
    #     node = frontier.pop(0)
    #     if node == movie2:
    #         visited.append(node)
    #         return visited
    #     visited.append(node)
    #     frontier.extend(env.get_neighbours(node).keys())


def depth_first_search(env, movie1, movie2):
    """
    Returns the path from movie1 to movie2
    """
    frontier = [movie1]
    visited = []
    search_tree_nodes = 0
    moves_to_goal = 0
    dead_ends = 0

    while frontier:
        node = frontier.pop()

        if node == movie2:
            return {
                "path": visited + [node],
                "search_tree_nodes": search_tree_nodes,
                "moves_to_goal": moves_to_goal,
                "dead_ends": dead_ends,
            }

        if node not in visited:
            visited.append(node)
            search_tree_nodes += 1
            moves_to_goal += 1  # Increment only once per iteration
            frontier = list(env.get_neighbours(node).keys()) + frontier

    return False
    # frontier = [movie1]
    # visited = []

    # """ add to list from front """
    # while len(frontier) > 0:
    #     node = frontier.pop()
    #     if node == movie2:
    #         visited.append(node)
    #         return visited
    #     if node not in visited:
    #         visited.append(node)
    #         frontier = list(env.get_neighbours(node).keys()) + frontier

    # return False


def uniform_cost_search(env, movie1, movie2):
    """priority queue"""
    node_start = {"node": movie1, "value": 0, "path": [movie1]}
    frontier = [node_start]
    explored = set()
    search_tree_nodes = 0
    moves_to_goal = 0
    dead_ends = 0

    while len(frontier) > 0:
        min_dict = min(frontier, key=lambda x: x["value"])
        frontier.remove(min_dict)
        node = min_dict["node"]

        if node == movie2:
            return {
                "path": min_dict["path"],
                "weight": min_dict["value"],
                "search_tree_nodes": search_tree_nodes,
                "moves_to_goal": moves_to_goal,
                "dead_ends": dead_ends,
                "visied_nodes": explored,
            }

        explored.add(node)
        search_tree_nodes += 1

        neighbours = env.get_neighbours(node)

        if not neighbours:  # Check for dead-end
            dead_ends += 1
            continue

        neighbours = [
            {"node": movie, "value": weights} for movie, weights in neighbours.items()
        ]

        value_to_add = min_dict["value"]
        for neighbor in neighbours:
            neighbor["value"] += value_to_add
            neighbor["path"] = min_dict["path"] + [neighbor["node"]]

        for neighbour in neighbours:
            child = neighbour

            if child["node"] not in explored and not any(
                item["node"] == child["node"] for item in frontier
            ):
                frontier.append(child)
                moves_to_goal += 1
            elif any(
                item["node"] == child["node"] and child["value"] < item["value"]
                for item in frontier
            ):
                frontier = [
                    (
                        child
                        if item["node"] == child["node"]
                        and child["value"] < item["value"]
                        else item
                    )
                    for item in frontier
                ]

    return False

    # node_start = {"node": movie1, "value": 0, "path": [movie1]}
    # frontier = [node_start]
    # explored = set()

    # while len(frontier) > 0:
    #     min_dict = min(frontier, key=lambda x: x["value"])
    #     frontier.remove(min_dict)
    #     node = min_dict["node"]

    #     if node == movie2:
    #         return {"path": min_dict["path"], "weight": min_dict["value"]}

    #     explored.add(node)
    #     neighbours = env.get_neighbours(node)

    #     neighbours = [
    #         {"node": movie, "value": weights} for movie, weights in neighbours.items()
    #     ]

    #     value_to_add = min_dict["value"]
    #     for neighbor in neighbours:
    #         neighbor["value"] += value_to_add
    #         neighbor["path"] = min_dict["path"] + [neighbor["node"]]

    #     for neighbour in neighbours:
    #         child = neighbour

    #         if child["node"] not in explored and not any(
    #             item["node"] == child["node"] for item in frontier
    #         ):
    #             frontier.append(child)
    #         elif any(
    #             item["node"] == child["node"] and child["value"] < item["value"]
    #             for item in frontier
    #         ):
    #             frontier = [
    #                 (
    #                     child
    #                     if item["node"] == child["node"]
    #                     and child["value"] < item["value"]
    #                     else item
    #                 )
    #                 for item in frontier
    #             ]

    # return False
    # node_start = {"node": movie1, "value": 0}
    # frontier = [node_start]
    # explored = set()

    # while len(frontier) > 0:
    #     min_dict = min(frontier, key=lambda x: x["value"])
    #     frontier.remove(min_dict)
    #     node = min_dict["node"]
    #     if node == movie2:
    #         explored.add(node)
    #         return list(explored)

    #     explored.add(node)
    #     neighbours = env.get_neighbours(node)

    #     neighbours = [
    #         {"node": movie, "value": weights} for movie, weights in neighbours.items()
    #     ]

    #     value_to_add = min_dict["value"]
    #     for neighbor in neighbours:
    #         neighbor["value"] += value_to_add

    #     for neighbour in neighbours:
    #         child = neighbour
    #         print(child)

    #         if child["node"] not in explored and not any(
    #             item["node"] == child["node"] for item in frontier
    #         ):
    #             frontier.append(child)
    #         elif any(
    #             item["node"] == child["node"] and child["value"] < item["value"]
    #             for item in frontier
    #         ):
    #             frontier = [
    #                 (
    #                     child
    #                     if item["node"] == child["node"]
    #                     and child["value"] < item["value"]
    #                     else item
    #                 )
    #                 for item in frontier
    #             ]

    # return False


""" Your code ends here     """


if __name__ == "__main__":
    env = MovieEnvironment()

    movie1 = input("enter movie1 name:")
    i = 1
    while movie1 not in env.titles:
        print("name not in the list")
        movie1 = input("enter movie1 name:")
        i += 1
        if i >= 3:
            sys.exit()

    movie2 = input("enter movie2 name:")
    i = 1
    while movie2 not in env.titles:
        print("name not in the list")
        movie2 = input("enter movie1 name:")
        i += 1
        if i >= 3:
            sys.exit()

    print("Breadth-First Search:")
    print(breadth_first_search(env, movie1, movie2))

    print("\nDepth-First Search:")
    print(depth_first_search(env, movie1, movie2))

    print("\nUniform Cost Search:")
    print(uniform_cost_search(env, movie1, movie2))


# env.display_graph()
