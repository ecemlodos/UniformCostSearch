import csv
from queue import PriorityQueue


class CityNotFoundError(Exception):
    def __init__(self, city):
        print("%s does not exist" % city)


# Implement this function to read data into an appropriate data structure.
def build_graph(path):
    file = open(path,'r')
    routes = {}
    next(file)
    for row in file:
        row = row.split(',')
        routes.setdefault(row[0], []).append((row[1],row[2]))
        routes.setdefault(row[1], []).append((row[0], row[2]))

    file.close()
    return routes


# Implement this function to perform uniform cost search on the graph.
def uniform_cost_search(graph, start, end):
    visited = set()
    route = []
    priority_queue = PriorityQueue()
    priority_queue.put((0, [start]))

    while priority_queue:
        if priority_queue.empty():
            print('distance: infinite \nroute: \nnone')
            break

        distance, route = priority_queue.get()
        city = route[len(route)-1]

        if city not in visited:
            visited.add(city)
            if city == end:
                route.append(distance)
                display_route(graph,route)
                return route

        childs = graph[city]
        neighbour=[i[0] for i in childs]

        for i in neighbour:
            if i not in visited:
                total_distance = distance + int(city_to_neighbour(graph, city, i))
                temp = route[:]
                temp.append(i)
                priority_queue.put((total_distance, temp))

    return priority_queue

def city_to_neighbour(graph, current, neighbour):
    index = [i[0] for i in graph[current]].index(neighbour)
    return graph[current][index][1]


def display_route(graph,route):
    length = len(route)
    distance = route[-1]
    print()
    print('Distance between cities: %s km'%(distance))
    print()
    print('Best route option: ')
    count = 0
    while count < (length-2):
        km = city_to_neighbour(graph, route[count], route[count+1])
        print('%s -> %s %s' %(route[count],route[count+1],km))
        count+=1
    return


# Implement main to call functions with appropriate try-except blocks
if __name__ == "__main__":
    while True:
        try:
            inputFile = input("Enter road map path: ")
            test = open(inputFile, 'r').readlines()
        except FileNotFoundError:
            print("Wrong file or file path, please try again!")
        else:
            break

    graph = build_graph(inputFile)

    while True:
        try:
            start = input("Enter the start city: ")
            if start not in graph:
                raise CityNotFoundError(start)
            break
        except CityNotFoundError:
            print("City not found on map, choose another city!")

    while True:
        try:
            end = input("Enter the destination city: ")
            if end not in graph:
                raise CityNotFoundError(end)
            break
        except CityNotFoundError:
            print("City not found on map, choose another city!")

    uniform_cost_search(graph, start, end)
    
    pass
