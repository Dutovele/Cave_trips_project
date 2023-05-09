from collections import defaultdict
import numpy as np

num_caves = 0
num_paths = 0
max_path_len = 0
min_path_len = 0
all_paths = 0

class Stack:
  def __init__(self):
    self.storage = []
  def isEmpty(self):
    return len(self.storage) == 0
  def push(self, node):
    self.storage.append(node)
  def pop(self):
    return self.storage.pop()


class Graph:

    def __init__(self, num_caves):
        self.V = num_caves
        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.edges = []

    # function to add an edge to graph
    def addEdge(self, u, v, time):
        self.graph[u].append([v, time])
        self.edges.append([u, v, time])


def create_graph(dir):
    global num_caves
    global num_paths
    global max_path_len
    global min_path_len

    line_number = 0

    file = open(dir, 'r')
    for line in file:
        if line_number == 0:
            num_caves, num_paths, min_path_len, max_path_len = line.split(" ")
            num_caves = int(num_caves)
            num_paths = int(num_paths)
            min_path_len = int(min_path_len)
            max_path_len = int(max_path_len)

            # print(num_caves, num_paths, min_path_len, max_path_len)
            g.V = num_caves

        else:
            templine = line.strip("\n")
            v1, v2, time = templine.split(" ")
            v1 = int(v1)
            v2 = int(v2)
            time = int(time)
            # print(v1,v2,time)
            g.addEdge(v1,v2,time)
            g.addEdge(v2, v1, time)

        line_number += 1
    file.close()

def make_neib_matrix(g):
    edges = np.array(g.edges)
    neib_matrix = np.zeros((num_caves, num_caves), dtype=int)
    neib_matrix[edges[:,0], edges[:,1]] = edges[:,2]
    # print("Adjacency matrix for neighbours")
    # print_matrix(neib_matrix)
    return neib_matrix

def print_matrix(matrix):

    for row in range(len(matrix)):
        print("   ".join(map(str, matrix[row])))


def find_path():

    possible_paths = []

    for e in g.edges:
        if e[1] > e[0]:
            for s_neib in g.graph[e[0]]:
                if s_neib[0] != e[1]:
                    for e_neib in g.graph[e[1]]:
                        if e_neib[0] != e[0]:
                            if check_connections(s_neib[0],e[0],e[1],e_neib[0], neib_matrix):
                                # print("Possible path", [s_neib[0], e[0],e[1], e_neib[0]])
                                possible_paths.append([s_neib[0], e[0],e[1], e_neib[0]])

    # print(possible_paths)

    return possible_paths

def clean_path(possble_paths):

    sortedTup = [tuple(sorted(i)) for i in possble_paths]
    clean_paths = list(set(sortedTup))
    # print(clean_paths)
    return clean_paths


def check_connections(s, x, y, e, neib_matrix):

    if neib_matrix[s][y] == 0:
        if neib_matrix[s][e] != 0:
            if neib_matrix[x][e] == 0:
                return True


def sum_path(x,y,neib_matrix):

    sum = neib_matrix[x][y]
    return sum


def choose_path(clean_paths, neib_matrix):
    global max_path_len
    global min_path_len
    global all_paths

    for i in clean_paths:
        sum = 0
        for j in range(len(i)):
            for k in range(len(i)):
                if k > j:
                    if neib_matrix[i[j]][i[k]] != 0:
                        # print(i[j],i[k])
                        sum += sum_path(i[j],i[k],neib_matrix)
        if sum >= min_path_len and sum <= max_path_len:
            all_paths +=1

        # print("current sum for ", i, "is ", sum)

    print("All paths", all_paths)

g = Graph(num_caves)
create_graph('./pubdata_cavetrips/pub10.in')
# print(g.edges)
neib_matrix = make_neib_matrix(g)
possible_paths = find_path()
clean_paths = clean_path(possible_paths)
choose_path(clean_paths, neib_matrix)