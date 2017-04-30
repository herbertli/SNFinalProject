import json

INFINITY = 1e9

def convert_votes_to_adjacency(data):
    adj_matrix = {}
    for name in data:
        adj_matrix[name] = {}
        for other_name in data[name]:
            adj_matrix[name][other_name] = int(data[name][other_name]) / int(data[name][name])
    return adj_matrix


def convert_money_to_adjacency(data):
    new_data = {}

    industries = data.keys()
    for industry in industries:
        senators = data[industry].keys()
        for senator in senators:
            if senator not in new_data:
                new_data[senator] = {}
            for other_senator in senators:
                if other_senator not in new_data[senator]:
                    new_data[senator][other_senator] = 1
                else:
                    new_data[senator][other_senator] += 1

    adj_matrix = {}
    for name in new_data:
        adj_matrix[name] = {}
        for other_name in new_data[name]:
            adj_matrix[name][other_name] = int(new_data[name][other_name]) / int(new_data[name][name])
    return adj_matrix


def get_diameter(distances):
    max_dist = 0
    for i in distances:
        for j in distances:
            if distances[i][j] != INFINITY:
                max_dist = max(max_dist, distances[i][j])
    return max_dist


def get_average_distance(distances):
    total = 0
    counter = 0
    for i in distances:
        for j in distances:
            if distances[i][j] != INFINITY:
                total += distances[i][j]
                counter += 1
    return total / counter


def floyd_warshall(adj_matrix, threshold):
    senators = list(adj_matrix.keys())
    distances = {}

    for i in senators:
        distances[i] = {}
        for j in senators:
            distances[i][j] = INFINITY

    for i in senators:
        adj_matrix[i][i] = 0

    for i in adj_matrix:
        for j in adj_matrix[i]:
            if adj_matrix[i][j] >= threshold:
                distances[i][j] = 1

    for k in distances:
        for i in distances:
            for j in distances:
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]

    return distances


def get_stats(adj_matrix, threshold):
    distances = floyd_warshall(adj_matrix, threshold)
    diameter = get_diameter(distances)
    average = get_average_distance(distances)
    print("Threshold:", threshold)
    print("Average distance is", average)
    print("Diameter of graph is", diameter)
    return True


if __name__ == "__main__":

    filename = input("(v)oting data, or (m)oney data: ")
    # threshold = float(input("Enter threshold (enter 50 for 50%): "))
    if filename == "v":
        with open("vdata.json", "r") as f:
            data = json.load(f)
            data = convert_votes_to_adjacency(data)
            for i in range(50, 101, 10):
                get_stats(data, i / 100)
    elif filename == "m":
        with open("mdata.json", "r") as f:
            data = json.load(f)
            data = convert_money_to_adjacency(data)
            for i in range(50, 101, 10):
                get_stats(data, i / 100)
    else:
        print("Invalid option (case sensitive)")